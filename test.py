# %%
from ipwhois import IPWhois
import dns.resolver

if __name__ == "__main__":
    dns_name = dns.resolver.query('dnspython.org', 'A').response.answer[0]
    test = IPWhois('27.5.16.43').lookup_whois()
    print(test)