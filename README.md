# Secure_Check_Traffic_Police_Logs
In the ipynb file:
Initially I'm reading the csv file called traffic_stops and converting it into a dataframe.
Post conversion clearing the unwanted columns like driver_race, driver_age_raw, violation_raw by dropping those columns.
Creating a new column called timestamp by concatenating the values from stop_date and stop_time columns and converting the resulting strings into datetime objects.
Filling any missing values in the search_type column with the string 'None'.
Establishing the mysql workbench connection using the username and password.
Creating an object called cursor inorder to execute the SQL queries through the connection.
Now creating a database using the query and executing the use query to use the database.
Creating the table traffic_analysis. The table schema includes columns like Vehicle_ID (primary key, auto-increment), stop_date, stop_time, driver_age (INT), and timestamp (Datetime)
Converting stop_date and stop_time to correct datetime format.
Defining my insert query for inserting the data from the dataframe into my sql.
Initiating a loop that iterates row by row over the DataFrame df.
Executing the insert_query for the current row by passing the tuple of columns as values by checking wheteher data is missing and Nan data to be handled by None.
Committing the changes (the inserted rows) to the MySQL database.

In the py file:
I have imported the essential libraries.Then I have created a database connection for mysql.
Then I have created a function called fetchdata(select_query) to execute the SQL select_query. 
Post this the the result is stored in a Dataframe.
Then the Streamlit UI setup along with the Bar chart representation and the Advanced Queries selectbox for analysing the different scenario outcomes.
