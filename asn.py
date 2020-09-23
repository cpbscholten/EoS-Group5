#%%
import pandas
from pathlib import Path

if __name__ == "__main__":
    base_path = Path().absolute()
    data = pandas.read_csv(base_path / 'csv.txt', header=8, nrows=1000, parse_dates=['dateadded'])
    ips = data['url'].str.split('/').str[2].str.split(':').str[0]

    print("yay")


# %%
