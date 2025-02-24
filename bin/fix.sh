#!/bin/sh

mntroot rw
cd /mnt/base-us/extensions/fixcovers/bin
if [ $# -eq 0 ]
  then
    python3 fix_covers.py
  else  
    python3 show_covers.py
fi
