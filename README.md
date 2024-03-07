# GVE DevNet Catalyst Center PnP Automatic Claim

This repository contains sample code that automates the process of onboarding devices using Plug and Play (PnP) in Cisco Catalyst Center. Thereby, the device is automatically claimed and assigned to a specific site based on its IP address. 

The scripts utilize the "Device waiting to be claimed" webhook option of Cisco Catalyst Center. 
As soon as the device contacts Catalyst Center, information such as its IP address and serial number is sent via the webhook to the sample application. If the type of device aligns with the script settings, the application maps the device IP address to a subnet provided in an external CSV file. If a successful mapping is possible, further parameters are read from the file and used to configure the device with an minimal onboarding template and assign it to a site during the claiming process. 

> Note: This repository is an adapted version of the [PnPAutoClaim](https://github.com/pamosima/PnPAutoClaim) repository.

The sample code was tested with Catalyst 9200/9300 and Catalyst Center version 2.3.7.4.


## Contacts
* Ramona Renner

## Solution Components
* Python
* DNA Center 
* DNA Center REST API's
* Environment set up for PnP process


## Prerequisites

### Webhooks

The app needs to be reachable on port 9002 from the public internet for Catalyst Center Webhooks to be received and processed. Any option is valid, like AWS Lambda, Heroku, GCP, etc. Ngrok is used here to expose the local app for simplicity.

#### Ngrok

The Flask app runs on http://localhost:9002 by default, so it requires a Ngrok forwarding address to port 9002 to receive the webhooks.

Follow these instructions to set up ngrok:

1. Create a free account or login to [Ngrok](https://ngrok.com/).
2. Retrieve your auth token by navigating to `Getting Started > Your Authtoken` on the menu on the left-hand side. Copy the token on this page.
3. Then install the client library, depending on your OS [here](https://ngrok.com/download).
4. Once you have ngrok installed, update the ngrok configuration file with your auth token by running the following command on the terminal/command prompt:   

    ```ngrok authtoken <yourtoken>```   

replacing <yourtoken> with the authtoken you copied in Step 2.   

5. Start the ngrok tunnel for port 9002 with the command:

    ```ngrok http https://localhost:9002```   

6. Note the link under `Forwarding` with the format `http://xxxxx.ngrok-free.app` for a later step.


### Cisco DNA Center 

#### Configure the Webhook Event and Notification

1. Choose **Platform > Developer Toolkit > Event Notifications > Notifications**

2. Click **+** to create a new notification

3. For  **Step 1 - Select Site and Events**, search for ```Device waiting to be claimed```, select the notification and click **Next**

4. In **Step 2 - Select Channels**, select **Rest** as a notification channels and click **Next**

5. In **Step 3 - REST Settings**, click **here** to create a new setting instance. 

6. On the **Destinations** page, click **Add** and provide the following information, and click **Save**
   * Name: Name of the Webhook destination, e.g. PnP Sample Script
   * (Optional) Description 
   * URL: public URL of the sample application, format: `<ngrok-url see last section>/claim`
   * Authentication, e.g. `No Auth`
   * Proxy, e.g. checked


7. Return to the **Step 3 - REST Settings** page, refresh the instance select, and select the created instance.

8. Click on **Next**

9. In **Step 4 - Name and Description**, provide a name and short description for your notification, and click on **Next**

10. On the Summary page, click on **Finish**

Done! Your new notification is complete.


#### Import the Onboarding Template

1. Choose **Design** > **CLI Templates** or alternative in older Catalyst Versions **Tools** > **Template Hub**

2. Click **Import** > **Import Template**

3. Select the project **Onboarding Configuration** and upload the template provided in the **work_files** folder of this repository. Click **Import**.


### Set up the Sample App

8. Make sure you have [Python 3.8.10](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

9. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html))   

10. Access the created virtual environment folder
    ```
    cd [add name of virtual environment here] 
    ```

11. Clone this GitHub repository into the local folder:  
    ```
    git clone [add GitHub link here]
    ```
    * For GitHub link: 
      In GitHub, click on the **Code** button in the upper part of the page > click the **copy icon**  

  * Or simply download the repository as zip file using the 'Download ZIP' button and extract it

12. Access the downloaded folder:  
    ```
    cd gve_devnet_catalyst_center_pnp_automatic_claim
    ```

13. Install all dependencies:
    ```
    pip3 install -r requirements.txt
    ```

14. Fill in your variables in the .env file. Feel free to leave the variable without note as is: 

  ```python
      DNAC_HOST=<Catalyst Center address, without https://>
      USERNAME=<Catalyst Center Username>
      PASSWORD=<Catalyst Center Password>
      DAY0_TEMPLATE=<Name of imported PnP Onboarding Template, see section: Import the Onboarding Template>
      AUTOCLAIM_DEVICE_PID=<PID of device, e.g. C9200L-24P-4X>
  ```

> Note: Mac OS hides the .env file in the finder by default. View the demo folder for example with your preferred IDE to make the file visible.

15. Fill in one row for each network, site and configuration values in the **work_files/mapping.csv** file. As soon as a device with a defined type contacts Catalyst Center its IP address is compared to each entry in the **mapping.csv** file. If the IP address is part of one of the listed networks, the device will be claimed using the provided information for the mapping network.

IP,CIDR,site,hostname   
<network address>,<subnet CIDR>,<Full path of site e.g. Global/<area name>/<building name>,<Hostname of the device>

## Usage

16. Start the flask application:   

```python3 flaskapp.py```

The sample script will react as soon as a new device of the defined type is waiting to be claimed.


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
