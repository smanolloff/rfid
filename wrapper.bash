#!/bin/bash -e

DIR=$(dirname $0)
PROGRAM=barcode_input.py
CONFIG=$DIR/config.ini

fail() {
  echo "ERROR: $1"
  exit 1
}

read_config() {
  DISK=$(awk -F "=" '/disk/ {print $2}' $CONFIG | sed 's/\r$//')
  MOUNTPOINT=$(awk -F "=" '/mountpoint/ {print $2}' $CONFIG | sed 's/\r$//')

  [ -n "$DISK" -a -n "$MOUNTPOINT" ] || return 1
  return 0
}

run_program() {
  python $DIR/$PROGRAM
}

remount_disk() {
  sudo umount $DISK $MOUNTPOINT 2>/dev/null || :
  sudo mount $DISK $MOUNTPOINT || :
}

while true; do
  echo -n 'RFID starting.'
  for i in $(seq 1 1); do sleep 1 && echo -n '.'; done

  if ! read_config; then
    echo "ERROR: Could not read config from $CONFIG"
    echo
    continue
  fi

  if ! remount_disk; then
    echo "ERROR: Could not mount $DISK to $MOUNTPOINT"
    echo 'CHECK USB DISK!'
    echo
    continue
  fi

  clear

  if ! run_program; then
    echo "Error: program terminated with $?"
    sleep 10
  fi
done
