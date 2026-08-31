# Uniden Bearcat BC75XLT — Master 300-Channel Scan Plan
**Geographic Focus: Mount Vernon, GA / SE Georgia / Savannah & Atlanta Corridors**

The **Uniden BC75XLT** scanner organizes its 300 memory channels into **10 Banks of 30 Channels each**. This hardware layout unlocks full AM civilian aviation, CB trucker channels (27 MHz), fast scanning (~100 ch/sec), and Close Call RF capture.

---

## 📑 10-Bank Architecture Overview

```
┌──────┬──────────────────────┬─────────────┬──────────────────────────────────────────────────────┐
│ Bank │ Channels             │ Modulation  │ Core Service / Focus                                 │
├──────┼──────────────────────┼─────────────┼──────────────────────────────────────────────────────┤
│ 1    │ CH 001 – 030         │ AM          │ ✈️ Civilian Aviation & Air Traffic Control (Tower/App)│
│ 2    │ CH 031 – 060         │ AM / FM     │ 🚁 Life Flight & Emergency Medical Helicopters       │
│ 3    │ CH 061 – 090         │ AM (HF)     │ 🚚 CB Radio Highway & Interstate 16/75 Truckers       │
│ 4    │ CH 091 – 120         │ NFM / FM    │ 🚂 Freight Railroads (Norfolk Southern, CSX, AAR)    │
│ 5    │ CH 121 – 150         │ FM          │ 🚢 Marine VHF & Coastal Waterways (Ch 16, USCG)      │
│ 6    │ CH 151 – 180         │ NFM         │ 🚒 Public Safety Interop, Fire Mutual Aid & SAR       │
│ 7    │ CH 181 – 210         │ FM          │ 📻 Local Amateur Repeaters (Mount Vernon / Vidalia)   │
│ 8    │ CH 211 – 240         │ FM          │ 🌐 Peach State Intertie & Atlanta Metro Linked Hubs  │
│ 9    │ CH 241 – 270         │ FM / NFM    │ 🛒 GMRS, FRS, MURS & Retail Store Walkies (Walmart)  │
│ 10   │ CH 271 – 300         │ FM          │ 🌧️ NOAA Weather Radio (All 7) & ISS Space Ops         │
└──────┴──────────────────────┴─────────────┴──────────────────────────────────────────────────────┘
```

---

