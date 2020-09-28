import matplotlib.pyplot as plt
import csv
from operator import itemgetter

first_line = True

response_time_per_country  = {}
countries = {}

def string_to_datetime(string_to_parse):
    index_days = string_to_parse.find('days')
    index_hours = string_to_parse.find('hours')
    index_minutes = string_to_parse.find('minutes')
    if(index_days != -1):
        if ((string_to_parse[index_days-3]).isnumeric()):
            days = int(string_to_parse[index_days-3] + string_to_parse[index_days-2])
        else:
            days = int(string_to_parse[index_days-2])
    else:
        days = 0
    if(index_hours != -1):
        if ((string_to_parse[index_hours-3]).isnumeric()):
            hours = int(string_to_parse[index_hours-3] + string_to_parse[index_hours-2])
        else:
            hours = int(string_to_parse[index_hours-2])
    else:
        hours = 0
    if(index_minutes != -1):
        if ((string_to_parse[index_minutes-3]).isnumeric()):
            minutes = int(string_to_parse[index_minutes-3] + string_to_parse[index_minutes-2])
        else:
            minutes = int(string_to_parse[index_minutes-2])
    
    print(str(days) + ":" + str(hours) + ":" + str(minutes))


    #4 hours, 54 minutes


string_to_datetime("9 hours, 21 minutes")

'''with open('dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if first_line:
            first_line = False
            pass
        else:
            country = row[9]
            if country in countries:
                countries[country] += 1
                response_time_per_country[country] = row[11]
            else:
                countries[country] = 1
                response_time_per_country[country] = row[11]

print(countries)
ordered_countries = {k: v for k, v in sorted(countries.items(), key=lambda item: item[1])}
print(ordered_countries)

plt.bar(ordered_countries.keys(), ordered_countries.values(), width = 0.5, color='#0504aa',alpha=0.7)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Istances',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('Distribution of HPs',fontsize=15)
plt.show()
'''
