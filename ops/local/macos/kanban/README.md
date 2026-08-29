# HermesOS Kanban — macOS Local Runtime

This package makes the local Kanban LaunchAgent reproducible without storing one Mac's absolute paths or secrets in GitHub.

## Source-of-truth rule

GitHub stores the installer, verification logic, and operating documentation.

The generated file below remains local machine state and MUST NOT be treated as canonical source code:

`~/Library/LaunchAgents/com.hermes.kanban.plist`

Runtime truth must be established from current launchd/process/health evidence.

## Safety rule

Do not delete or replace a working local Kanban runtime solely because this package exists. Install/update intentionally, verify, preserve rollback, and record evidence.

## Expected Preparation Station location

Default workspace:

`$HOME/Projects/TEAM-MMM01/mmm-education-storefront`

If the clone lives elsewhere:

```bash
export HERMES_KANBAN_WORKSPACE="/absolute/path/to/mmm-education-storefront"
```

Optional overrides:

```bash
export HERMES_PYTHON="/absolute/path/to/python3"
export PORT="8088"
```

## Install / reconcile

From the `hermes-agent` checkout containing this package:

```bash
bash ops/local/macos/kanban/install.sh
bash ops/local/macos/kanban/verify.sh
```

The installer:

- requires `tools/kanban/server.py` to exist in the selected Preparation Station workspace;
- discovers an executable Python 3 path;
- generates `~/Library/LaunchAgents/com.hermes.kanban.plist`;
- validates the plist with `plutil`;
- removes an old registration safely;
- stops an obvious duplicate manual Kanban process;
- registers the service using modern `launchctl bootstrap`;
- enables/kickstarts it;
- stores logs under `~/Library/Logs/HermesOS/`.

## Verify

Normal non-destructive verification:

```bash
bash ops/local/macos/kanban/verify.sh
```

Checks:

- launchd registration;
- `/health` returns JSON with `status=healthy`;
- `/api/board` responds and reports task count;
- process PID where available.

Optional controlled restart test:

```bash
bash ops/local/macos/kanban/verify.sh --crash-test
```

This terminates the registered Kanban process and confirms launchd starts a new process that becomes healthy. Use only when interrupting the local Kanban service briefly is acceptable.

## Reboot/login verification

A script cannot prove login/reboot recovery without an actual login/reboot cycle.

After reboot/login, run:

```bash
cd /path/to/hermes-agent
bash ops/local/macos/kanban/verify.sh
```

Record the timestamp, hostname/node identifier, git commit of this package, launchd status, health result, and board task count in the HermesOS verification/event system. Do not store credentials, customer data, or raw sensitive board contents in that evidence.

## Logs

```bash
tail -n 100 "$HOME/Library/Logs/HermesOS/kanban.out.log"
tail -n 100 "$HOME/Library/Logs/HermesOS/kanban.err.log"
```

Log rotation is not yet implemented by this LaunchAgent package. Treat rotation/retention as a follow-up reliability task rather than allowing unbounded logs indefinitely.

## Manage manually

```bash
DOMAIN="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/com.hermes.kanban.plist"

launchctl print "$DOMAIN/com.hermes.kanban"
launchctl kickstart -k "$DOMAIN/com.hermes.kanban"
launchctl bootout "$DOMAIN" "$PLIST"
```

## Rollback

Before replacing a known-good local plist, preserve a local backup if it materially differs:

```bash
cp "$HOME/Library/LaunchAgents/com.hermes.kanban.plist" \
   "$HOME/Library/LaunchAgents/com.hermes.kanban.plist.backup" 2>/dev/null || true
```

To restore a backup:

```bash
DOMAIN="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/com.hermes.kanban.plist"
launchctl bootout "$DOMAIN" "$PLIST" 2>/dev/null || true
cp "$PLIST.backup" "$PLIST"
plutil -lint "$PLIST"
launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl kickstart -k "$DOMAIN/com.hermes.kanban"
```

## MASTER classification

Until current Mac evidence is collected:

- Installer/runbook in GitHub: `GITHUB_EXISTING / CANDIDATE`
- Generated LaunchAgent: `LOCAL_EXISTING`
- Historical successful health result: `HISTORICAL_CONTEXT`
- Current runtime health: `UNKNOWN` until verified
- Crash restart: `UNKNOWN` until verified
- Reboot/login persistence: `UNKNOWN` until verified
- Cross-node/failover readiness: `MISSING/PARTIAL` until implemented and tested

Future Hermes Supervisor work should prove parity/superiority before this LaunchAgent is deprecated.
