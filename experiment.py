import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# convert csv into numpy
mobility_dataset = pd.read_csv('./2020_US_Region_Mobility_Report.csv') # Google's mobility dataset
precipitation_dataset = pd.read_csv('./3134619.csv') # NOAA's precipitation dataset

# keep only the mobility data from Rensselaer County
mobility_dataset.query("sub_region_2 == 'Rensselaer County'", inplace=True)

# keep only certain columns - from https://stackoverflow.com/questions/45846189/how-to-delete-all-columns-in-dataframe-except-certain-ones
mobility_keep = ['date','retail_and_recreation_percent_change_from_baseline',
'grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline',
'transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline',
'residential_percent_change_from_baseline'
]
mobility_dataset.drop(mobility_dataset.columns.difference(mobility_keep), axis=1, inplace=True)

# rename columns for readability
mobility_dataset.rename(columns={'retail_and_recreation_percent_change_from_baseline': 'Retail',
                                 'grocery_and_pharmacy_percent_change_from_baseline': 'Grocery',
                                 'parks_percent_change_from_baseline': 'Parks',
                                 'transit_stations_percent_change_from_baseline': 'Transit Stations',
                                 'workplaces_percent_change_from_baseline': 'Workplaces',
                                 'residential_percent_change_from_baseline': 'Residential'
                                 }, inplace=True)

precip_keep = ['DATE','PRCP']
precipitation_dataset.drop(precipitation_dataset.columns.difference(precip_keep), axis=1, inplace=True)


# https://stackoverflow.com/questions/30584486/join-two-pandas-dataframe-using-a-specific-column
# inner join drops rows where one table does not have a matching date
merged = pd.concat([mobility_dataset.set_index('date'),precipitation_dataset.set_index('DATE')], axis=1, join='inner').reset_index()


# remove the Date column
merged = merged.drop(['index'], axis=1)

# split data based on precipitation
rain = merged.query("`PRCP` != 0")
no_rain = merged.query("`PRCP` == 0")


rain_mean = rain.mean(axis=0)
no_rain_mean = no_rain.mean(axis=0)

print("ON RAINY DAYS")
print(rain_mean)
print("\nON NICE DAYS")
print(no_rain_mean)

# Create a graph to display the difference between mobility on rainy/not rainy days
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

labels = ["Retail","Grocery", "Parks", "Transit Stations", "Workplaces", "Residential"]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, rain_mean[0:-1], width, label="RAIN", color='#3098ff')
rects2 = ax.bar(x + width/2, no_rain_mean[0:-1], width, label="NO RAIN", color='#ebc934')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("Percent change")
ax.set_title("Percent change of mobility based on precipitation in Rensselaer County in 2020\n")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
fig.tight_layout()
plt.show()

print(mobility_dataset.shape)
print(precipitation_dataset.shape)
print(merged.shape)
