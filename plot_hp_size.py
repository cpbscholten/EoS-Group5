import matplotlib.pyplot as plt
import csv
from operator import itemgetter

first_line = True

biggest_hp = []

with open('domains_hosted_per_asn.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if first_line:
            first_line = False
            pass
        count_domain = int(row[2])
        name_hp = row[1][8:]
        biggest_hp.append([count_domain, name_hp])

print(biggest_hp[:10])
sorted_list = sorted(biggest_hp, key=itemgetter(0))[-10:]

plt.pie([item[0] for item in sorted_list], autopct="%0.0f%%")#, labels=[item[1] for item in sorted_list], autopct="%0.0f%%")
plt.legend([item[1] for item in sorted_list],bbox_to_anchor=(0.85,1.025), loc="upper left")
plt.show()