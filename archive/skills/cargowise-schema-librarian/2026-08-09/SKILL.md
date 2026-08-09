---
name: cargowise-schema-librarian
description: >
  Living reference for the CargoWise One read-replica SQL schema as discovered
  through empirical investigation. Contains confirmed table relationships, join
  paths, query patterns, internal table codes, and known replica gaps. Consult
  this skill before writing any CargoWise SQL to avoid re-discovering known
  patterns. Update this skill whenever new schema knowledge is confirmed. All
  findings are also mirrored in the memory MCP knowledge graph under entity
  types CW_Table, CW_View, CW_QueryPattern, CW_ReplicaGap, and CW_TableCode.
---

# CargoWise Schema Librarian

> **Last updated:** 2026-07-23 (2)
> **Source:** Empirical discovery via read-replica SQL investigation
> **Query tool:** `python C:\Users\whanusiewicz\.gemini\config\skills\cargowise-database-query\scripts\query_cw.py "SQL"`

---

## Internal Table Codes

CW uses short codes in cross-reference columns (e.g. `EQ_ParentTableCode`, `SM_Type`).
These do NOT always match the column prefix of the actual table.

| Code | Table | PK Column |
|------|-------|-----------|
| `JS` | `JobShipment` | `JS_PK` |
| `JK` | `JobConsol` | `JK_PK` |
| `JP` | `JobDocsAndCartage` | `JP_PK` |
| `JD` | `JobDeclaration` | `JE_PK` (prefix mismatch) |
| `OH` | `OrgHeader` | `OH_PK` |
| `B2` | Unknown | TBD |
| `BF` | Unknown | TBD |

**StorageMain SM_Type codes** — each entity type gets its own StorageMain record:

| SM_Type | Entity | Table |
|---------|--------|-------|
| `SHP` | Shipment | `JobShipment` |
| `CIV` | Commercial Invoice | `JobComInvoiceHeader` |
| `CON` | Consolidation | `JobConsol` |
| `ORG` | Organisation | `OrgHeader` |
| `RIN` | Receivable Invoice | `AccTransactionHeader` |

---

## Confirmed Table Relationships

### Consol Routing Tab Standard (SOP)
- Cartage / local delivery legs to final door addresses are **NOT** entered in the Consol Routing tab (`JobConsolTransport`).
- The Consol Routing tab is strictly used for main line transport legs up to the destination airport, ocean port, or rail yard.
- Local door delivery details are managed in `JobDocsAndCartage` / Delivery Cartage.


### Shipment -> Document Tracking (eDocs Tab, lower grid)
```
JobShipment (JS_PK)
  └── JobDocsAndCartage  [JP_ParentID = JS_PK, JP_ParentTableCode = 'JS']
        └── JobRequiredDocument  [EQ_ParentID = JP_PK, EQ_ParentTableCode = 'JP']
```

**Confirmed working SQL:**
```sql
SELECT EQ_DocType, EQ_DocDescription, EQ_DateReceived, EQ_SystemCreateUser
FROM JobRequiredDocument
WHERE EQ_ParentID = (
    SELECT JP_PK FROM JobDocsAndCartage
    WHERE JP_ParentID = (
        SELECT JS_PK FROM JobShipment WHERE JS_HouseBill = 'SXXXXXXXX'
    )
)
ORDER BY EQ_SystemCreateTimeUtc
```

### Consol -> Document Tracking
```
JobConsol (JK_PK)
  └── JobRequiredDocument  [EQ_ParentID = JK_PK, EQ_ParentTableCode = 'JK']
```

### Related eDocs Tree (eDocs left panel in CW UI)
```
StorageMain records for all related entities:
  SM_ParentFK = JS_PK   → SM_Type = SHP  (This Shipment)
  SM_ParentFK = JZ_PK   → SM_Type = CIV  (each Commercial Invoice)
  SM_ParentFK = JK_PK   → SM_Type = CON  (Consol)
  SM_ParentFK = OH_PK   → SM_Type = ORG  (Organisation)
  SM_ParentFK = AH_PK   → SM_Type = RIN  (Receivable Invoice)
```
**Confirmed query to reconstruct the Related eDocs tree:**
```sql
SELECT SM_PK, SM_Type, SM_ParentFK, SM_SystemCreateUser, SM_SystemCreateTimeUtc
FROM StorageMain
WHERE SM_ParentFK IN (
    SELECT JS_PK FROM JobShipment WHERE JS_HouseBill = 'SXXXXXXXX'
    UNION ALL
    SELECT JZ_PK FROM JobComInvoiceHeader JZ
        JOIN JobDeclaration JE ON JE.JE_PK = JZ.JZ_JE
        JOIN JobShipment JS ON JS.JS_PK = JE.JE_JS
        WHERE JS.JS_HouseBill = 'SXXXXXXXX'
    UNION ALL
    SELECT JK_PK FROM JobConsol WHERE JK_UniqueConsignRef = 'CXXXXXXXX'
)
ORDER BY SM_SystemCreateTimeUtc
```
Confirmed working for S00233526 — matched CW UI exactly. StorageDocs file blobs not in replica
(see Replica Gaps), but StorageMain metadata (who created, when, SM_Type) IS available.

