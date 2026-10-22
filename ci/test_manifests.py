#!/usr/bin/env python3
"""CI test for every manifest in bucket/: what `scoop install` would do.

For each manifest it downloads the real `url`, checks `hash` (sha256), unpacks the
zip, checks `extract_dir` and every `bin` entry exist, and runs each bin with Python
and `--help` (exit 0, prints usage) and `--version` (must print the manifest's version). It also checks `version` matches the tag in the
URL, that `url`/`checkver`/`autoupdate` use the tool's public GitHub repo (the site never sends users to our
own git host) and that `extract_dir` is GitHub's `<repo>-<version>` archive folder.
"""
import glob
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFESTS = sorted(glob.glob(os.path.join(os.path.dirname(HERE), "bucket", "*.json")))


def download(url):
    last = None
    for _ in range(6):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read()
        except Exception as e:  # archive downloads can fail transiently
            last = e
            time.sleep(5)
    raise last


def check(path):
    m = json.load(open(path))
    for k in ("version", "description", "homepage", "license", "url", "hash", "bin", "checkver"):
        assert k in m, f"manifest has no {k!r}"
    assert f"/v{m['version']}." in m["url"], f"version {m['version']} doesn't match url {m['url']}"
    repo = m["url"].split("/CanuteTheGreat/", 1)[1].split("/", 1)[0]
    assert m["homepage"] == f"https://errant.solutions/tools/{repo}.html", m["homepage"]
    gh = f"https://github.com/CanuteTheGreat/{repo}"
    assert m["url"] == f"{gh}/archive/refs/tags/v{m['version']}.zip", m["url"]
    assert m["checkver"] == {"github": gh}, m["checkver"]
    assert m.get("extract_dir") == f"{repo}-{m['version']}", m.get("extract_dir")
    assert m.get("autoupdate") == {"url": f"{gh}/archive/refs/tags/v$version.zip", "extract_dir": f"{repo}-$version"}, \
        m.get("autoupdate")
    assert "canutethegreat.com" not in json.dumps(m).lower(), "manifest still points at our own git host"
    data = download(m["url"])
    got = hashlib.sha256(data).hexdigest()
    assert got == m["hash"].lower(), f"hash mismatch for {m['url']}: manifest {m['hash']}, actual {got}"
    with tempfile.TemporaryDirectory() as work:
        zipfile.ZipFile(io.BytesIO(data)).extractall(work)
        root = os.path.join(work, m.get("extract_dir", ""))
        assert os.path.isdir(root), f"extract_dir {m.get('extract_dir')!r} not in the archive"
        for entry in m["bin"]:
            src = entry[0] if isinstance(entry, list) else entry
            exe = os.path.join(root, src)
            assert os.path.isfile(exe), f"bin {src} not in the archive"
            p = subprocess.run([sys.executable, exe, "--help"], capture_output=True, text=True, timeout=60, cwd=work)
            if "boto3" in m.get("notes", ""):
                # its notes tell the user to pip install boto3; without it the tool must say so, not crash
                assert p.returncode == 2 and "requires boto3" in p.stderr and "Traceback" not in p.stderr, \
                    f"{src} without boto3 exited {p.returncode}: {p.stderr[-300:]}"
            else:
                assert p.returncode == 0 and "usage" in (p.stdout + p.stderr).lower(), \
                    f"{src} --help exited {p.returncode}: {p.stderr[-300:]}"
                v = subprocess.run([sys.executable, exe, "--version"], capture_output=True, text=True, timeout=60)
                assert v.returncode == 0 and v.stdout.strip().endswith(" " + m["version"]), \
                    f"{src} --version printed {v.stdout.strip()!r}, manifest says {m['version']}"
    return m["url"]


def main():
    assert MANIFESTS, "no manifests found"
    failures = 0
    for f in MANIFESTS:
        try:
            print(f"ok   {os.path.basename(f)}  ({check(f)})")
        except Exception as e:
            failures += 1
            print(f"FAIL {os.path.basename(f)}: {e}")
    print(f"MANIFEST TESTS: {len(MANIFESTS) - failures} passed, {failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
