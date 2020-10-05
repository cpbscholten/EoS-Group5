import pandas

data_countries_instances = pandas.read_csv("results/countries_list.csv", usecols=['country', 'count']).set_index('country')
data_countries_speed = pandas.read_csv("Data/speedtest.csv", usecols=['country', 'speed']).set_index('country')
print(data_countries_speed)


both = pandas.merge(data_countries_instances, data_countries_speed, how='left', left_index=True, right_index=True)
print(both.corr())
