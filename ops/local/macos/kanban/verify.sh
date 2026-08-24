#!/usr/bin/env bash
set -euo pipefail

# Recover a sane macOS command path even if the user's shell PATH is broken.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin:${PATH:-}"

LABEL="com.hermes.kanban"
PORT="${PORT:-8088}"
UID_NUM="$(/usr/bin/id -u)"
DOMAIN="gui/$UID_NUM"
BASE_URL="http://127.0.0.1:$PORT"
CRASH_TEST="${1:-}"

pass() { printf 'PASS: %s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

[[ -x /bin/launchctl ]] || fail "launchctl unavailable; this verification is for macOS."
[[ -x /usr/bin/curl ]] || fail "curl unavailable."

PYTHON="${HERMES_PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
    if [[ -x "$candidate" ]]; then PYTHON="$candidate"; break; fi
  done
fi
[[ -n "$PYTHON" && -x "$PYTHON" ]] || fail "python3 unavailable. Set HERMES_PYTHON to an executable Python 3 path."

if /bin/launchctl print "$DOMAIN/$LABEL" >/tmp/hermes-kanban-launchctl.txt 2>&1; then
  pass "LaunchAgent is registered: $DOMAIN/$LABEL"
else
  /bin/cat /tmp/hermes-kanban-launchctl.txt >&2 || true
  fail "LaunchAgent is not registered."
fi

health="$(/usr/bin/curl --fail --silent --show-error --max-time 5 "$BASE_URL/health" || true)"
[[ -n "$health" ]] || fail "Health endpoint did not respond: $BASE_URL/health"
printf '%s' "$health" | "$PYTHON" -c 'import json,sys; d=json.load(sys.stdin); assert d.get("status") == "healthy", d' \
  && pass "Health endpoint reports healthy" \
  || fail "Health endpoint returned unexpected JSON/status"

board="$(/usr/bin/curl --fail --silent --show-error --max-time 5 "$BASE_URL/api/board" || true)"
[[ -n "$board" ]] || fail "Board endpoint did not respond: $BASE_URL/api/board"
task_count="$(printf '%s' "$board" | "$PYTHON" -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("tasks", [])))')"
pass "Board endpoint responded; tasks=$task_count"

pid="$(/bin/launchctl print "$DOMAIN/$LABEL" 2>/dev/null | /usr/bin/awk '/pid =/ {print $3; exit}')"
if [[ -n "${pid:-}" && "$pid" =~ ^[0-9]+$ ]]; then
  pass "LaunchAgent process is running; pid=$pid"
else
  warn "Could not extract a running PID from launchctl output."
fi

if [[ "$CRASH_TEST" == "--crash-test" ]]; then
  [[ -n "${pid:-}" && "$pid" =~ ^[0-9]+$ ]] || fail "Cannot run crash test without a PID."
  before="$pid"
  printf 'Crash test requested: terminating pid %s and waiting for launchd recovery...\n' "$before"
  /bin/kill -TERM "$before"

  recovered=""
  for _ in {1..20}; do
    /bin/sleep 1
    recovered="$(/bin/launchctl print "$DOMAIN/$LABEL" 2>/dev/null | /usr/bin/awk '/pid =/ {print $3; exit}')"
    if [[ -n "$recovered" && "$recovered" =~ ^[0-9]+$ && "$recovered" != "$before" ]]; then
      if /usr/bin/curl --fail --silent --max-time 3 "$BASE_URL/health" >/dev/null 2>&1; then
        pass "Crash recovery succeeded; old pid=$before new pid=$recovered"
        break
      fi
    fi
  done
  [[ -n "$recovered" && "$recovered" != "$before" ]] || fail "LaunchAgent did not recover within the verification window."
fi

printf '\nRuntime verification complete.\n'
printf 'For reboot/login verification, reboot/login is still required on the Mac; after login rerun this script and record the evidence.\n'
