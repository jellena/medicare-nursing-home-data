## Overview
Here is a little project to show some of the skills ACHP is looking for in their next analyst.

##### Data
Data on nursing home metrics was downloaded from [data.medicare.gov](https://data.medicare.gov/data?tool=nursing-home-compare&tag=&sort=alpha&q=).
* For testing unzip all files from medicare_nursing_data.zip into the data directory

##### Hosting
Next an AWS RDS instance running PostgreSQL 11.6 was spun up and configured for access.
* Please feel free to use the credentials given to Karen or reach out to myself for access if you'd like to poke around.

##### Processing
A small script in python was created that checks a directory and formats any csv files into a table.
 * This was more proof of concept and more time would be needed to accurately translate pandas datatypes into relevant SQL ones.
 * Additionally while working through this I discovered Postgres RDS instances have restrictions on super user access which prevented me from updating tables within the bounds of a jupyter notebook.
* Data was imported into the created tables through the pgAdmin 4 console.

##### Analysis
Finally a Tableau workbook was connected to the server and small dashboard was created showcasing some of the data.

[Tableau Public Link](https://public.tableau.com/profile/jacob.ellena#!/vizhome/medicare-nursing-home-data-snapshot/Dashboard)
