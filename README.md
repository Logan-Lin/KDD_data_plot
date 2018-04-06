# Air quality and meteorology data plotter for KDD 2018

## Simple introduction

An data plotter for viewing trendings of air quality and meteorology data, specialized for KDD 2018's data. Include a data plotter and a data fetcher for inserting latest API data into database.

## How to use

To use the plotter, you have to store KDD data into tables akin to the form of the provided MySQL scripts. If you are holding raw data provided in CSV files, you can use files in `csv_data_extract` to help you insert them into MySQL.

After your database is ready, you can use `data_plot/data_plot.py` to plot data. All the value you have to change are provided in the first 5 rows below the import statements. I recommand you to run this file in terminal so the matplotlib's windows can be displayed correctly.

Besides adjusting these variables, you can also use command line arguments. If you do the internal values will be replaced. The correct format should be:

	python data_plot.py {start_time} {end_time} {grid_count} {station_id1} {station_id2} ... {station_idn}

