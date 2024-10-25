#!/bin/bash

# How to run this script:
# Run it: ./rb_start_mitre_wide_attack.sh
#
# To view the running screen session:
# - To watch and attach to screen: screen -r mitre_wide_attack
# - Detach from screen: Ctrl+A then D
while getopts "hs:" opt; do
  case $opt in
    h)
      echo "Usage: $0 [-s screen_name]"
      echo "Starts the mitre_wide_attack.py script in a screen session"
      exit 0
      ;;
    s)
      SCREEN_NAME="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

SCREEN_NAME=${SCREEN_NAME:-mitre_wide_attack}

echo "Restarting mitre_wide_attack.py"
screen -X -S ${SCREEN_NAME} quit 2>/dev/null || true
screen -dmS ${SCREEN_NAME} python3 mitre_wide_attack.py