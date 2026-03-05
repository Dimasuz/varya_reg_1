#!/bin/sh

echo "make sites copy"
python3 sites_fix.py
sleep 5
echo "strt program"
python3 main.py

exec "$@"
