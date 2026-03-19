#!/bin/sh

echo "make sites copy"
python3 sites_fix.py
sleep 10
echo "strt program"
python3 main.py

exec "$@"