### Shipment -> eDocs File Storage (PARTIAL - replica gap)
```
JobShipment (JS_PK)
  └── StorageMain  [SM_ParentFK = JS_PK, SM_Type = 'SHP']
        └── StorageDocs  [SC_SM = SM_PK]  ** SC_SM ZEROED IN REPLICA **
              └── StorageReference  [SR_SM = SM_PK]  ** 0 ROWS IN REPLICA **
```

### PO Number -> Shipment (J&J / Ethicon pattern)
```
JobComInvoiceHeaderRefs  [JCI_Reference = PO#]
  └── JobComInvoiceHeader  [JZ_PK]
        └── JobDeclaration  [JE_PK via JZ_JE column on invoice table]
              └── JobShipment  [JS_PK via JE_JS column on declaration table]
```

### Shipment -> Commercial Invoices
```
JobShipment (JS_PK)
  └── JobDeclaration  [JE_JS = JS_PK]
        └── JobComInvoiceHeader  [JZ_JE = JE_PK]
              └── JobComInvoiceHeaderRefs  [PO# and other refs]
```

### Shipment -> Container / Equipment Type
```
JobShipment (via HAWB or S-Number)
  └── vw_list_ShipDec  [JS_HouseBill or JS_UniqueConsignRef]
        └── JobConsol  [via JK_UniqueConsignRef]
              └── JobContainer  [JC_JK = JK_PK]
                    └── RefContainer  [RC_PK = JC_RC]
```

**Confirmed working SQL to get Container Type by HAWB:**
```sql
SELECT JC_ContainerNum, RC_Code, RC_Description 
FROM JobContainer JC 
LEFT JOIN RefContainer RC ON RC.RC_PK = JC.JC_RC 
WHERE JC.JC_JK IN (
    SELECT JK_PK FROM JobConsol WHERE JK_UniqueConsignRef IN (
        SELECT JK_UniqueConsignRef FROM vw_list_ShipDec WHERE JS_HouseBill = 'WINAES2606041'
    )
)
```

---

## Key Tables Quick Reference

### JobShipment
- Prefix: `JS_`
- PK: `JS_PK` (uniqueidentifier)
- **`JS_UniqueConsignRef`** = the CW **S-number** (e.g. `S00242597`) — use this to look up a shipment by its job/shipment number
- **`JS_HouseBill`** = the actual **HAWB / house bill number** (e.g. `WSA20169191`) — NOT the S-number
- Job number link: `JS_HouseBill` = `JobHeader.JH_JobNum`

> [!IMPORTANT]
> `JS_UniqueConsignRef` and `JS_HouseBill` are NOT the same field. Searching by S-number (e.g. `S00242597`) against `JS_HouseBill` will return **zero rows**. Always use `JS_UniqueConsignRef` for S-number lookups.

### JobHeader
- Prefix: `JH_`
- PK: `JH_PK` -- DIFFERENT from JS_PK, separate entity
- Job number: `JH_JobNum` (matches JS_HouseBill)

### JobDocsAndCartage
- Prefix: `JP_`
- PK: `JP_PK`
- Parent link: `JP_ParentID` + `JP_ParentTableCode`
- Also stores: pickup/delivery dates, custom attributes (JP_CustomAttrib1/2, JP_CustomDate1/2)
- THIS IS THE BRIDGE between JobShipment and JobRequiredDocument

### JobRequiredDocument
- Prefix: `EQ_`
- Key columns: `EQ_DocType`, `EQ_DocDescription`, `EQ_DateReceived`, `EQ_DocUsage`, `EQ_DocNumber`
- Audit: `EQ_SystemCreateUser`, `EQ_SystemCreateTimeUtc`
- Replicated: YES (1M+ rows confirmed)
- Common doc types:

