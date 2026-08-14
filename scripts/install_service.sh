#!/bin/bash
PLIST="$HOME/Library/LaunchAgents/com.user.internshipbot.plist"
LOGDIR="$PWD/logs"
mkdir -p "$LOGDIR"
cat << XML > "$PLIST"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.internshipbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PWD/venv/bin/python</string>
        <string>$PWD/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PWD</string>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOGDIR/bot.log</string>
    <key>StandardErrorPath</key>
    <string>$LOGDIR/error.log</string>
</dict>
</plist>
XML
launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"
echo "Service loaded with logging. Runs every 30 mins."
