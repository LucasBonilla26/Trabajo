#!/bin/bash
curl -s -H 'Authorization: Bearer '"$1" -L 'https://unex.admin.quodus.ai/api/location-raw-latest'