#!/bin/bash -e

DIR=$(dirname $0)
PROGRAM=frontend.py
CONFIG=$DIR/config.ini

fail() {
  echo "ERROR: $1"
  exit 1
}

flush_stdin() {
  while read -t 1 -n 10000 _; do :; done
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
  sudo mount $DISK $MOUNTPOINT -t vfat -o auto,rw,user,umask=000
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

  flush_stdin
  clear

  if ! run_program; then
    echo "Error: abrupt program exit"
    sleep 5
  fi
done
