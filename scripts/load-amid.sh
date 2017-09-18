#!/bin/bash

USERNAME="${USERNAME:-test}"
PASSWORD="${PASSWORD:-test}"
BACKEND="${BACKEND:-xivo_service}"
SLEEPTIME="${SLEEPTIME:-1}"
RUNTIME="${RUNTIME:-$(echo "3600 * 8 / ${SLEEPTIME}" | bc)}"

if ! pidof asterisk > /dev/null; then
	echo 'Asterisk is not running'
	exit 0
fi

for ((n=0;n<${RUNTIME};n++)); do
	token=$(curl -k -i POST -H 'Content-Type: application/json' -u "${USERNAME}:${PASSWORD}" "https://localhost:9497/0.1/token" -d "{\"backend\": \"${BACKEND}\"}" 2>/dev/null | tail -n 1 | jq  -r ".data | .token")
	curl -k -i -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -H "X-Auth-Token: ${token}" 'https://localhost:9491/1.0/action/QueueSummary'
	sleep 1
done


