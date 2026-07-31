param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Save", "Load", "List", "CreateAntigravityProfile")]
    [string]$Action,

    [string]$ProfileName
)

$VSCodeUserPath = "$env:APPDATA\Code\User"
$ProfilesDir = "$PSScriptRoot\profiles"

if (!(Test-Path $ProfilesDir)) {
    New-Item -ItemType Directory -Path $ProfilesDir | Out-Null
}

function Save-Profile {
    param([string]$Name)
    if (-not $Name) { Write-Error "ProfileName is required for Save action"; return }
    
    $TargetDir = Join-Path $ProfilesDir $Name
    if (!(Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir | Out-Null
    }

    # Save Settings
    if (Test-Path "$VSCodeUserPath\settings.json") {
        Copy-Item "$VSCodeUserPath\settings.json" "$TargetDir\settings.json" -Force
    }

    # Save Keybindings
    if (Test-Path "$VSCodeUserPath\keybindings.json") {
        Copy-Item "$VSCodeUserPath\keybindings.json" "$TargetDir\keybindings.json" -Force
    }

    # Save Extensions
    Write-Host "Saving extensions list..."
    $extensions = code --list-extensions
    $extensions | Out-File "$TargetDir\extensions.txt" -Encoding UTF8

    Write-Host "Profile '$Name' saved successfully."
}

function Load-Profile {
    param([string]$Name)
    if (-not $Name) { Write-Error "ProfileName is required for Load action"; return }
    
    $SourceDir = Join-Path $ProfilesDir $Name
    if (!(Test-Path $SourceDir)) {
        Write-Error "Profile '$Name' not found."
        return
    }

    # Load Settings
    if (Test-Path "$SourceDir\settings.json") {
        Copy-Item "$SourceDir\settings.json" "$VSCodeUserPath\settings.json" -Force
        Write-Host "Settings restored."
    }

    # Load Keybindings
    if (Test-Path "$SourceDir\keybindings.json") {
        Copy-Item "$SourceDir\keybindings.json" "$VSCodeUserPath\keybindings.json" -Force
        Write-Host "Keybindings restored."
    }

    # Load Extensions
    if (Test-Path "$SourceDir\extensions.txt") {
        Write-Host "Installing extensions... this may take a moment."
        $currentExts = code --list-extensions
        $profileExts = Get-Content "$SourceDir\extensions.txt"
        
        foreach ($ext in $profileExts) {
            if (![string]::IsNullOrWhiteSpace($ext) -and $currentExts -notcontains $ext) {
                Write-Host "Installing $ext..."
                # Use Start-Process with Wait to ensure synchronous processing without blocking stdout completely
                Start-Process -FilePath "code" -ArgumentList "--install-extension", "$ext", "--force" -Wait -NoNewWindow
            }
        }
        Write-Host "Extensions restored."
    }
    
    Write-Host "Profile '$Name' loaded successfully."
}

function List-Profiles {
    $profiles = Get-ChildItem -Directory $ProfilesDir
    if ($profiles.Count -eq 0) {
        Write-Host "No profiles found."
    } else {
        Write-Host "Available Profiles:"
        foreach ($p in $profiles) {
            Write-Host " - $($p.Name)"
        }
    }
}

function Create-AntigravityProfile {
    $Name = "Antigravity-Equivalent"
    $TargetDir = Join-Path $ProfilesDir $Name
    if (!(Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir | Out-Null
    }

    # Create Antigravity-like settings, enhanced for this environment
    $settings = @{
        "python.languageServer" = "Default"
        "workbench.colorTheme" = "Default Dark+"
        "workbench.iconTheme" = "material-icon-theme"
        "editor.formatOnSave" = $true
        "files.autoSave" = "afterDelay"
        "editor.wordWrap" = "on"
        "editor.minimap.enabled" = $false
        "terminal.integrated.defaultProfile.windows" = "PowerShell"
        "security.promptForLocalFileProtocolHandling" = $false
        "git.autofetch" = $true
    }
    $settings | ConvertTo-Json | Out-File "$TargetDir\settings.json" -Encoding UTF8

    # Create extensions list (based on public ones from the IDE)
    $exts = @(
        "ms-python.python",
        "ms-python.debugpy",
        "golang.go",
        "redhat.java",
        "shopify.ruby-lsp",
        "ms-azuretools.vscode-docker",
        "llvm-vs-code-extensions.vscode-clangd",
        "eamodio.gitlens",
        "PKief.material-icon-theme"
    )
    $exts | Out-File "$TargetDir\extensions.txt" -Encoding UTF8

    Write-Host "Antigravity Equivalent profile generated! You can load it with:"
    Write-Host ".\Manage-VSCodeEnv.ps1 -Action Load -ProfileName $Name"
}

switch ($Action) {
    "Save" { Save-Profile -Name $ProfileName }
    "Load" { Load-Profile -Name $ProfileName }
    "List" { List-Profiles }
    "CreateAntigravityProfile" { Create-AntigravityProfile }
}
