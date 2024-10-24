#!/usr/bin/env ruby

# This script is used to run different incidentes that are following a full path of Mitre tactics, by running the corresponding scripts.
# Each of the scripts is responsible for running the incident that triggers the corresponding tactic.
# On start, this script will create an instace in screen named "mitre_wide_attack" and will repeat itself every 2 hours.

# Array of scripts to execute in sequence
SCRIPTS_PATH = [
    # Add paths to your attack scripts here, one per line
'/root/vimesa/scripts/attacks/at1_reconocimiento_scan.py',
'/root/vimesa/scripts/attacks/at2_resource_development_ssl.py',
'/root/vimesa/scripts/attacks/at3.py',
'/etc/synthetic_producer/config/vault_new_powershell.yml',
'/root/vimesa/scripts/attacks/at5_persistence_backdoor.py',
'/root/vimesa/scripts/attacks/at6.py',
'/root/vimesa/scripts/attacks/at7_defense_evasion.py',
'/root/vimesa/scripts/attacks/at8_credential_access.py',
'/root/vimesa/scripts/attacks/at9_lateral_movement.py',
'/root/vimesa/scripts/attacks/at10_collection_screen.py',
'/root/vimesa/scripts/attacks/at11_exfiltration_dropbox.py',
'/root/vimesa/scripts/attacks/at12_cnc.py',
'/root/vimesa/scripts/attacks/at13_impact_ransom.py']

import os
import time

for script in SCRIPTS_PATH:
    if os.path.exists(script):
        if script.endswith('.yml'):
            os.system(f'rb_synthetic_producer -r 1 -p 1 -c {script} &')
            time.sleep(30)
            os.system(f'pkill -f "rb_synthetic_producer -r 1 -p 1 -c {script}"')
            time.sleep(5)
            # Check if process was killed
            check_process = os.popen(f'pgrep -f "rb_synthetic_producer -r 1 -p 1 -c {script}"').read()
            if check_process:
                print(f"Warning: Process for {script} is still running")
            
        else:
            # Wait 10' for each attack
            os.system(f'python3 {script}')     
        time.sleep(600)