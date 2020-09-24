import requests
import json
import csv
import time
import re
first_line = True

ip_list_2 = []

with open('csv.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if first_line:
            first_line = False
            pass
        ip = row[2].split('/')[2].split(':')[0]
        ip_list_2.append(ip)

print(ip_list_2[876])

ip_list = ["134.201.250.155"]

private_key = "ac953b47418de2b1d37f9f353725d799"
countries = {}

for ip in ip_list_2:
    response = requests.get("http://api.ipstack.com/"+ip+"?access_key=" + private_key)
    response = json.loads(response.content.decode('utf-8'))

    country_name = response['country_name']
    print(ip +":" + country_name)

    if country_name in countries:
        countries[country_name] += 1
    else:
        countries[country_name] = 1

    print(countries)
    time.sleep(2)

print(countries)