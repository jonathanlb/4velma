#!/bin/sh
# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

# Script for udev-and-at to copy images from SD card upon card insertion.

LOG_FILE=/tmp/udev.txt
CARD_INPUT=/mnt/card/DCIM/101_PANA/
PIC_OUTPUT=/home/pi/Documents/4velma/pics 
MAX_TRIES=10
SLEEP_SECONDS=3

while [ "${MAX_TRIES}" -gt "0" ]
do
  echo "$(date) ${MAX_TRIES} checking ${CARD_INPUT}" >> ${LOG_FILE}
  if test -d ${CARD_INPUT}
  then
    find ${CARD_INPUT} -maxdepth 1 -type f -exec cp -n -v {} ${PIC_OUTPUT} \; 2>&1 >> ${LOG_FILE}
    exit $?
  else
    MAX_TRIES=$((MAX_TRIES-1))
    sleep ${SLEEP_SECONDS}
  fi
done
