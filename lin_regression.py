import pandas as pd
import numpy as np
import statsmodels.api as sm

kaspersky = pd.read_csv('Data/kaspersky.csv').set_index('country')
speedtest = pd.read_csv('Data/speedtest.csv').set_index('country')
print(kaspersky.shape)
countries_instances = pd.read_csv('results/countries_list.csv').set_index('country')

merged_data1 = kaspersky.merge(countries_instances, on=['country'])
print(merged_data1.shape)
merged_data = merged_data1.merge(speedtest, on=['country'])
print(merged_data.shape)


# x = merged_data.loc[:, "% of Mobiles Infected with Malware":"Most Up-to-Date Legislation"]
y = merged_data['count']

cols = ["% of Mobiles Infected with Malware",
        "Financial Malware Attacks (% of Users)",
        "% of Computers Infected with Malware",
        "% of Telnet Attacks by Originating Country (IoT)",
        "% of Attacks by Cryptominers",
        "Best Prepared for Cyberattacks",
        "Most Up-to-Date Legislation",
        "speed"]

for col in cols:
    x = merged_data[col]
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)
    print(f"Model for {col}")
    print(model.summary())

x = merged_data[cols]
model = sm.OLS(y, x).fit()
model.predict(x)
print("Combined model")
print(model.summary())


# # standardise variables
# standardised_x = scale(x)
# standardised_x = pd.DataFrame(standardised_x, index=x.index, columns=x.columns)
# print(standardised_x.apply(np.mean))
# print(standardised_x.apply(np.std))
#
# pca = PCA().fit(standardised_x)
#
# def pca_summary(pca, standardised_data, out=True):
#     names = ["PC"+str(i) for i in range(1, len(pca.explained_variance_ratio_)+1)]
#     a = list(np.std(pca.transform(standardised_data), axis=0))
#     b = list(pca.explained_variance_ratio_)
#     c = [np.sum(pca.explained_variance_ratio_[:i]) for i in range(1, len(pca.explained_variance_ratio_)+1)]
#     columns = pd.MultiIndex.from_tuples([("sdev", "Standard deviation"), ("varprop", "Proportion of Variance"), ("cumprop", "Cumulative Proportion")])
#     summary = pd.DataFrame(zip(a, b, c), index=names, columns=columns)
#     if out:
#         print("Importance of components:")
#         display(summary)
#     return summary
#
# summary = pca_summary(pca, standardised_x)