## ✈️ BANK 1 (CH 001–030): Civilian Aviation & Air Traffic Control
*Modulation: AM (108.000 – 136.975 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Location / Facility | Purpose / Function |
|---:|:-----------|:---------------:|:----:|:--------------------|:-------------------|
| 1 | JVX CTAF | 122.8000 | AM | Vidalia Regional Airport | Common Traffic Advisory / UNICOM |
| 2 | JVX AWOS | 121.1250 | AM | Vidalia Regional Airport | Automated Weather Broadcast (Continuous) |
| 3 | TBR CTAF | 122.8000 | AM | Statesboro-Bulloch Co. | UNICOM / Airport Traffic |
| 4 | TBR AWOS | 118.8250 | AM | Statesboro-Bulloch Co. | Automated Weather Broadcast |
| 5 | DBN CTAF | 122.8000 | AM | Dublin Laurens Co. Airport | UNICOM / Airport Traffic |
| 6 | DBN AWOS | 118.3750 | AM | Dublin Laurens Co. Airport | Automated Weather Broadcast |
| 7 | SBO CTAF | 122.8000 | AM | Swainsboro-Emanuel Co. | UNICOM / Airport Traffic |
| 8 | SBO AWOS | 118.5250 | AM | Swainsboro-Emanuel Co. | Automated Weather Broadcast |
| 9 | SAV TWR | 119.1000 | AM | Savannah/Hilton Head Int'l | Main Tower Control (Active runway) |
| 10 | SAV APP1 | 120.4000 | AM | Savannah Approach/Depart | Approach Control East Sector |
| 11 | SAV APP2 | 125.3000 | AM | Savannah Approach/Depart | Approach Control West Sector |
| 12 | SAV GND | 121.9000 | AM | Savannah International | Ground Movement / Taxi |
| 13 | SAV ATIS | 124.5500 | AM | Savannah International | Terminal Information Broadcast |
| 14 | MCN TWR | 124.9500 | AM | Macon Middle GA Regional | Main Control Tower |
| 15 | MCN APP | 124.2000 | AM | Macon Approach/Depart | Approach Radar Control |
| 16 | ZTL SEC1 | 120.4500 | AM | Atlanta ARTCC (Center) | Enroute High Altitude Sector (Macon/Dublin) |
| 17 | ZTL SEC2 | 127.5000 | AM | Atlanta ARTCC (Center) | Enroute High Altitude Sector (South GA) |
| 18 | ZJX SEC1 | 127.5750 | AM | Jacksonville ARTCC | Coastal Georgia Enroute Sector |
| 19 | ZJX SEC2 | 126.7500 | AM | Jacksonville ARTCC | SE Georgia Low Altitude Sector |
| 20 | AIR-EMRG | 121.5000 | AM | International Guard | **Civilian Emergency / Distress / ELT Search** |
| 21 | FSS FLT | 122.2000 | AM | Flight Service Station | Enroute Pilot Weather & Flight Plan Open/Close |
| 22 | AIR-MULT | 122.7500 | AM | Air-to-Air Multicom | Fixed-wing private pilot communications |
| 23 | AIR-AIR | 123.4500 | AM | "Fingers" Oceanic/Enroute | Unofficial pilot-to-pilot chat frequency |
| 24 | HELI-AIR | 123.0500 | AM | Helicopter Air-to-Air | Rotary aircraft flight coordination |
| 25 | HELI-UNI | 123.0750 | AM | Heliport Unicom | General commercial & private heliport advisory |
| 26 | CTRY UN1 | 122.7000 | AM | Unicom (Uncontrolled) | Rural airfields without dedicated tower |
| 27 | CTRY UN2 | 122.7250 | AM | Unicom (Private) | Rural airstrips / Crop dusting operations |
| 28 | CTRY UN3 | 122.9750 | AM | Unicom (High Altitude) | Regional unicom alternate |
| 29 | SAR AIR | 123.1000 | AM | Search and Rescue | Civil Air Patrol / Coast Guard air search |
| 30 | FLIGHT1 | 122.9000 | AM | Multicom Search & Train | Flight instruction / agricultural spraying |

---

## 🚁 BANK 2 (CH 031–060): Life Flight & Emergency Medical Helicopters
*Modulation: AM (Aviation) / FM (Hospital & Dispatch)*

| CH | Tag / Name | Frequency (MHz) | Mode | Operator / Service Area | Description / Function |
|---:|:-----------|:---------------:|:----:|:------------------------|:-----------------------|
| 31 | MED-AIR1 | 123.0250 | AM | **National Medevac Air-to-Air** | Air ambulance enroute inter-helicopter coordination |
| 32 | MED-AIR2 | 123.0500 | AM | Air Evac Lifeteam | Flight coordination & LZ landing zone advisory |
| 33 | MED-AIR3 | 123.0750 | AM | Memorial Health Binnicker | Savannah Medevac inbound advisory |
| 34 | SAV-LZ | 123.1000 | AM | Savannah Hospital LZ | Memorial University Medical Center Helipad |
| 35 | MCN-LZ | 123.0250 | AM | Atrium Health Navicent LZ | Macon Level 1 Trauma Center Helipad |
| 36 | AUG-LZ | 123.0500 | AM | AU Health Augusta LZ | Augusta Regional Trauma / Burn Center LZ |
| 37 | VMED28 | 155.3400 | NFM | **National Medical Calling** | Statewide ambulance-to-hospital emergency triage |
| 38 | VMED29 | 155.3550 | NFM | Medical Coordination | GA EMS mutual aid & multi-casualty transport |
| 39 | VMED30 | 155.3850 | NFM | Hospital State Net | Regional hospital bed status / major disaster net |
| 40 | MED-1 | 463.0000 | FM | UHF Med Net Channel 1 | Direct telemetry & physician medical direction |
| 41 | MED-2 | 463.0250 | FM | UHF Med Net Channel 2 | Paramedic-to-ER doctor consultation |
| 42 | MED-3 | 463.0500 | FM | UHF Med Net Channel 3 | Trauma patient telemetry patch |
| 43 | MED-4 | 463.0750 | FM | UHF Med Net Channel 4 | Cardiac telemetry transmission |
| 44 | MED-5 | 463.1000 | FM | UHF Med Net Channel 5 | Hospital emergency room triage |
| 45 | MED-6 | 463.1250 | FM | UHF Med Net Channel 6 | Critical care inter-facility transfer |
| 46 | MED-7 | 463.1500 | FM | UHF Med Net Channel 7 | Regional medical dispatch & triage |
| 47 | MED-8 | 463.1750 | FM | UHF Med Net Channel 8 | Regional trauma center patch |
| 48 | MED-9 | 462.9500 | FM | UHF Med Net Channel 9 | **Life Flight Helicopter Dispatch (VHF/UHF Patch)** |
| 49 | MED-10 | 462.9750 | FM | UHF Med Net Channel 10 | Life Flight Landing Zone (LZ) Ground Crew Patch |
| 50 | GA-HEMS1 | 155.2800 | NFM | State EMS Tactical 1 | Field EMS disaster response & triage |
| 51 | GA-HEMS2 | 155.2200 | NFM | State EMS Tactical 2 | Rural county ambulance backup dispatch |
| 52 | GA-HEMS3 | 155.2050 | NFM | State EMS Mutual Aid | Cross-county mass casualty evacuation |
| 53 | TOOMBSMED | 155.1750 | NFM | Toombs County EMS | Local ambulance dispatch (Vidalia/Lyons) |
| 54 | MONTGMED | 155.2950 | NFM | Montgomery County EMS | Local ambulance dispatch (Mount Vernon) |
| 55 | LAURNMED | 155.2350 | NFM | Laurens County EMS | Local ambulance dispatch (Dublin) |
| 56 | CANDLRMED | 155.2650 | NFM | Candler County EMS | Local ambulance dispatch (Metter) |
| 57 | EMANLMED | 155.1600 | NFM | Emanuel County EMS | Local ambulance dispatch (Swainsboro) |
| 58 | BULLCHMED | 155.2500 | NFM | Bulloch County EMS | Local ambulance dispatch (Statesboro) |
| 59 | EVANSMED | 155.2200 | NFM | Evans County EMS | Local ambulance dispatch (Claxton) |
| 60 | CHATHMMED | 155.2800 | NFM | Chatham County EMS | Savannah metro mutual aid EMS |

---

## 🚚 BANK 3 (CH 061–090): CB Radio Highway & Trucker Spectrum
*Modulation: AM (26.965 – 27.405 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Channel Designation | Primary Usage & Highlights |
|---:|:-----------|:---------------:|:----:|:-------------------:|:---------------------------|
| 61 | CB 19 | 27.1850 | AM | **Channel 19 (Highway)** | **The Nationwide Trucker Channel** (I-16, I-75, US-280, US-1) |
| 62 | CB 09 | 27.0650 | AM | **Channel 9 (Emergency)** | Official Emergency, Motorist Aid, & REACT |
| 63 | CB 14 | 27.1250 | AM | Channel 14 | Rural chat, local haulers, timber/log trucks |
| 64 | CB 17 | 27.1650 | AM | Channel 17 | North/South alternate highway traffic (I-75) |
| 65 | CB 21 | 27.2150 | AM | Channel 21 | East/West alternate highway traffic (I-16) |
| 66 | CB 06 | 27.0250 | AM | Channel 6 ("Superbowl") | High-power long-distance skip / amplifier testing |
| 67 | CB 11 | 27.0850 | AM | Channel 11 | Historic active calling channel |
| 68 | CB 01 | 26.9650 | AM | Channel 1 | General road chatter |
| 69 | CB 02 | 26.9750 | AM | Channel 2 | General road chatter |
| 70 | CB 03 | 26.9850 | AM | Channel 3 | Rural farm & agricultural transport |
| 71 | CB 04 | 27.0050 | AM | Channel 4 | 4x4 off-road / convoy channel |
| 72 | CB 05 | 27.0150 | AM | Channel 5 | Local haulers |
| 73 | CB 07 | 27.0350 | AM | Channel 7 | General road chatter |
| 74 | CB 08 | 27.0550 | AM | Channel 8 | General road chatter |
| 75 | CB 10 | 27.0750 | AM | Channel 10 | Regional road traffic |
| 76 | CB 12 | 27.1050 | AM | Channel 12 | General road chatter |
| 77 | CB 13 | 27.1150 | AM | Channel 13 | Marine & RV convoy channel |
| 78 | CB 15 | 27.1350 | AM | Channel 15 | General road chatter |
| 79 | CB 16 | 27.1550 | AM | Channel 16 | 4x4 / Trail riders channel |
| 80 | CB 18 | 27.1750 | AM | Channel 18 | Secondary highway alternate |
| 81 | CB 20 | 27.2050 | AM | Channel 20 | General road chatter |
| 82 | CB 22 | 27.2250 | AM | Channel 22 | General road chatter |
| 83 | CB 23 | 27.2550 | AM | Channel 23 | Shared general road channel |
| 84 | CB 24 | 27.2350 | AM | Channel 24 | General road chatter |
| 85 | CB 25 | 27.2450 | AM | Channel 25 | General road chatter |
| 86 | CB 26 | 27.2650 | AM | Channel 26 | General road chatter |
| 87 | CB 27 | 27.2750 | AM | Channel 27 | General road chatter |
| 88 | CB 28 | 27.2850 | AM | Channel 28 | Long-range skip channel |
| 89 | CB 38 | 27.3850 | AM | Channel 38 | LSB Calling / Long-distance chatter |
| 90 | CB 40 | 27.4050 | AM | Channel 40 | Upper band highway talk |

---

## 🚂 BANK 4 (CH 091–120): Freight Railroad (AAR Utility Channels)
*Modulation: NFM (160.200 – 161.600 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Designation | Railroad Operations & Usage |
|---:|:-----------|:---------------:|:----:|:------------|:----------------------------|
| 91 | AAR-046 | 160.8000 | NFM | **AAR 046** | **Nationwide Standard Road Main** (Train crew to dispatcher) |
| 92 | AAR-008 | 160.2300 | NFM | AAR 008 | Norfolk Southern Road / Dispatcher |
| 93 | AAR-096 | 161.5500 | NFM | **AAR 096** | **End-of-Train (EOT) Device & Brake Telemetry** |
| 94 | AAR-073 | 161.2050 | NFM | AAR 073 | Norfolk Southern Yard Switching & Train Make-up |
| 95 | AAR-042 | 160.7400 | NFM | AAR 042 | Regional Rail Switching & Industrial Spurs |
| 96 | AAR-056 | 160.9500 | NFM | AAR 056 | Norfolk Southern Atlanta Division Dispatcher |
| 97 | AAR-064 | 161.0700 | NFM | AAR 064 | Norfolk Southern Coastal Division Dispatcher |
| 98 | AAR-084 | 161.3700 | NFM | AAR 084 | CSX Road Channel (SE Georgia) |
| 99 | AAR-032 | 160.5900 | NFM | AAR 032 | CSX Dispatcher Channel |
| 100 | AAR-020 | 160.4100 | NFM | AAR 020 | CSX Yard Operations |
| 101 | AAR-014 | 160.3200 | NFM | AAR 014 | Rail Maintenance-of-Way (Track crews & repair) |
| 102 | AAR-072 | 161.1900 | NFM | AAR 072 | Rail Defect Detector (Hotbox / dragging equipment) |
| 103 | AAR-086 | 161.4000 | NFM | AAR 086 | Rail Defect Detector Voice Broadcast |
| 104 | AAR-094 | 161.5200 | NFM | AAR 094 | Rail Intermodal Facility Ground Crew |
| 105 | AAR-022 | 160.4400 | NFM | AAR 022 | Shortline Railroad Local Road Channel |
| 106 | AAR-038 | 160.6800 | NFM | AAR 038 | Rail Bridge Tender & River Crossing |
| 107 | AAR-050 | 160.8600 | NFM | AAR 050 | Secondary Road Channel |
| 108 | AAR-058 | 160.9800 | NFM | AAR 058 | Secondary Dispatcher |
| 109 | AAR-066 | 161.1000 | NFM | AAR 066 | Industrial switching |
| 110 | AAR-076 | 161.2500 | NFM | AAR 076 | Maintenance-of-Way |
| 111 | AAR-080 | 161.3100 | NFM | AAR 080 | Rail Safety Inspections |
| 112 | AAR-088 | 161.4300 | NFM | AAR 088 | Train Yard Hump Operations |
| 113 | AAR-090 | 161.4600 | NFM | AAR 090 | Yard Office |
| 114 | AAR-092 | 161.4900 | NFM | AAR 092 | Yard Car Inspectors |
| 115 | AAR-018 | 160.3800 | NFM | AAR 018 | Signal Department Maintenance |
| 116 | AAR-026 | 160.5000 | NFM | AAR 026 | Railroad Police Patrol |
| 117 | AAR-034 | 160.6200 | NFM | AAR 034 | Railroad Police Emergency |
| 118 | AAR-048 | 160.8300 | NFM | AAR 048 | Local switching |
| 119 | AAR-060 | 161.0100 | NFM | AAR 060 | Local switching |
| 120 | AAR-070 | 161.1600 | NFM | AAR 070 | Local switching |

---

## 🚢 BANK 5 (CH 121–150): Marine VHF & Coastal Waterways
*Modulation: FM (156.000 – 157.425 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Channel | Maritime Safety & Operational Usage |
|---:|:-----------|:---------------:|:----:|:-------:|:-----------------------------------|
| 121 | MAR 16 | 156.8000 | FM | **Ch 16** | **International Distress, Safety & Hailing** |
| 122 | MAR 09 | 156.4500 | FM | Ch 09 | Secondary Boater Calling & Recreational Hailing |
| 123 | MAR 13 | 156.6500 | FM | Ch 13 | **Bridge-to-Bridge Navigational Safety** (Tug/Barge) |
| 124 | MAR 22A | 157.1000 | FM | **Ch 22A** | **US Coast Guard Liaison & Maritime Safety Broadcasts** |
| 125 | MAR 06 | 156.3000 | FM | Ch 06 | Inter-ship Safety & Coast Guard SAR Coordination |
| 126 | MAR 12 | 156.6000 | FM | Ch 12 | Port of Savannah Vessel Traffic & Harbor Pilots |
| 127 | MAR 14 | 156.7000 | FM | Ch 14 | Port Operations & Commercial Docking |
| 128 | MAR 21A | 157.0500 | FM | Ch 21A | US Coast Guard Working Channel |
| 129 | MAR 23A | 157.1500 | FM | Ch 23A | US Coast Guard Working Channel |
| 130 | MAR 83A | 157.1750 | FM | Ch 83A | US Coast Guard Auxiliary Patrols |
| 131 | MAR 68 | 156.4250 | FM | Ch 68 | Recreational Non-commercial Ship-to-Ship |
| 132 | MAR 69 | 156.4750 | FM | Ch 69 | Recreational Non-commercial Ship-to-Ship |
| 133 | MAR 71 | 156.5750 | FM | Ch 71 | Recreational Non-commercial Ship-to-Ship |
| 134 | MAR 72 | 156.6250 | FM | Ch 72 | Inter-ship Working (Recreational/Fishing) |
| 135 | MAR 78A | 156.9250 | FM | Ch 78A | Non-commercial working |
| 136 | MAR 79A | 156.9750 | FM | Ch 79A | Commercial vessel operations |
| 137 | MAR 80A | 157.0250 | FM | Ch 80A | Commercial vessel operations |
| 138 | MAR 01A | 156.0500 | FM | Ch 01A | Port Operations |
| 139 | MAR 05A | 156.2500 | FM | Ch 05A | Vessel Traffic Service (VTS) |
| 140 | MAR 07A | 156.3500 | FM | Ch 07A | Commercial Ship-to-Ship |
| 141 | MAR 08 | 156.4000 | FM | Ch 08 | Commercial Fishing Operations |
| 142 | MAR 10 | 156.5000 | FM | Ch 10 | Commercial Towing / Tugboats |
| 143 | MAR 11 | 156.5500 | FM | Ch 11 | Commercial Vessel Docking |
| 144 | MAR 17 | 156.8500 | FM | Ch 17 | Maritime State & Local Government Control |
| 145 | MAR 18A | 156.9000 | FM | Ch 18A | Commercial Towing / Dredging |
| 146 | MAR 19A | 156.9500 | FM | Ch 19A | Coast Guard Commercial Working |
| 147 | MAR 20A | 157.0000 | FM | Ch 20A | Port Authority |
| 148 | MAR 65A | 156.2750 | FM | Ch 65A | Marine Towing / Salvage |
| 149 | MAR 66A | 156.3250 | FM | Ch 66A | Marina Dockmaster / Fuel Dock |
| 150 | MAR 77 | 156.8750 | FM | Ch 77 | Port Pilot Boat Transfer Operations |

---

## 🚒 BANK 6 (CH 151–180): Public Safety Interop, Fire Mutual Aid & SAR
*Modulation: NFM (150.000 – 460.000 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Interop System | Channel Designation / Purpose |
|---:|:-----------|:---------------:|:----:|:---------------|:------------------------------|
| 151 | VCALL10 | 155.7525 | NFM | DHS / NIFOG | **National VHF Interoperability Calling** |
| 152 | VTAC11 | 151.1375 | NFM | DHS / NIFOG | VHF Tactical Interoperability Channel 11 |
| 153 | VTAC12 | 154.4525 | NFM | DHS / NIFOG | VHF Tactical Interoperability Channel 12 |
| 154 | VTAC13 | 158.7375 | NFM | DHS / NIFOG | VHF Tactical Interoperability Channel 13 |
| 155 | VTAC14 | 159.4725 | NFM | DHS / NIFOG | VHF Tactical Interoperability Channel 14 |
| 156 | VFIRE21 | 154.2800 | NFM | National Fire | **National Fire Mutual Aid Simplex** |
| 157 | VFIRE22 | 154.2650 | NFM | National Fire | Regional Fire Ground Tactical 22 |
| 158 | VFIRE23 | 154.2950 | NFM | National Fire | Regional Fire Ground Tactical 23 |
| 159 | VFIRE24 | 154.2725 | NFM | National Fire | Wildland Fire Incident Command |
| 160 | VFIRE25 | 154.2875 | NFM | National Fire | Wildland Fire Incident Command |
| 161 | VFIRE26 | 154.3025 | NFM | National Fire | Structure Fire Tactical Operations |
| 162 | VLAW31 | 155.4750 | NFM | National Police | **National Law Enforcement Emergency (NLEEF)** |
| 163 | VLAW32 | 155.4825 | NFM | National Police | Law Enforcement Tactical / Chase Net |
| 164 | SAR-NAT | 155.1600 | NFM | National SAR | **National Search and Rescue Simplex** |
| 165 | SAR-SEC | 155.1750 | NFM | State SAR | Georgia SAR Ground Search & K9 Team |
| 166 | UCALL40 | 453.2125 | NFM | DHS / NIFOG | **National UHF Interoperability Calling** |
| 167 | UTAC41 | 453.4625 | NFM | DHS / NIFOG | UHF Tactical Interoperability Channel 41 |
| 168 | UTAC42 | 453.7125 | NFM | DHS / NIFOG | UHF Tactical Interoperability Channel 42 |
| 169 | UTAC43 | 453.8625 | NFM | DHS / NIFOG | UHF Tactical Interoperability Channel 43 |
| 170 | GEMA-1 | 154.9500 | NFM | GA Emergency | Georgia Emergency Management Agency Net |
| 171 | GEMA-2 | 154.9650 | NFM | GA Emergency | State EOC Emergency Operations Channel |
| 172 | GEMA-3 | 155.0250 | NFM | GA Emergency | State Disaster Field Coordination |
| 173 | GFC-1 | 159.2250 | NFM | GA Forestry | GA Forestry Commission Wildfire Dispatch |
| 174 | GFC-2 | 159.2850 | NFM | GA Forestry | Forestry Commission Air Attack / Helitack |
| 175 | GFC-3 | 159.3300 | NFM | GA Forestry | Forestry Ground Firefighting Crews |
| 176 | GFC-4 | 159.3900 | NFM | GA Forestry | Forestry Dozers & Heavy Equipment |
| 177 | GFC-5 | 159.4350 | NFM | GA Forestry | Forestry District Repeater |
| 178 | GDNR-1 | 155.4450 | NFM | GA DNR | GA Dept of Natural Resources (Rangers/Boating) |
| 179 | GDNR-2 | 159.3450 | NFM | GA DNR | DNR Law Enforcement Tactical |
| 180 | GDNR-3 | 159.4650 | NFM | GA DNR | DNR Wildlife Resources |

---

## 📻 BANK 7 (CH 181–210): Local Amateur Repeaters (SE Georgia Corridor)
*Modulation: FM (144.000 – 450.000 MHz)*

| CH | Tag / Name | Frequency (MHz) | Tone | City / Area | Club / Sponsoring System |
|---:|:-----------|:---------------:|:----:|:------------|:-------------------------|
| 181 | K4HAO | 146.6250 | 88.5 | Vidalia (12 mi E) | **Four Rivers ARC (Primary Mount Vernon Machine)** |
| 182 | W4VDA | 147.2400 | 100.0 | Vidalia | Vidalia SKYWARN / Emergency Net |
| 183 | W4MTR | 444.8000 | 141.3 | Metter | Candler County ARES / RACES |
| 184 | K4GAS | 146.9400 | 100.0 | Statesboro | Statesboro ARES / SKYWARN Linked |
| 185 | KF4DG | 147.3900 | 100.0 | Statesboro | Statesboro Amateur Radio Society (STARS) |
| 186 | NC4D | 147.0500 | 100.0 | Statesboro | STARS Club 2m Local Net |
| 187 | WR4A | 145.4500 | 107.2 | Swainsboro | Emanuel County ARC |
| 188 | K4EMN | 147.0000 | 100.0 | Swainsboro | Emanuel County ARES |
| 189 | W4CLA | 147.0750 | 82.5 | Claxton | Evans County ARES |
| 190 | KF4DG-W | 147.1050 | 100.0 | Pembroke | **WVAN Tower (40-mile footprint along I-16)** |
| 191 | W4LHS-1 | 146.9700 | 123.0 | Savannah | **Chatham County ARES / SKYWARN Primary** |
| 192 | W4LHS-2 | 442.7000 | 123.0 | Savannah | **CARS Flagship UHF (850 ft WSAV TV Tower)** |
| 193 | W4LHS-3 | 147.2100 | 210.7 | Savannah | CARS Talmadge Bridge Repeater |
| 194 | W4LHS-4 | 147.3300 | 203.5 | Savannah | CARS East Savannah / EchoLink |
| 195 | W4LHS-5 | 147.1050 | 100.0 | Savannah | CARS Dual-Mode Analog / Fusion |
| 196 | K4DBN-1 | 147.1500 | 123.0 | Dublin | **Peach State Intertie / SKYWARN Linked** |
| 197 | WA4HZX | 147.3600 | 123.0 | Dublin | Dublin Amateur Radio Club |
| 198 | K4GSO | 146.8800 | 100.0 | Dublin | Laurens County ARES Net |
| 199 | KD4IEZ | 443.0250 | 156.7 | Dublin | Laurens County UHF Repeater |
| 200 | CALL-2M | 146.5200 | CSQ | Nationwide | **National 2m FM Simplex Calling** |
| 201 | CALL-70 | 446.0000 | CSQ | Nationwide | **National 70cm FM Simplex Calling** |
| 202 | 2MSIMP1 | 146.5500 | CSQ | Simplex | 2m Secondary Chat Channel |
| 203 | 2MSIMP2 | 146.5800 | CSQ | Simplex | 2m Secondary Chat Channel |
| 204 | 2MSIMP3 | 147.5250 | CSQ | Simplex | 2m Upper Simplex |
| 205 | 2MSIMP4 | 147.5550 | CSQ | Simplex | 2m Upper Simplex |
| 206 | 70SIMP1 | 446.1000 | CSQ | Simplex | 70cm Secondary Simplex |
| 207 | 70SIMP2 | 446.5000 | CSQ | Simplex | 70cm Secondary Simplex |
| 208 | TYBEE-L | 146.4450 | 91.5 | Tybee Island | Tybee Island Crossband Link to 442.700 |
| 209 | HAGANS | 147.3900 | 131.8 | Hagan / Evans | Evans County Rural Repeater |
| 210 | W4NAS | 146.8350 | 127.3 | Glennville | Tattnall County ARES Repeater |

---

## 🌐 BANK 8 (CH 211–240): Regional Linked Systems & Atlanta Metro
*Modulation: FM (144.000 – 450.000 MHz)*

| CH | Tag / Name | Frequency (MHz) | Tone | Location | System / Network Highlights |
|---:|:-----------|:---------------:|:----:|:---------|:----------------------------|
| 211 | KC4YNB | 145.2100 | 103.5 | Eastman | **Peach State Intertie (PSI) SE GA Mega-Hub** |
| 212 | K4DBN-2 | 145.4900 | 77.0 | Cochran | Southeastern Linked Repeater Net / SKYWARN |
| 213 | WR4MG-1 | 146.8950 | 107.2 | Hawkinsville | Middle Georgia Radio Association (MGRA) |
| 214 | WR4MG-2 | 146.9550 | 107.2 | Perry | MGRA Perry Hospital / EchoLink WR4MG-L |
| 215 | WR4MG-3 | 147.1950 | 107.2 | Perry West | MGRA Taylor/Peach County Wide Footprint |
| 216 | WM4B-1 | 146.6700 | 82.5 | Warner Robins | Houston County ARES / Linked to PSI |
| 217 | WM4B-2 | 443.1500 | 82.5 | Warner Robins | Houston County ARES UHF Partner |
| 218 | WX4PCH | 145.2900 | 82.5 | Byron | **Peach State Intertie Key Backbone Link** |
| 219 | WR4MG-4 | 147.3000 | 107.2 | Centerville | MGRA Club Net & Talk-in |
| 220 | KD4UTQ | 146.8950 | 88.5 | Macon | **Peach State Intertie Primary Hub / SKYWARN** |
| 221 | AA4RI | 145.4300 | 88.5 | Macon | Macon ARC "Cherry Blossom Intertie" |
| 222 | WX4EMA | 147.0150 | 88.5 | Macon | Macon-Bibb EMA / ARES Linked |
| 223 | KK4JPG | 146.8350 | 77.0 | Forsyth | Monroe County ARS / PSI Linked |
| 224 | WX4BCA | 147.2850 | 131.8 | Jackson | Butts County ARES / Sylvan Grove Hospital |
| 225 | WB4GWA | 145.3900 | 110.9 | Griffin | Spalding County ARES Primary |
| 226 | KI4FVI | 146.7150 | 146.2 | McDonough | **Henry Link System Hub (AllStar #41014)** |
| 227 | KJ4KPY | 145.1700 | 146.2 | Stockbridge | Piedmont Henry Hospital / Henry ARS |
| 228 | W9KLS | 442.1250 | 103.5 | McDonough | Henry Linked UHF Partner |
| 229 | KE4UAS | 444.8750 | 100.0 | McDonough | Henry County Fire Dept AllStar Link |
| 230 | KK4GQ | 145.2100 | 131.8 | Fayetteville | Fayette County ARC / EchoLink |
| 231 | WX4PTC1 | 444.6750 | 77.0 | Peachtree City | **NWS Peachtree City HQ (SKYWARN State Hub)** |
| 232 | WX4PTC2 | 444.6000 | 77.0 | Fayetteville | NWS Peachtree City SKYWARN Secondary |
| 233 | W4DOC-1 | 146.8200 | 146.2 | Downtown Atlanta | **Atlanta Radio Club (Bank of America Plaza, 1000+ ft)** |
| 234 | W4BOC-1 | 146.7600 | 107.2 | Stone Mountain | **Alford Memorial ARC ("The '76" - Mega Metro Footprint)** |
| 235 | NF4GA-1 | 145.4700 | 100.0 | Sweat Mountain | North Fulton AR League (North Metro Umbrella) |
| 236 | W4BTI | 146.8800 | 100.0 | Sweat Mountain | Kennehoochee ARC / Cobb County ARES |
| 237 | W4GR-1 | 147.0750 | 82.5 | Snellville | Gwinnett ARS / Gwinnett ARES Hub |
| 238 | W4AQL | 145.1500 | 167.9 | Midtown Atlanta | Georgia Tech Amateur Radio Club |
| 239 | W4BOC-2 | 145.4500 | 107.2 | Stone Mountain | Alford Memorial ARC Secondary VHF |
| 240 | W4DOC-2 | 443.1000 | 100.0 | Downtown Atlanta | Atlanta Radio Club UHF |

---

## 🛒 BANK 9 (CH 241–270): GMRS, FRS, MURS & Retail Walkies
*Modulation: FM / NFM (151.000 – 468.000 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Service Class | Description & Real-World User Base |
|---:|:-----------|:---------------:|:----:|:--------------|:-----------------------------------|
| 241 | GMRS 1 | 462.5625 | NFM | GMRS/FRS 1 | General family & neighborhood handhelds |
| 242 | GMRS 2 | 462.5875 | NFM | GMRS/FRS 2 | General family & neighborhood handhelds |
| 243 | GMRS 3 | 462.6125 | NFM | GMRS/FRS 3 | General family & neighborhood handhelds |
| 244 | GMRS 4 | 462.6375 | NFM | GMRS/FRS 4 | General family & neighborhood handhelds |
| 245 | GMRS 5 | 462.6625 | NFM | GMRS/FRS 5 | General family & neighborhood handhelds |
| 246 | GMRS 6 | 462.6875 | NFM | GMRS/FRS 6 | General family & neighborhood handhelds |
| 247 | GMRS 7 | 462.7125 | NFM | GMRS/FRS 7 | General family & neighborhood handhelds |
| 248 | GMRS 15 | 462.5500 | FM | GMRS Main 15 | High-power GMRS mobile/base direct |
| 249 | GMRS 16 | 462.5750 | FM | GMRS Main 16 | High-power GMRS mobile/base direct |
| 250 | GMRS 17 | 462.6000 | FM | GMRS Main 17 | High-power GMRS mobile/base direct |
| 251 | GMRS 18 | 462.6250 | FM | GMRS Main 18 | High-power GMRS mobile/base direct |
| 252 | GMRS 19 | 462.6500 | FM | GMRS Main 19 | High-power GMRS mobile/base direct |
| 253 | GMRS 20 | 462.6750 | FM | **GMRS Main 20** | **National GMRS Emergency & Traveler Calling** |
| 254 | GMRS 21 | 462.7000 | FM | GMRS Main 21 | High-power GMRS mobile/base direct |
| 255 | GMRS 22 | 462.7250 | FM | GMRS Main 22 | High-power GMRS mobile/base direct |
| 256 | GM20-RPT | 462.6750 | FM | GMRS 20 Repeater | Standard open travel repeater output |
| 257 | MURS 1 | 151.8200 | NFM | MURS Ch 1 | VHF License-Free (Hunting / Farms) |
| 258 | MURS 2 | 151.8800 | NFM | MURS Ch 2 | VHF License-Free (Drive-thrus / Security) |
| 259 | MURS 3 | 151.9400 | NFM | MURS Ch 3 | VHF License-Free (Job site communications) |
| 260 | MURS 4 | 154.5700 | FM | **MURS 4 ("Blue Dot")** | **Walmart & Home Depot Employee Walkies** |
| 261 | MURS 5 | 154.6000 | FM | **MURS 5 ("Green Dot")**| **Retail Store Operations & Inventory** |
| 262 | RED-DOT | 151.6250 | NFM | Business "Red Dot" | Home Depot / Lowe's / Construction Crews |
| 263 | PURP-DT | 151.9550 | NFM | Business "Purple Dot" | Industrial Plant / Warehouse Walkies |
| 264 | BLU-STR | 467.8500 | NFM | Business "Blue Star" | Lowe's / Target / Lumber Yard Handhelds |
| 265 | YEL-STR | 467.8750 | NFM | Business "Yellow Star"| Supermarket & Department Store Walkies |
| 266 | RED-STR | 467.9000 | NFM | Business "Red Star" | Hardware & Home Improvement Centers |
| 267 | BRN-STR | 467.9250 | NFM | Business "Brown Star" | Commercial Security & Facilities Maintenance |
| 268 | FRS 08 | 467.5625 | NFM | FRS Ch 8 | FRS Handheld Walkie-Talkie |
| 269 | FRS 11 | 467.6375 | NFM | FRS Ch 11 | FRS Handheld Walkie-Talkie |
| 270 | FRS 14 | 467.7125 | NFM | FRS Ch 14 | FRS Handheld Walkie-Talkie |

---

## 🌧️ BANK 10 (CH 271–300): NOAA Weather & Space Station
*Modulation: FM (145.000 – 162.550 MHz)*

| CH | Tag / Name | Frequency (MHz) | Mode | Station / Transmitter | Description & Coverage Area |
|---:|:-----------|:---------------:|:----:|:----------------------|:----------------------------|
| 271 | WX 1 | 162.5500 | FM | WXN22 (Dublin, GA) | **Primary NOAA Transmitter for Laurens/Treutlen** |
| 272 | WX 2 | 162.4000 | FM | KHB40 (Savannah, GA) | **Primary NOAA Transmitter for Coastal/Chatham** |
| 273 | WX 3 | 162.4750 | FM | WXJ76 (Statesboro, GA) | **Primary NOAA Transmitter for Bulloch/Evans** |
| 274 | WX 4 | 162.4250 | FM | WXJ36 (Baxley/Vidalia) | **Primary NOAA Strongest Signal in Mount Vernon** |
| 275 | WX 5 | 162.4500 | FM | KEC84 (Augusta, GA) | NOAA East Central Georgia Weather |
| 276 | WX 6 | 162.5000 | FM | WXK90 (Macon, GA) | NOAA Middle Georgia Weather |
| 277 | WX 7 | 162.5250 | FM | WXJ33 (Waycross, GA) | NOAA South Central Georgia Weather |
| 278 | ISS-VC | 145.8000 | FM | **International Space Station** | **Astronaut Crew Voice Downlink (FM Voice)** |
| 279 | ISS-PKT | 145.8250 | FM | International Space Station | ISS APRS Packet Telemetry (1200 baud) |
| 280 | SO-50 | 436.7950 | FM | SaudiSat-1C (SO-50) | Amateur FM Voice Satellite Downlink |
| 281 | AO-91 | 145.9600 | FM | RadFxSat (AO-91) | Amateur FM Voice Satellite Downlink |
| 282 | PO-101 | 145.9000 | FM | Diwata-2 (PO-101) | Amateur FM Voice Satellite Downlink |
| 283 | APRS-NAT | 144.3900 | FM | North America APRS | National Automatic Packet Reporting Digipeater |
| 284 | WX-ALRT1 | 162.4000 | FM | Emergency Tone Alert | Severe Thunderstorm / Tornado Warning Standby |
| 285 | WX-ALRT2 | 162.4250 | FM | Emergency Tone Alert | Severe Weather Warning Standby (Mount Vernon) |
| 286 | WX-ALRT3 | 162.4750 | FM | Emergency Tone Alert | Severe Weather Warning Standby (Statesboro) |
| 287 | WX-ALRT4 | 162.5500 | FM | Emergency Tone Alert | Severe Weather Warning Standby (Dublin) |
| 288 | WX-SWAT | 162.5000 | FM | Severe Weather Net | Middle GA Emergency Warning Relay |
| 289 | SPACE-1 | 145.8000 | FM | Orbital Pass Monitor | Overhead Satellite Voice Relay |
| 290 | SPACE-2 | 145.8250 | FM | Orbital APRS Monitor | Overhead Satellite Position Relay |
| 291 | RES-01 | 146.5200 | FM | Spare Simplex | Reserve Channel |
| 292 | RES-02 | 146.5500 | FM | Spare Simplex | Reserve Channel |
| 293 | RES-03 | 146.5800 | FM | Spare Simplex | Reserve Channel |
| 294 | RES-04 | 446.0000 | FM | Spare Simplex | Reserve Channel |
| 295 | RES-05 | 446.1000 | FM | Spare Simplex | Reserve Channel |
| 296 | RES-06 | 151.8200 | NFM | Spare MURS | Reserve Channel |
| 297 | RES-07 | 154.5700 | FM | Spare Business | Reserve Channel |
| 298 | RES-08 | 462.5625 | NFM | Spare GMRS | Reserve Channel |
| 299 | RES-09 | 462.6750 | FM | Spare GMRS Travel | Reserve Channel |
| 300 | RES-10 | 27.1850 | AM | Spare CB 19 | Reserve Channel |
