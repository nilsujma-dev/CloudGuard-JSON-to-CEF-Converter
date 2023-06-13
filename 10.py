import json
import time
import sys
from datetime import datetime

# Make sure a filename is provided
if len(sys.argv) < 2:
    print('Usage: python3 script.py jsonfile.json')
    sys.exit()

# Load the JSON data
filename = sys.argv[1]

with open(filename, 'r') as f:
    data = json.load(f)

# Extract the keys from the JSON data
rule_name = data['rule']['name']
rule_description = data['rule']['description']
severity = data['rule']['severity']
source_username = data['entity']['name']
source_user_id = data['entity']['id']

# Convert reportTime to UNIX timestamp (milliseconds)
report_time = data['reportTime']
dt = datetime.strptime(report_time, "%Y-%m-%dT%H:%M:%S.%fZ")
unix_time_ms = int(time.mktime(dt.timetuple())) * 1000

status = data['status']
rule_remediation = data['rule']['remediation']
account = json.dumps(data['account'])

# Construct the CEF string
cef = f'CEF:0|CheckPoint|CloudGuard||{rule_name}|{rule_name}|{severity}|' \
      f'msg={rule_description} suser={source_username} suid={source_user_id} rt={unix_time_ms} ' \
      f'fname=CLOUD-011 CheckPoint CloudGuard Compliance Alert-24Hrs outcome={status} ' \
      f'cs1={rule_remediation} cs1Label=Rule Remediation flexString1={account} flexString1Label=Account'

# Print the CEF string
print(cef)
