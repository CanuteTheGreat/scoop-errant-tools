#!/bin/sh
# Runs the tap's install tests inside a throwaway, resource-capped python
# container with no extra packages (no boto3, no docker CLI) -- the same bare
# environment a fresh `scoop install` user has. Removed on exit.
set -eu
NAME="ci-$(basename "$(pwd)")-${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-0}-$$"
cleanup() { docker rm -f -v "$NAME" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM
docker run -d --name "$NAME" --memory 512m --cpus 1 --pids-limit 256 python:3.12-bookworm sleep 1800 >/dev/null
docker cp . "$NAME:/src"
docker exec -w /src "$NAME" python ci/test_manifests.py
