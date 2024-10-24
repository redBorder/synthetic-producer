#!/bin/bash

echo 'Restarting mitre_wide_attack.py'
screen -X -S mitre_wide_attack quit 2>/dev/null || true
screen -dmS mitre_wide_attack python3 mitre_wide_attack.py