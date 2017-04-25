#!/usr/bin/python

# This script runs a MySQL query and saves the results 
# as a CSV file.

import csv
import datetime
import MySQLdb

# TODO: Get all this info from a config file.
homeDir = "/home/user/"
output_filename = "query_results_"
user = "us3r"
password = "p4ssw0rd"
host = "mysqldb.example.com"
database = "my_database"
port = "3306"
query = "SELECT * FROM table;"

# Open database connection.
connection = MySQLdb.connect(host,user,password,database)

# Prepare a cursor object using the cursor() method.
cursor = connection.cursor()

# Execute query and fetch results.
cursor.execute(query)
try:
    results = cursor.fetchall()
    # Get column names from executed query.
    header = [i[0] for i in cursor.description]
except Exception as exception:
    print "ERROR: Unable to fetch data. Reason:", exception
finally:
    # Closing DB connection.
    if connection:
        connection.close()

# Save results into a file.
with open(output_filename + 
    str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".csv", "w") as csv_file:
    # Create a writer object.
    writer = csv.writer(csv_file, dialect = "excel", delimiter = ",",
        quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    # Write the header (column names) into the file.
    writer.writerow(header)
    # Write the query results into the file.
    for row in results:
        writer.writerow(row)
