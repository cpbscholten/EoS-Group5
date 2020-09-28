from typing import Union, Any

import pandas
from pathlib import Path
import socket
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN
import time


base_path = Path().absolute()
ip_to_asn = {}
domain_to_ip_table = pandas.read_csv(base_path / 'domain_to_ip.csv').set_index('domain')


def string_to_seconds_list(string_list):
    seconds_list = []
    for entry in string_list:
        if entry:
            months = re.findall(r'(\d+) months', entry)
            days = re.findall(r'(\d+) days', entry)
            hours = re.findall(r'(\d+) hours', entry)
            minutes = re.findall(r'(\d+) minutes', entry)

            seconds = 0
            seconds += int(minutes[0]) * 60 if minutes else 0
            seconds += int(hours[0]) * 3600 if hours else 0
            seconds += int(days[0]) * 86400 if days else 0
            seconds += int(months[0]) * 2628000 if months else 0
            seconds_list.append(seconds)
        else:
            seconds_list.append(-1)
    return seconds_list


def get_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return '0.0.0.0'


def ip_to_asn_lookup(ip: str) -> Union[dict, Any]:
    if ip in ip_to_asn:
        return ip_to_asn[ip]
    else:
        asn_info = IPASN(Net(ip)).lookup()
        ip_to_asn[ip] = asn_info
        return asn_info


def domain_to_ip(domain):
    if domain and domain in domain_to_ip_table:
        return domain_to_ip_table.loc[domain, :]['ip']
    else:
        return None


if __name__ == "__main__":
    response_data = pandas.read_csv(base_path / 'asn_response_data.csv').set_index('ASN')
    domains_hosted_on_asn = pandas.read_csv(base_path / 'domains_hosted_per_asn.csv').set_index('ASN')

    # data['dateadded'] >= '2020-01-01')] = 270578 rows

    while j <= 270578:
        start_time = time.time()
        data = pandas.read_csv(base_path / 'csv.txt', names=['id','dateadded','url','url_status','threat','tags','urlhaus_link','reporter'], nrows=1000, skiprows=j, parse_dates=['dateadded'])
        response_data = pandas.read_csv(base_path / 'asn_response_data.csv').set_index('ASN')
        domains_hosted_on_asn = pandas.read_csv(base_path / 'domains_hosted_per_asn.csv').set_index('ASN')
        # print(domains_hosted_on_asn)
        # print(response_data)

        # convert urls to ip addresses
        ips_urls = data['url'].str.split('/').str[2].str.split(':').str[0].str.split('www.').str[0]
        ips = [(domain_to_ip(x) if not bool(re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", x)) else x) for x in ips_urls]

        # retrieve ASN number and location
        asn_data = [ip_to_asn_lookup(x) if x and x != '0.0.0.0' else None for x in ips]
        # do a split, since there might be a possibility that multiple ASNs are returned.
        asn = [x['asn'].split(" ")[0] if x else None for x in asn_data]
        # print(asn.index("7296"))

        data['asn'] = asn
        data['asn_loc'] = [x['asn_country_code'] if x else None for x in asn_data]

        # add asn maintainer name
        asn_name = [response_data.loc['AS' + x, :]['Name'] if x and 'AS' + x in response_data.index else None for x in asn]
        data['asn_name'] = asn_name

        # add average response time
        avg_response_string = [response_data.loc['AS' + x, :]['Average Reaction Time'] if x and 'AS' + x in response_data.index else None for x in asn]
        data['avg_response_time'] = avg_response_string
        # convert this to seconds for
        data['avg_response_time_seconds'] = string_to_seconds_list(avg_response_string)

        # add number of domains hosted on ASN
        data['domains_hosted'] = [domains_hosted_on_asn.loc['AS' + x, :]['domains'] if x and 'AS' + x in domains_hosted_on_asn.index else -1 for x in asn]

        data.to_csv(f'results/dataset{j}.csv', index=False)
        j += 1000
        end_time = time.time()
        print(f'Were now at: {j}, it took - {end_time - start_time}')