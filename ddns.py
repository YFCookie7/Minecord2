import time
import requests
import json

def ddns_service():
    global ip_addr
    ip_addr=''

    with open("config.json", "r") as json_file:
        data = json.load(json_file)
        sub_domain = data.get('Sub_Domain', '')
        domain = data.get('Domain', '')
        ddns_url = data.get('DDNS_URL', '')
        ddns_password = data.get('DDNS_PASSWORD', '')
    
    while(True):
        try:
            with requests.Session() as session:
                response = session.get('https://checkip.amazonaws.com/', timeout=5, verify=True)
                response.raise_for_status()
                new_ip_addr = response.text.strip()
                if(ip_addr!=new_ip_addr):
                    if (ip_addr!=''):
                        print(f"New Ip found {new_ip_addr}")
                    ip_addr=new_ip_addr
                    try:
                        with requests.Session() as session:
                            url = f"{ddns_url}?host={sub_domain}&domain={domain}&password={ddns_password}&ip={ip_addr}"
                            response = session.get(url, timeout=5, verify=True)
                            response.raise_for_status()
                            print(f"Dynamic DNS updated successfully. {url}")
                    except requests.exceptions.RequestException as e:
                        print("Failed to update dynamic DNS:", str(e))
                else:
                    print("No ip update needed")
                              
        except requests.exceptions.RequestException as e:
            print("Failed to retrieve the public IP address:", str(e))
            return None
        
        time.sleep(950)