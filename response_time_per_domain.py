import matplotlib.pyplot as plt
import csv
from operator import itemgetter
import datetime
from tabulate import tabulate

first_line = True

response_time_per_domains  = {}
number_of_domains = {}

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
    else:
        minutes = 0
    return datetime.timedelta(days=days, hours=hours, minutes=minutes)

with open('dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if first_line:
            first_line = False
            pass
        else:
            number_of_domain = row[13]
            if number_of_domain in number_of_domains:
                number_of_domains[number_of_domain] += 1
                response_time_per_domains[number_of_domain] += string_to_datetime(row[11])
            else:
                number_of_domains[number_of_domain] = 1
                response_time_per_domains[number_of_domain] = string_to_datetime(row[11])

#print(response_time_per_country)

average_response_time = {}

for key in number_of_domains:
    if(key != "" and key.isdigit()):
        average_response_time[key] = str(response_time_per_domains[key] / number_of_domains [key])

average_list = list(map(list, average_response_time.items()))

print(tabulate(average_list, headers=['Number of domains', 'Avg Response Time']))
