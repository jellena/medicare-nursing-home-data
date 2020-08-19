# Imports
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib as plt
import glob
import os

# ## Creating SQL Engine and Connection

# ### Set the connection variables
# Reach out to Karen from TPO or myself for login credentials

postgres_user     = '*****' # Update user name
postgres_password = '*****' # Update password
postgres_host     = '*****' # Update host address
postgres_port     = '*****' # Update port
postgres_database = '*****' # Update database name


# Connection code from https://pynative.com/python-postgresql-tutorial/
connection = psycopg2.connect(user     = postgres_user,
                              password = postgres_password,
                              host     = postgres_host,
                              port     = postgres_port,
                              database = postgres_database)
cursor = connection.cursor()


# Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")


# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")


# Functions for Building Tables
# Creating a list of files in directory
files = []
for file in glob.glob('.\data\*.csv'): # creates relative files paths from current directory
    files.append(file.replace('.\\data\\', ''))


# Creating dictionary to replace panda data types with postgres data types
dtype_dict = {
    'object'  : 'TEXT',
    'int64'   : 'INTEGER',
    'bool'    : 'BOOLEAN',
    'float64' : 'NUMERIC'
}


# Function for formating and builing tables
def sql_table_builder(files_list):
    for file in files_list:
        # Temporary dataframe to pull out and format columns names
        temp_df = pd.read_csv(f'./data/{file}')
        # Converting column names to lower case font, replacing all white space with '_', and removing all '-'
        temp_df.columns = temp_df.columns.str.replace(' ', '_').str.replace('-','').str.lower()
        # Setting table name
        temp_table = file.replace('.csv', '')
        # Creating a dictionary of column data types
        temp_column_dtypes_dict = dict(temp_df.dtypes)
        # Creating the table using the first column in the data frame as the PK
        # This column is the same for each data file
        cursor.execute(f'''
        CREATE TABLE {temp_table} (
        {temp_df.columns[0]} TEXT
        )''')
        # Pushing table to server
        connection.commit()
        # Iterating through each column but the first
        for column in temp_df.columns[1:]:
            # Converting the data type of the column into a string
            temp_data_type = str(temp_column_dtypes_dict[column])
            # Converting the pandas data type into a Postgres data type
            temp_data_type_converted = temp_data_type.replace(temp_data_type, dtype_dict[temp_data_type])
            # Adding column with converted data type to table
            cursor.execute(f'''
            ALTER TABLE {temp_table}
            ADD COLUMN {column} {temp_data_type_converted};
            ''')
            connection.commit()


sql_table_builder(files)
