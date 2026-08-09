param (
    [Parameter(Mandatory=$true)]
    [string]$ImagePath
)

if (-not (Test-Path -Path $ImagePath)) {
    Write-Error "Error: File not found at path '$ImagePath'"
    exit 1
}

try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $img = [System.Drawing.Image]::FromFile($ImagePath)
    [System.Windows.Forms.Clipboard]::SetImage($img)
    $img.Dispose()
    Write-Host "Success! Image copied to clipboard."
}
catch {
    Write-Error "Failed to copy image to clipboard: $_"
    exit 1
}
