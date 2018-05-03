#!/usr/bin/env bash
set -e

END_POINT="api-a:${APP_BIND_PORT}"
echo "requesting cache update"
/root/wait-for-it.sh ${END_POINT} && curl -L ${END_POINT}/update_cache