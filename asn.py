import pandas
from pathlib import Path
import socket
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN


if __name__ == "__main__":
    # load csv files
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'csv.txt', header=8, nrows=100, parse_dates=['dateadded'])
    response_data = pandas.read_csv(base_path / 'asn_response_data.csv').set_index('ASN')
    # print(response_data)

    # convert urls to ip addresses
    ips_urls = data['url'].str.split('/').str[2].str.split(':').str[0].str.split('www.').str[0]
    ips = [(socket.gethostbyname(x) if not bool(re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", x)) else x) for x in ips_urls]

    # retrieve ASN number and location
    asn_data = [IPASN(Net(x)).lookup() if x != '0.0.0.0' else None for x in ips]
    asn = [x['asn'] if x else None for x in asn_data]
    data['asn'] = asn
    asn_loc = [x['asn_country_code'] if x else None for x in asn_data]
    data['asn_loc'] = asn_loc

    # add average response time
    data['avg_response_time'] = [response_data.loc['AS' + x, :]['Average Reaction Time'] if x else None for x in asn]

    print(data)

# %%
