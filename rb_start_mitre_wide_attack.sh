#!/bin/bash

# How to run this script:
# Run it: ./rb_start_mitre_wide_attack.sh
#
# To view the running screen session:
# - To watch and attach to screen: screen -r mitre_wide_attack
# - Detach from screen: Ctrl+A then D

echo 'Restarting mitre_wide_attack.py'
screen -X -S mitre_wide_attack quit 2>/dev/null || true
screen -dmS mitre_wide_attack python3 mitre_wide_attack.py