| Code | Description |
|------|-------------|
| `CAD` | Cartage Advice |
| `CIN` / `CIV` | Commercial Invoice |
| `HBL` | House Waybill / House Airway Bill |
| `PKL` | Packing List |
| `INV` | Invoice |
| `VIN` | Vendor Invoice |
| `MBL` | Master Bill of Lading / Master AWB |
| `MAN` | Manifest |
| `EML` | Email Correspondence |
| `IBL` | Inland Bill of Lading |
| `EPR` | Entry Print / Customs Declaration Doc |

### StorageMain
- Prefix: `SM_`
- PK: `SM_PK`
- Link to job: `SM_ParentFK` = job entity PK
- `SM_Type` = entity type (e.g. `SHP` for shipment)
- Replicated: YES

### StorageDocs
- Prefix: `SC_`
- Binary file blobs in `SC_ImageData` (PDFs stored directly in SQL Server)
- `SC_SM` -> StorageMain.SM_PK
- `SC_ImageDataHasValue` = 1 means blob present
- `SC_ExternalStorageSize` = 0 means blob is in DB (not external)
- CRITICAL: `SC_SM` is zeroed (00000000...) in read replica -- job linkage stripped
- Blobs present but cannot be linked to specific jobs from replica

### AccTransactionHeader
- Prefix: `AH_`
- PK: `AH_PK`
- Invoice number: `AH_TransactionNum` (e.g. MIA00011908 — branch prefix + sequential number)
- Reference: `AH_TransactionReference`
- SM_Type when linked to StorageMain: `RIN`
Branch prefix codes confirmed in AH_TransactionNum:
  MIA = Miami
  JFK = New York JFK
  HKG = Hong Kong (confirmed 2026-07-25)
Format: BRANCHXXXXXXXX (branch + sequential number, NOT always 8 digits)

### OrgHeader
- Prefix: `OH_`
- PK: `OH_PK`
- Short code: `OH_Code` (e.g. ETHICOJFK, JOHJOHSQM3)
- Full name: `OH_FullName`
- SM_Type when linked to StorageMain: `ORG`
- Known org: ETHICOJFK = ETHICON US, LLC (OH_PK: FCDB9208-E005-4DD4-A45C-5EE6A7A2CB24)
- Known org: JOHJOHSQM3 = Johnson & Johnson organization code (J&J)

> [!WARNING]
> J&J org codes (OH_Code values like `JOHJOHSQM3`) can appear as **stray values in the HAWB column** of the air report when column shifts occur in the baseline history. They are NOT shipment identifiers. If you see an OH_Code in the HAWB field, the correct HAWB must be looked up via `JS_UniqueConsignRef` (the S-number) in `JobShipment`.
> Confirmed 2026-07-23: `JOHJOHSQM3` was found in HAWB column for S00235926 — real HAWB is `ACAN00034769`.

### GlbStaff
- Prefix: `GS_`
- `GS_Code` = short staff code (e.g. `CV`, `DH1`)
- `GS_LoginName` = wlt.* Windows login
Known codes (confirmed 2026-07-25):
  ~AD  = CWAutoDataImport  → Automated Data Import (eAdaptor)
  ~BP  = CargoWise BP system automation (not a real person)
  CV   = A. Cynthia Vargas
  DH1  = Damarys Hernandez
  DR1  = Donna Rogers  (WLT.donna.rogers)
Confirmed columns: GS_Code, GS_LoginName, GS_FullName, GS_GivenName, GS_Surname
INVALID column: GS_FamilyName (errors — use GS_Surname instead)

### System Audit Columns (confirmed on all major tables)
Every CW entity table carries these four audit columns:
- `JS_SystemCreateUser` / `JK_SystemCreateUser` — staff code who created the record
- `JS_SystemCreateTimeUtc` / `JK_SystemCreateTimeUtc` — UTC timestamp of creation
- `JS_SystemLastEditUser` / `JK_SystemLastEditUser` — staff code who last edited
- `JS_SystemLastEditTimeUtc` / `JK_SystemLastEditTimeUtc` — UTC timestamp of last edit

Also available on vw_list_ShipDec: `JS_SystemCreateTimeUtc` (use for date-range filtering)

