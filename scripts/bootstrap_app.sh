#!/usr/bin/env bash
set -e
END_POINT="api-a:${APP_BIND_PORT}"
/root/wait-for-it.sh ${END_POINT} && curl ${END_POINT}/bootstrap_db && curl -L ${END_POINT}/update_cache