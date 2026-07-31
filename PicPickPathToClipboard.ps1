param(
    [Parameter(Mandatory=$false)]
    [string]$FilePath
)

# Debug logging to see what PicPick is actually passing
$logPath = "C:\Users\whanusiewicz\Documents\utility-scripts\picpick_debug.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$timestamp - Received arg: '$FilePath'" | Out-File $logPath -Append

if (![string]::IsNullOrEmpty($FilePath)) {
    Set-Clipboard -Value $FilePath
    "Set clipboard to: $FilePath" | Out-File $logPath -Append
} else {
    "No file path provided." | Out-File $logPath -Append
}