Pattern: `~AD` (CWAutoDataImport) as creator = record was auto-generated via eAdaptor
from a partner's CW system. The partner's reference (e.g. HKG00033759) and their
consol number (e.g. C00384546 — which will NOT exist in Walker's replica) are passed
in as external references. The numeric portion of the partner's MBL IS searchable:
  e.g. MBL "20585752251" found via: WHERE JK_MasterBillNum LIKE '%85752251%'

Query pattern — resolve who is handling a shipment:
  SELECT JS_SystemCreateUser, JS_SystemCreateTimeUtc,
         JS_SystemLastEditUser, JS_SystemLastEditTimeUtc
  FROM JobShipment WHERE JS_UniqueConsignRef = 'S00XXXXXX'

### JobComInvoiceHeaderRefs
Prefix: `J2_` (NOT `JCI_` — that prefix does not exist)
- `J2_ReferenceNumber` — primary reference value
- `J2_ReferenceNumber2` — secondary reference
- `J2_ReferenceType` — type code
- `J2_JZ` — FK to JobComInvoiceHeader
- `J2_PK` — primary key

### JobPackLines
- Prefix: `JL_`
- PK: `JL_PK`
- `JL_JS` -> JobShipment.JS_PK

### JobConsol
- Prefix: `JK_`
- PK: `JK_PK`
- Table code: `JK`

### Shipment Lookup by S-Number vs HAWB

**By S-number (JS_UniqueConsignRef):**
```sql
SELECT JS_UniqueConsignRef, JS_HouseBill, JS_TransportMode,
       JS_RL_NKOrigin, JS_RL_NKDestination
FROM JobShipment
WHERE JS_UniqueConsignRef = 'S00242597'
```

**By HAWB (JS_HouseBill):**
```sql
SELECT JS_UniqueConsignRef, JS_HouseBill, JS_TransportMode,
       JS_RL_NKOrigin, JS_RL_NKDestination
FROM JobShipment
WHERE JS_HouseBill = 'WSA20169191'
```

**To resolve S-number from HAWB (or vice versa):**
```sql
SELECT JS_UniqueConsignRef, JS_HouseBill
FROM JobShipment
WHERE JS_HouseBill = 'WSA20169191'
-- Returns: JS_UniqueConsignRef = 'S00242597'
```
Confirmed working 2026-07-23 against replica (shipment WSA20169191 / S00242597).

### Foreign Reference Resolution Chain (eAdaptor Partner Systems)

When an external reference (e.g., from a partner agent's CW system like `HKG00033759` or their local consol `C00384546`) cannot be found directly in Walker's CW instance, you can use the numeric portion of the Master Bill (MBL) to bridge the gap and find Walker's matching shipment and the human handling it.

**Step 1: Find Walker's Consol via MBL**
Extract the numeric portion of the partner's MBL (e.g. `85752251`) and search with wildcards:
```sql
SELECT JK_UniqueConsignRef, JK_MasterBillNum
FROM JobConsol
WHERE JK_MasterBillNum LIKE '%85752251%'
```
*Returns Walker's Consol ID (e.g. `C00122389`).*

**Step 2: Find Walker's House Bill and Parties**
Join the Consol ID against `vw_list_ShipDec`:
```sql
SELECT JS_UniqueConsignRef, JS_ConsignorCode, JS_ConsigneeCode
FROM vw_list_ShipDec
WHERE JS_TableName = 'JobShipment' AND JK_UniqueConsignRef = 'C00122389'
```
*Returns Walker's House Bill (e.g. `S00241563`) and org codes.*

**Step 3: Identify the Responsible Human**
Check the audit columns on the Shipment/Consol to see who is processing it locally. The creator will often be `~AD` (eAdaptor), but the `SystemLastEditUser` will be the real human.
```sql
SELECT JS_SystemCreateUser, JS_SystemLastEditUser
FROM JobShipment WHERE JS_UniqueConsignRef = 'S00241563'
```
*Returns `~AD` (Creator) and `DR1` (Last Editor). Look up `DR1` in `GlbStaff` to get the human (e.g., Donna Rogers).*

---

## Useful Views

### `vw_list_ShipDec`
- Unions JobShipment + JobDeclaration rows together
- WARNING: `JS_PK` in this view is SYNTHETIC -- not equal to `JobShipment.JS_PK`
- `JS_UniqueID` = the real entity PK (equals `JobShipment.JS_PK`)
- `JS_TableName` column tells you which entity type each row represents
- Contains `JP_` columns pulled from JobDocsAndCartage
- Use `JS_UniqueID` (not `JS_PK`) to join back to JobShipment

### `cvw_ShipmentForwarding`
- Forwarding shipment view; `JS_PK` here DOES equal `JobShipment.JS_PK` directly

### `ViewShipmentConsolAndMasterBillNumbers`
- Columns: `VV_PK`, `VV_HouseBill`, `VV_ConsolNumbers`, `VV_MasterBillNumbers`
- Good for resolving house bill -> MAWB

---

## Known Replica Gaps

| Feature | Status | Notes |
|---------|--------|-------|
| Document tracking (types, dates, who filed) | AVAILABLE | Via JobRequiredDocument |
| eDocs file names / list | NOT LINKABLE | SC_SM zeroed in replica |
| eDocs file blobs (actual PDFs) | NOT USABLE | Post-2021 blobs not replicated |
| Related eDocs tree (metadata) | AVAILABLE | Via StorageMain SM_Type + SM_ParentFK |
| RelatedParentMains (multi-parent docs) | EXCLUDED | StorageReference = 0 rows |
| CusStorageDocPivot | EXCLUDED | 0 rows |

**StorageDocs replication history:**
- 2015–mid 2020: Thousands of records/month replicated normally
- 2021 onwards: Near-zero — only 4 records total in all of 2026
- StorageMain IS replicated for all SM_Types (SHP, CIV, CON, ORG, RIN)
- SC_SM always zeroed for post-2021 records
- Document IDs (SC_PK GUIDs) copied from CW UI will NOT resolve in replica for recent jobs
- **Workaround:** Use `StorageMain` to confirm edoc containers exist, use `JobRequiredDocument` for doc type and date tracking

---

## Known J&J / Ethicon Reference Mapping

| J&J Reference Type | CW Location | Status |
|---------------------|-------------|--------|
| PO Number (e.g. 5700422271) | `JobComInvoiceHeaderRefs.J2_ReferenceNumber` | Traceable |
| Invoice # (e.g. 3000079454) | `JobComInvoiceHeader.JZ_InvoiceNumber` | Direct lookup |
| OBD / Delivery # (e.g. 0847778729) | Not in CW refs | SAP internal, not mapped |
| Commercial Invoice # (e.g. 945616771) | `JobDeclaration` entry refs | Traceable |
| Org Code (e.g. JOHJOHSQM3) | `OrgHeader.OH_Code` | Known stray — NOT a HAWB |

### Known Kenvue / J&J Org Codes — Italy EMEA Lanes (confirmed 2026-07-22)
| OH_Code      | Description                          | CW Role  |
|--------------|--------------------------------------|----------|
| KENITAPOM    | Kenvue Italy Pomezia (Santa Palomba) | Shipper  |
| SANITAGOA    | Kenvue/Sanita Genoa (La Spezia area) | Shipper  |
| KENARAJED    | Kenvue Arabia Jeddah                 | Consignee|
| KUEJAFJEA    | Kuehne+Nagel Jeddah/Jebel Ali        | Consignee|
| KENPROJNB    | Kenvue Project Johannesburg          | Consignee|
| JOHJOHPOM    | J&J Pomezia (legacy, pre-Kenvue)     | Shipper  |
| JOHJOHPOM1   | J&J Pomezia v1 (legacy)              | Shipper  |
| JOHJOHPIR    | J&J Piraeus Greece (NOT Italy)       | Shipper  |

Note: KENITAPOM uses Civitavecchia (ITCVV) as actual POL despite contract saying Salerno.
SANITAGOA uses La Spezia (ITSPE) despite contract saying Genoa.
These are active on KOEM1667-KOEM1672 Kenvue contract lanes (see memory graph).
KOEM1673/KOEM1674 (Flero factory → Genoa → Dubai) still unconfirmed — shipper unknown.

---

## How to Update This Skill

When you discover a new confirmed join, table, or pattern:
1. Add it to this SKILL.md under the appropriate section
2. Add to the memory MCP knowledge graph:
   - New table: `memory -> create_entities` with entityType `CW_Table`
   - New relation: `memory -> create_relations`
   - New observation: `memory -> add_observations`
   - New query pattern: `memory -> create_entities` with entityType `CW_QueryPattern`
3. Note the date discovered and whether it was confirmed working against the replica
