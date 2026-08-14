#!/bin/bash
PLIST="$HOME/Library/LaunchAgents/com.user.internshipbot.pdf.plist"
LOGDIR="$PWD/logs"
mkdir -p "$LOGDIR"
cat << XML > "$PLIST"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.internshipbot.pdf</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PWD/venv/bin/python</string>
        <string>$PWD/export_pdf.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PWD</string>
    <key>StartInterval</key>
    <integer>18000</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOGDIR/pdf.log</string>
    <key>StandardErrorPath</key>
    <string>$LOGDIR/pdf_error.log</string>
</dict>
</plist>
XML
launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"
echo "PDF export service loaded! Will check and export every 5 hours."
