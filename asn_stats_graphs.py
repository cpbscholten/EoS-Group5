import pandas
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # load csv files
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'dataset.csv')

    # Count instances of asn_name
    print(data.asn_name.value_counts())
    data.asn_name.value_counts().to_csv('results/asn_counts.csv')

    # descriptive statistics of average response time
    avg_response_times = data.loc[:, 'avg_response_time_seconds']

    print("Mean ", np.mean(avg_response_times))
    print("Median ", np.median(avg_response_times))
    print("Standard deviation ", np.std(avg_response_times))

    # Count instances of countries
    print(data.asn_loc.value_counts())
    data.asn_loc.value_counts().to_csv('results/countries_list.csv')