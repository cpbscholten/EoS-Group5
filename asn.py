#%%
import pandas
from pathlib import Path
import socket
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN


if __name__ == "__main__":
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'csv.txt', header=8, nrows=1000, parse_dates=['dateadded'])
    ips_urls = data['url'].str.split('/').str[2].str.split(':').str[0]

    ips = [(socket.gethostbyname(x) if bool(re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", x)) else x) for x in ips_urls]
    asn = [IPASN(Net(x)).lookup()['asn'] for x in ips]


    print(asn)

# %%
