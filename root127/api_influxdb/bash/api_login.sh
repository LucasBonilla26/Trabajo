#!/bin/bash
LOGIN_REPLY="$(curl -s -X POST -H "Content-Type: application/json" -d '{"username": "'"$1"'", "password": "'"$2"'"}' 'https://unex.admin.quodus.ai/token/auth')"
AUTH_COOKIE="$(echo "$LOGIN_REPLY" | grep -Po '"access_token"\s*:\s*"\K[^"]+')"
echo $AUTH_COOKIE