#%%
import pandas

data_countries_instances = pandas.read_csv("results/countries_list.csv", usecols=['country', 'count'])
data_countries_instances['country'] = data_countries_instances['country'].str.strip()

data_countries_speed = pandas.read_csv("Data/speedtest.csv", usecols=['country', 'speed'])
data_countries_speed['country'] = data_countries_speed['country'].str.strip()


both = pandas.merge(data_countries_instances, data_countries_speed, how='left', left_on='country', right_on='country')
print(both.corr())