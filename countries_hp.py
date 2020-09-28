import matplotlib.pyplot as plt
import csv
from operator import itemgetter

first_line = True

countries = {}

with open('dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if first_line:
            first_line = False
            pass
        else:
            country = row[10]
            if country in countries:
                countries[country] += 1
            else:
                countries[country] = 1

print(countries)
ordered_countries = {k: v for k, v in sorted(countries.items(), key=lambda item: item[1], reverse=True)}
print(ordered_countries)

plt.bar(list(ordered_countries.keys())[1:11], list(ordered_countries.values())[1:11], width = 0.5, color='#0504aa',alpha=0.7)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Country',fontsize=15)
plt.ylabel('Istances',fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('Distribution of HPs',fontsize=15)

plt.savefig("country.pdf")
plt.show()
