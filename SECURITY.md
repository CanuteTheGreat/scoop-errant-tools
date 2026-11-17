# Security policy

## Reporting a vulnerability

Please report suspected vulnerabilities in this repository or the tools it installs by email to security@errant.solutions (see also
https://errant.solutions/.well-known/security.txt). Include the version (tool and version), what you
ran, and what you expected to happen. Please do not open a public issue for a vulnerability.

You will get an acknowledgement within 3 working days, and a fix or a mitigation plan within 30 days
for anything that is a real vulnerability. We credit reporters who want to be credited.

## Supported versions

Only the latest release is supported. Fixes ship as a new release; there are no back-ports.

## What this repository contains

Scoop manifests only: each points at the release archive of one Errant Solutions tool and pins its SHA-256.
A bad pin or a hijacked archive is the main risk, so CI installs every entry the way a user does
on each push and daily, and the hash must match the published archive. The tools' own releases carry a
signed `SHA256SUMS.asc` (key fingerprint 5439 3549 39B9 C055 2A68  E9BB E323 A6A3 AC0A 6506, public key at
https://errant.solutions/signing-key.asc); see each tool's SECURITY.md for how to verify it.
