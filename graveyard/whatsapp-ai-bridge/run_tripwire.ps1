# This script runs a low-latency loop checking for the tripwire file.
# When the WhatsApp monitor detects an authorized trigger, it writes to tripwire.txt.
# This watcher detects the file, deletes it, and breaks out, signaling the AI sandbox to wake up.

Write-Host "Arming Zero-Latency Tripwire..."
while ($true) {
    if (Test-Path tripwire.txt) {
        Remove-Item tripwire.txt
        Write-Host 'TRIPWIRE_TRIGGERED'
        break
    }
    Start-Sleep -Milliseconds 500
}
