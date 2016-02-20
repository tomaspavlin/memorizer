#!/bin/bash

cd `dirname $0`

exec 1>>day_routine.log 2>&1

echo "Starting day routine for day" $(date '+%d %b %Y, %a')


file=/tmp/memorizer_data_backup_`date +%Y-%m-%d_%H:%M:%S`.tar.gz
echo "Backing up data info file $file..."
tar -zcf $file data


file=/tmp/memorizer_scheduler_status_`date +%Y-%m-%d_%H:%M:%S`
echo "Printing scheduler status into $file..."
./scheduler.py status > $file


echo "Starting scheduler..."
./scheduler.py

echo "Starting uploader..."
./uploader.py

echo "==="
echo ""

