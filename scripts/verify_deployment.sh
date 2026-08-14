#!/bin/sh
set -eu
curl -fsS http://localhost:8000/health
printf '\nDeployment smoke check passed.\n'
