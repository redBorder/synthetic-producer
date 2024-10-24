#!/usr/bin/env python3

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
'/root/vimesa/scripts/attacks/at9_discovery.py',
'/root/vimesa/scripts/attacks/at10_collection_screen.py',
'/root/vimesa/scripts/attacks/at11_exfiltration_dropbox.py',
'/root/vimesa/scripts/attacks/at12_cnc.py',
'/root/vimesa/scripts/attacks/at13_impact_ransom.py']

import os
import time
from datetime import datetime, timedelta
TEST_TIME=10
TIME_TO_NEXT_ATTACK=600
def check_and_kill_process(script, command):
    os.system(f'pkill -f "{command}"')
    time.sleep(5)
    check_process = os.popen(f'pgrep -f "{command}"').read()
    while check_process:
        os.system('figlet "WARNING: Process still running"')
        print(f"Warning: Process for {script} is still running")
        os.system(f'pkill -f "{command}"')
        time.sleep(5)
        check_process = os.popen(f'pgrep -f "{command}"').read()

while True:
    for script in SCRIPTS_PATH:
        print('Starting attack script')
        os.system(f'figlet "{os.path.basename(script)}"')   
        if os.path.exists(script):
            if script.endswith('.yml'):
                command = f'rb_synthetic_producer -r 1 -p 1 -c {script}'
                os.system(f'{command} &')
                time.sleep(10) # because synthetic needs more time to start
                check_and_kill_process(script, command)
            else:
                command = f'python3 {script}'
                os.system(command)
                time.sleep(5)
                check_and_kill_process(script, command)
        time.sleep(TEST_TIME)
        # time.sleep(TIME_TO_NEXT_ATTACK)
    
    next_run = datetime.now() + timedelta(hours=2)
    os.system(f'figlet "Repeating scenario at {next_run.strftime("%H:%M")} UTC"')
    time.sleep(7200) # Back in 2 hours
