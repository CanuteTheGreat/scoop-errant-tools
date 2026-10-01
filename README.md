# scoop-errant-tools

Scoop bucket for free command-line tools from [Errant Solutions](https://errant.solutions).

## Add this bucket

```
scoop bucket add errant-tools https://git.canutethegreat.com/CanuteTheGreat/scoop-errant-tools
```

## Tools

| App | Description |
|---|---|
| [sshd-hardening-auditor](bucket/sshd-hardening-auditor.json) | Audit sshd_config against CIS/NIST SSH hardening recommendations |
| [tls-cert-watchdog](bucket/tls-cert-watchdog.json) | Check TLS certificate expiry/chain health for one or more hosts |

## Install

```
scoop install errant-tools/sshd-hardening-auditor
scoop install errant-tools/tls-cert-watchdog
```

Both tools are pure-stdlib Python 3 scripts (no third-party dependencies). Requires Python 3 on PATH -- `scoop install python` or the official python.org installer with the `.py` file association enabled.

Source, issues, and the rest of our free tools: https://git.canutethegreat.com/CanuteTheGreat
