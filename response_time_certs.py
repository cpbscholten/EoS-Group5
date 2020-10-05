#%% 
import pandas
from pathlib import Path
import re
import numpy as np
base_path = Path().absolute()

dataset = pandas.read_csv('asn_response_data.csv')
certs = pandas.read_json('irt-teams.json')


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

dataset['Country'] = dataset['Country'].str[2:]
dataset['response_time_seconds'] = string_to_seconds_list(dataset['Average Reaction Time'])

#%%
response_time_per_country = dataset.groupby(['Country']).agg({"response_time_seconds" : np.mean}) 
# %%
no_of_certs = certs.groupby(['country-code']).size().to_frame('cert_count')
both = pandas.merge(response_time_per_country, no_of_certs, how='left', left_index=True, right_index=True)