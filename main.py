import json
import csv
import requests
from requests.exceptions import HTTPError

def make_request(url, headers):
    try:
        response = requests.get(url, headers= headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise
    else:
        print('Request successfully made!')
        return response
    
def decode_reponse(response):
    decoded_response = json.loads(response.content)

    response_content = decoded_response['response']

    return response_content

def count_names(response_content):
    name_counter = dict()

    for contract in response_content:
        for policie in contract['policies']:
            for goods in policie['covered_goods']:
                name = goods.get('Nome')
                if name and name in name_counter:
                    name_counter[name] += 1
                elif name and name not in name_counter:
                    name_counter[name] = 1
                else:
                    continue
    
    return name_counter

def write_csv_file(name_counter):
    with open("name_counter.csv", "w", newline='') as csvFile:
        fieldNames = ['nome_pet', 'contador']

        csvWriter = csv.DictWriter(csvFile, fieldnames=fieldNames)

        csvWriter.writeheader()

        for name in name_counter:
            csvWriter.writerow({'nome_pet': name, 'contador': name_counter[name]})
 
url = 'https://api.suthubservice.com/v0/sales'
headers={'api_key': '', 'Content-Type': 'application/json'}

request_response = make_request(url, headers)

response_content = decode_reponse(request_response)

name_counter =  count_names(response_content)

write_csv_file(name_counter)
