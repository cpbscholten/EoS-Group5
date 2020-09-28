import pandas
from pathlib import Path
import socket
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN


def string_to_seconds_list(string_list):
    seconds_list = []
    for entry in string_list:
        months = re.findall(r'(\d+) months', entry)
        days = re.findall(r'(\d+) days', entry)
        hours = re.findall(r'(\d+) hours', entry)
        minutes = re.findall(r'(\d+) minutes', entry)

        seconds = 0
        seconds += int(minutes[0]) * 60 if minutes else 0
        seconds += int(hours[0]) * 3600 if hours else 0
        seconds += int(days[0]) * 86400 if days else 0
        seconds += int(months[0]) * 2628000 if months else 0
        seconds = -1 if seconds == 0 else seconds
        seconds_list.append(seconds)
    return seconds_list


def get_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return '0.0.0.0'


if __name__ == "__main__":
    # load csv files
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'csv.txt', header=8, parse_dates=['dateadded'])
    response_data = pandas.read_csv(base_path / 'asn_response_data.csv').set_index('ASN')
    domains_hosted_on_asn = pandas.read_csv(base_path / 'domains_hosted_per_asn.csv').set_index('ASN')
    # print(domains_hosted_on_asn)
    # print(response_data)

    # convert urls to ip addresses
    ips_urls = data['url'].str.split('/').str[2].str.split(':').str[0].str.split('www.').str[0]
    ips = [(get_ip(x) if not bool(re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", x)) else x) for x in ips_urls]

    # retrieve ASN number and location
    asn_data = [IPASN(Net(x)).lookup() if x != '0.0.0.0' else None for x in ips]
    asn = [x['asn'] if x else None for x in asn_data]

    data['asn'] = asn
    data['asn_loc'] = [x['asn_country_code'] if x else None for x in asn_data]

    # add asn maintainer name
    asn_name = [response_data.loc['AS' + x, :]['Name'] if x else None for x in asn]
    data['asn_name'] = asn_name

    # add average response time
    avg_response_string = [response_data.loc['AS' + x, :]['Average Reaction Time'] if x else None for x in asn]
    data['avg_response_time'] = avg_response_string
    # convert this to seconds for
    data['avg_response_time_seconds'] = string_to_seconds_list(avg_response_string)

    # add number of domains hosted on ASN
    data['domains_hosted'] = [domains_hosted_on_asn.loc['AS' + x, :]['domains'] if 'AS'+ x in domains_hosted_on_asn.index and x else -1 for x in asn]

    # Count instances of asn_name
    print(data.asn_name.value_counts())

    print(data)

    data.to_csv('dataset.csv', index=False)