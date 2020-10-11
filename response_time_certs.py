#%% 
import pandas
import statsmodels.api as sm
from pathlib import Path
import re
import numpy as np
base_path = Path().absolute()

dataset = pandas.read_csv('data/asn_response_data.csv')
certs = pandas.read_json('data/irt-teams.json')


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
            seconds_list.append(None)
    return seconds_list

dataset['Country'] = dataset['Country'].str[2:]
dataset['response_time_seconds'] = string_to_seconds_list(dataset['Average Reaction Time'])

#%%
response_time_per_country = dataset.groupby(['Country']).agg({"response_time_seconds" : np.mean}) 
# %%
no_of_certs = certs.groupby(['country-code']).size().to_frame('cert_count')
both = pandas.merge(no_of_certs, response_time_per_country, how='right', left_index=True, right_index=True)
# correlation:
both.corr()

#%%
# If there are no certs in that country, set it to 0, instead of NaN
both = both.fillna(0)
kaspersky = pandas.read_csv('Data/kaspersky.csv').set_index('country')

merged_data = kaspersky.merge(both, left_index=True, right_index=True)


#%%
y = merged_data['response_time_seconds']

cols = ["% of Mobiles Infected with Malware",
        "Financial Malware Attacks (% of Users)",
        "% of Computers Infected with Malware",
        "% of Telnet Attacks by Originating Country (IoT)",
        "% of Attacks by Cryptominers",
        "Best Prepared for Cyberattacks",
        "Most Up-to-Date Legislation",
        "cert_count"]

for col in cols:
    x = merged_data[col]
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)
    print(f"Model for {col}")
    print(model.summary())

x = merged_data.loc[:, "% of Mobiles Infected with Malware":"cert_count"]
model = sm.OLS(y, x).fit()
model.predict(x)
print("Combined model")
print(model.summary())
# %%
