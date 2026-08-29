#!/usr/bin/env bash
set -euo pipefail

# Recover a sane macOS command path even if the user's shell PATH is broken.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin:${PATH:-}"

LABEL="com.hermes.kanban"
PORT="${PORT:-8088}"
WORKSPACE="${HERMES_KANBAN_WORKSPACE:-$HOME/Projects/TEAM-MMM01/mmm-education-storefront}"
SERVER_REL="tools/kanban/server.py"
SERVER="$WORKSPACE/$SERVER_REL"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/HermesOS"
STDOUT_LOG="$LOG_DIR/kanban.out.log"
STDERR_LOG="$LOG_DIR/kanban.err.log"
UID_NUM="$(/usr/bin/id -u)"
DOMAIN="gui/$UID_NUM"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

[[ -x /bin/launchctl ]] || fail "launchctl is unavailable; this installer is for macOS."
[[ -d "$WORKSPACE" ]] || fail "Workspace not found: $WORKSPACE. Set HERMES_KANBAN_WORKSPACE to the correct clone."
[[ -f "$SERVER" ]] || fail "Kanban server not found: $SERVER. Do not install until tools/kanban/server.py exists at the selected workspace."

PYTHON="${HERMES_PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
    if [[ -x "$candidate" ]]; then
      PYTHON="$candidate"
      break
    fi
  done
  if [[ -z "$PYTHON" ]]; then
    candidate="$(command -v python3 2>/dev/null || true)"
    [[ -n "$candidate" && -x "$candidate" ]] && PYTHON="$candidate"
  fi
fi
[[ -n "$PYTHON" && -x "$PYTHON" ]] || fail "python3 not found. Set HERMES_PYTHON to an executable Python 3 path."

/bin/mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

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

/usr/bin/plutil -lint "$PLIST" >/dev/null

# Remove the previous registration if present. Ignore 'not found'.
/bin/launchctl bootout "$DOMAIN" "$PLIST" >/dev/null 2>&1 || true

# Avoid a duplicate manually-started copy of the same server.
/usr/bin/pkill -f "$SERVER_REL" >/dev/null 2>&1 || true
/bin/sleep 1

/bin/launchctl bootstrap "$DOMAIN" "$PLIST"
/bin/launchctl enable "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
/bin/launchctl kickstart -k "$DOMAIN/$LABEL"

info "Installed $LABEL"
info "Workspace: $WORKSPACE"
info "Python:    $PYTHON"
info "Port:      $PORT"
info "Plist:     $PLIST"
info "Logs:      $STDOUT_LOG / $STDERR_LOG"
info ""
info "Run verification next:"
info "  /bin/bash ops/local/macos/kanban/verify.sh"
