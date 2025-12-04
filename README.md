# Secure_Check_Traffic_Police_Logs
In the ipynb file:
Initially I'm reading the csv file called traffic_stops and converting it into a dataframe.
Post conversion clearing the unwanted columns like driver_race, driver_age_raw, violation_raw by dropping those columns.
Creating a new column called timestamp by concatenating the values from stop_date and stop_time columns and converting the resulting strings into datetime objects.
Filling any missing values in the search_type column with the string 'None'.
Establishing the mysql workbench connection using the username and password.
Creating an object called cursor inorder to execute the SQL queries through the connection.
      
