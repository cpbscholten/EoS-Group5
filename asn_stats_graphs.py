import pandas
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # load csv files
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'dataset.csv')

    # Count instances of asn_name
    asn_test = data.groupby(['asn_name', 'avg_response_time_seconds', 'domains_hosted']).size().sort_values(ascending=False)
    # asn_test.to_csv('results/asn_counts.csv')
    asn_test = pandas.read_csv('results/asn_counts.csv')
    print(asn_test)
    plt.scatter(asn_test['count'].values, asn_test['avg_response_time_seconds'].values)
    # plt.xscale('log')
    plt.xscale('log')
    plt.ylabel('Average response time (s)', fontsize=15)
    plt.xlabel('# of malicious content hosted', fontsize=15)
    plt.savefig('results/avg_response-malicous_content.pdf')
    plt.show()

    # descriptive statistics of average response time
    avg_response_times = data.loc[:, 'avg_response_time_seconds']

    print("Mean ", np.mean(avg_response_times))
    print("Median ", np.median(avg_response_times))
    print("Standard deviation ", np.std(avg_response_times))

    # Count instances of countries
    print(data.asn_loc.value_counts())
    data.asn_loc.value_counts().to_csv('results/countries_list.csv')

    # response time in seconds
    # test = data[['asn_name', 'asn_loc', 'avg_response_time', 'avg_response_time_seconds', 'domains_hosted']]
    # test.drop(test[test['domains_hosted'] == '-1'].index, inplace=True)
    # test.drop(test[test['avg_response_time_seconds'] == -1].index, inplace=True)
    # test.drop_duplicates(inplace=True)
    # test.sort_values(by=['avg_response_time_seconds'], inplace=True)
    # print(test)
    # test.to_csv('results/top_response_times_hp.csv')
