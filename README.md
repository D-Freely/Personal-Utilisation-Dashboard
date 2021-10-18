# Personal-Utilisation-Dashboard
Python script which creates an interactive dash web application from work utilisation data (dummy data used in the example below).

Python libraries used:
- Pandas
- Plotly
- Dash

### Description

At my job, the only tool we had to process personal utilisation data was an outdated timesheet system which we could use to export a csv file over a select time period. Once exported, the file was simply a table of raw data which we would then use to tell our story for moderation come year-end. I therefore decided to write this python script which, using plotly dash functionality, creates an interactive web application from the raw data csv file. Once the dash application is loaded, users can filter the graphs as they please and can also edit the date ranger slider to toggle between different performance periods. 

See the _code.py_ file for the python code. The dashboard itself is showcased in the following gif:


![Animation2](https://user-images.githubusercontent.com/92688098/137645624-80c07fdd-3bee-4c07-9ecc-4ef115f16c2f.gif)
