#!/bin/bash

echo "Starting day routine for day" $(date '+%d %b %Y, %a')
echo "Starting scheduler..."
./scheduler.py

echo "Starting uploader..."
./uploader.py
echo "==="
echo ""