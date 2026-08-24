#!/usr/bin/env bash
set -euo pipefail

LABEL="com.hermes.kanban"
PORT="${PORT:-8088}"
WORKSPACE="${HERMES_KANBAN_WORKSPACE:-$HOME/Projects/TEAM-MMM01/mmm-education-storefront}"
SERVER_REL="tools/kanban/server.py"
SERVER="$WORKSPACE/$SERVER_REL"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/HermesOS"
STDOUT_LOG="$LOG_DIR/kanban.out.log"
STDERR_LOG="$LOG_DIR/kanban.err.log"
UID_NUM="$(id -u)"
DOMAIN="gui/$UID_NUM"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

command -v launchctl >/dev/null 2>&1 || fail "launchctl is unavailable; this installer is for macOS."
[[ -d "$WORKSPACE" ]] || fail "Workspace not found: $WORKSPACE. Set HERMES_KANBAN_WORKSPACE to the correct clone."
[[ -f "$SERVER" ]] || fail "Kanban server not found: $SERVER. Do not install until tools/kanban/server.py exists at the selected workspace."

PYTHON="${HERMES_PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 "$(command -v python3 2>/dev/null || true)"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
      PYTHON="$candidate"
      break
    fi
  done
fi
[[ -n "$PYTHON" && -x "$PYTHON" ]] || fail "python3 not found. Set HERMES_PYTHON to an executable Python 3 path."

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$SERVER</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$WORKSPACE</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
    <key>Crashed</key>
    <true/>
  </dict>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>ProcessType</key>
  <string>Background</string>
  <key>StandardOutPath</key>
  <string>$STDOUT_LOG</string>
  <key>StandardErrorPath</key>
  <string>$STDERR_LOG</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PORT</key>
    <string>$PORT</string>
    <key>PYTHONUNBUFFERED</key>
    <string>1</string>
  </dict>
</dict>
</plist>
PLIST

plutil -lint "$PLIST" >/dev/null

# Remove the previous registration if present. Ignore 'not found'.
launchctl bootout "$DOMAIN" "$PLIST" >/dev/null 2>&1 || true

# Avoid a duplicate manually-started copy of the same server.
pkill -f "$SERVER_REL" >/dev/null 2>&1 || true
sleep 1

launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl enable "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl kickstart -k "$DOMAIN/$LABEL"

info "Installed $LABEL"
info "Workspace: $WORKSPACE"
info "Python:    $PYTHON"
info "Port:      $PORT"
info "Plist:     $PLIST"
info "Logs:      $STDOUT_LOG / $STDERR_LOG"
info ""
info "Run verification next:"
info "  bash ops/local/macos/kanban/verify.sh"
