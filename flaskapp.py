""" Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

from flask import Flask, request
from dnacentersdk import DNACenterAPI
import pandas as pd
import ipaddress
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

file = pd.read_csv("work_files/mapping.csv", sep=",")

@app.route('/claim', methods=['GET', 'POST'])
def dnac_alert_received():
    
    if request.method == 'POST':

        dnac_notification = request.get_json()
        print(f'-- Received webhook for device to be claimed:')
        print(json.dumps(dnac_notification, indent=2))

        ip = dnac_notification['details']['ipAddress']
        serialNo = dnac_notification['details']['deviceName']
        dnacIP = dnac_notification['dnacIP']

        api = DNACenterAPI(base_url="https://"+dnacIP+":443",
                           username=os.environ['USERNAME'],
                           password=os.environ['PASSWORD'],
                           version='2.3.3.0',
                           verify=False)

        device_info = api.device_onboarding_pnp.get_device_list(
            serial_number=serialNo)

        print("-- Device Info based on serial") 
        print(json.dumps(device_info, indent=2))

        deviceId = device_info[0]["id"]
        pid = device_info[0]["deviceInfo"]["pid"]

        if os.environ['AUTOCLAIM_DEVICE_PID'] == pid:

            print(f"Device has correct pid type: {os.environ['AUTOCLAIM_DEVICE_PID']}")

            for inx, row in file.iterrows():

                subnet = f"{row['IP']}/{row['CIDR']}"

                if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet):

                    print(f"The device IP {ip} is part of subnet: {subnet}")
                    
                    print(f"It will be assigned to site: {row['site']}")
                    siteId = api.sites.get_site(name=str(row["site"]))[
                        "response"][0]["id"]
                    print(f"Associated site id: {siteId}")
                    
                    print(f'Update name of device to {row["hostname"]}')
                    device_info = {'hostname': row["hostname"],
                                   'name': row["hostname"]}
                    api.device_onboarding_pnp.update_device(deviceId, deviceInfo=device_info)
                    
                    templateId = api.configuration_templates.get_templates_details(name=os.environ['DAY0_TEMPLATE'])["response"][0]["id"]
                    print(f"Prepare template ID and config parameters for template with ID: {templateId}")
                    configInfo = {'configId': templateId, 
                                  'configParameters': [{'key': 'hostname', 'value': row["hostname"]}]
                                  }
                    print(f"Template config parameters: {configInfo}")
                    
                    print(f"Claiming device to site. Result:")
                    response = api.device_onboarding_pnp.claim_a_device_to_a_site(configInfo=configInfo,
                                                                       deviceId=deviceId,
                                                                       siteId=siteId,
                                                                       type="Default")
                    print(response)
                    
                    break  

        return("Webhook Recieved")


if __name__ == '__main__':

    app.run(host="0.0.0.0", port="9002", ssl_context="adhoc")
