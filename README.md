# scoop-errant-tools

Scoop bucket for free command-line tools from [Errant Solutions](https://errant.solutions).

## Add this bucket

```
scoop bucket add errant-tools https://git.canutethegreat.com/CanuteTheGreat/scoop-errant-tools
```

## Tools

| App | Description |
|---|---|
| [aws-waste-finder](bucket/aws-waste-finder.json) | Read-only AWS cost drain scanner (EBS/EIP/NAT/snapshots/idle LBs) |
| [cert-transparency-watcher](bucket/cert-transparency-watcher.json) | Monitor Certificate Transparency logs for unexpected issuers/subdomains, free via crt.sh |
| [cron-sanity-checker](bucket/cron-sanity-checker.json) | Catch impossible dates, typos and overlap in cron schedules, with next-run preview |
| [dns-hygiene-checker](bucket/dns-hygiene-checker.json) | Find dangling DNS records (subdomain takeover setups) before an attacker does, free via DoH |
| [docker-baseline-auditor](bucket/docker-baseline-auditor.json) | Read-only Docker security baseline checker (CIS-adjacent), free and zero-dependency |
| [http-header-auditor](bucket/http-header-auditor.json) | Audit a live site's HTTP security headers, cookie flags and HTTPS redirect |
| [json-schema-diff](bucket/json-schema-diff.json) | Classify JSON Schema changes as BREAKING, compatible, or info-only for API versioning |
| [mail-security-auditor](bucket/mail-security-auditor.json) | Audit a domain's SPF/DKIM/DMARC/MX email authentication hygiene, free and zero-dependency |
| [nginx-config-auditor](bucket/nginx-config-auditor.json) | Static analyzer for nginx config files flagging common misconfigurations, free and zero-dependency |
| [security-txt-auditor](bucket/security-txt-auditor.json) | Audit robots.txt and security.txt (RFC 9116) for common misconfigurations |
| [sshd-hardening-auditor](bucket/sshd-hardening-auditor.json) | Audit sshd_config against CIS/NIST SSH hardening recommendations |
| [tls-cert-watchdog](bucket/tls-cert-watchdog.json) | Check TLS certificate expiry/chain health for one or more hosts |
| [webhook-sig-verifier](bucket/webhook-sig-verifier.json) | Verify webhook HMAC signatures locally (GitHub/Stripe/Slack/generic), free and zero-dependency |

## Install

```
scoop install errant-tools/sshd-hardening-auditor
scoop install errant-tools/tls-cert-watchdog
```

All tools are pure-stdlib Python 3 scripts except aws-waste-finder, which also needs
`python -m pip install --user boto3`. Requires Python 3 on PATH -- `scoop install python` or the official python.org installer with the `.py` file association enabled.

Source, issues, and the rest of our free tools: https://git.canutethegreat.com/CanuteTheGreat

## Tests

`ci/test_manifests.py` (run by CI on every push and daily) downloads every manifest's
real archive, checks its hash, and runs each `bin` entry.
