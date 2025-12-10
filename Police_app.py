import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from datetime import date

#Database Connection

def create_connection():
    try:
        connection=pymysql.connect(
            host='localhost',
            user='root',
            password='Mysql@1013',
            database='policestop_logs',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        st.error(f"Database connection Error: {e}")
        return None
    


#Fetch data from database

def fetch_data(select_query):
    connection=create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                result=cursor.fetchall()
                df=pd.DataFrame(result,columns=[i[0] for i in cursor.description])
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()



#Streamlit UI Setup

st.set_page_config(page_title="Traffic Police Dashboard",layout="wide")
st.title("👮‍♂️ SecureCheck: A Python-SQL Digital Ledger for Police Post Logs")
st.divider()



df = pd.read_csv("traffic_stops.csv")

#Quick Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_stops = df.shape[0]
    st.metric("Total Police Stops", total_stops)

with col2:
    arrests = df[df['stop_outcome'].str.contains("arrest", case=False, na=False)].shape[0]
    st.metric("Total arrests", arrests)

with col3:
    warnings_count = df[df['stop_outcome'].str.contains('warning', case=False, na=False)].shape[0]
    st.metric("Total Warnings", warnings_count)

with col4:
    drugs_related_stop = df[df['drugs_related_stop'] == 1].shape[0]
    st.metric("Drug Related Stops", drugs_related_stop)


#Visual Representation of traffic police logs data
# Display bar chart in Streamlit


st.header("📈 Visual Insights")
tab1, tab2 = st.tabs(["Insights based on Violation", "Insights based on Driver Gender"])



violation_type = {
    'Violation Type': ['Speeding', 'Signal', 'DUI', 'Other', 'Seatbelt'],
    'Count': [26300, 26224, 26150, 26388,26014]
}
df_violation = pd.DataFrame(violation_type)


gender_distribution={
    'Country Name': ['Canada (Male)','India (Male)','USA (Male)','Canada (Female)','USA (Female)','India (Female)'],
    'Driver Gender Distribution': [21822, 21910, 21582, 21994,21682,22086],
    'Gender':['Male','Male','Male','Female','Female','Female']
}
df_gender=pd.DataFrame(gender_distribution)


fig_violation = px.bar(
    df_violation,
    x='Violation Type',
    y='Count',
    color='Violation Type',
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="Stops Based On different Violations"
)


fig_gender = px.bar(
    df_gender,
    x='Country Name',
    y='Driver Gender Distribution',
    color='Gender',
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="Gender Distribution Across Countries"
)


with tab1:
    st.plotly_chart(fig_violation, use_container_width=False)

with tab2:
    st.plotly_chart(fig_gender, use_container_width=False)


#Advanced Queries

st.header("🧩 Advanced Insights")

selected_query=st.selectbox("Select a query to Run",[
"Top 10 Vehicle Number involved in Drug Related Stops",
"Most frequenctly searched Vehicles",
"Driver Age group with High Arrest Rate",
"Gender Distribution of Drivers stopped in each country",
"Gender that has highest search rate",
"Time of the day that has the most traffic stops",
"Average stop duration for different violation",
"Night stops likely to lead to arrests",
"Is there a violation that rarely results in search or arrest?",
"Which violations are most common among younger drivers (<25)",
"Violation that are associated with search or arrest",
"Countries with highest rate of drug related stops",
"Arrest rate by country and violation",
"Country with most stops with search conducted",
"Yearly Breakdown of Stops and Arrests by Country(Using Subquery and Window Functions)",
"Driver Violation Trends Based on Age (Join with Subquery)",
"Time Period Analysis of Stops (Joining with Date Functions), Number of Stops by Year, Month, Hour of the Day",
"Violations with High Search and Arrest Rates (Window Function)",
"Driver Demographics by Country (Age, Gender)",
"Top 5 Violations with Highest Arrest Rates"
]
)

select_query={
  "Top 10 Vehicle Number involved in Drug Related Stops": "select vehicle_number, count(*) as stop_count from traffic_analysis where drugs_related_stop=1 group by vehicle_number order by stop_count asc limit 10;",
  "Most frequenctly searched Vehicles":"select vehicle_number, count(*) as search_conducted from traffic_analysis where search_conducted = True group by vehicle_number order by search_conducted desc limit 10;",
  "Driver Age group with High Arrest Rate":"select driver_age, count(*) as is_arrested from traffic_analysis where is_arrested=1 group by driver_age order by is_arrested desc limit 10;",
  "Gender Distribution of Drivers stopped in each country":"select country_name, driver_gender, count(*) as driver_distribution from traffic_analysis group by country_name, driver_gender;",
  "Gender that has highest search rate":"select driver_gender, count(*) as search_rate from traffic_analysis where search_conducted=True group by driver_gender order by search_rate desc;",
  "Time of the day that has the most traffic stops":"select stop_time, count(*) as most_traffic_stops from traffic_analysis group by stop_time order by most_traffic_stops desc limit 5;",
  "Average stop duration for different violation" :"select violation, avg(stop_duration) from traffic_analysis group by violation;",
  "Night stops likely to lead to arrests":"select case when stop_time between '06:00:00' and '18:00:00' then 'day' else 'night' end as 'arrest_time', count(*)as total_arrests from traffic_analysis where is_arrested='1' group by case when stop_time between '06:00:00' and '18:00:00' then 'day' else 'night' end;",
  "Is there a violation that rarely results in search or arrest?": "select violation, SUM(CASE WHEN search_conducted = True then 1 else 0 end) as total_search, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests from traffic_analysis group by violation;",
  "Which violations are most common among younger drivers (<25)":"select violation, count(*) as count from traffic_analysis where driver_age < 25 group by violation;",
  "Violation that are associated with search or arrest":"select violation, count(*) as total_arrest from traffic_analysis where stop_outcome like '%arrest%'group by violation;",
  "Countries with highest rate of drug related stops":"select country_name, count(*) as highest_drug_related_stop from traffic_analysis where drugs_related_stop='1' group by country_name order by Highest_drug_related_stop desc;",
  "Arrest rate by country and violation":"select country_name, violation,round(sum(case when is_arrested = True then 1 else 0 end)*100/count(*), 2) as arrest_rate from traffic_analysis group by country_name, violation order by violation;",
  "Country with most stops with search conducted":"select country_name, count(*) as total_stops from traffic_analysis where search_conducted= True group by country_name order by total_stops desc;",
  "Yearly Breakdown of Stops and Arrests by Country(Using Subquery and Window Functions)":"select country_name, yearly_breakdown, SUM(total_stops) OVER (PARTITION BY country_name) AS total_stops, SUM(total_arrests) OVER (PARTITION BY country_name) AS total_arrests from (select country_name, count(*) as total_stops, extract(year from stop_date) as yearly_breakdown, sum(case when is_arrested = True then 1 else 0 end) as total_arrests from traffic_analysis group by country_name, extract(year from stop_date)) as yearly_data order by country_name, yearly_breakdown;",
  "Driver Violation Trends Based on Age (Join with Subquery)": "select distinct v.violation, ta.driver_age from traffic_analysis ta join (select driver_age, count(*) as violation from traffic_analysis group by driver_age) as v on ta.driver_age = v.driver_age order by v.violation desc;",
  "Time Period Analysis of Stops (Joining with Date Functions), Number of Stops by Year, Month, Hour of the Day":"select year(stop_date) as stop_year, month(stop_date) as stop_month, hour(stop_time) as stop_hour, count(*) as Number_of_stops from traffic_analysis group by stop_year, stop_month, stop_hour;",
  "Violations with High Search and Arrest Rates (Window Function)":"select violation, count(*) as total_stops, sum(case when search_conducted = True then 1 else 0 end) as total_search, sum(case when is_arrested = True then 1 else 0 end) as total_arrest, rank() over (order by sum(case when search_conducted = True then 1 else 0 end)* 1.0 / Count(*)) as search, rank() over (order by sum(case when is_arrested = True then 1 else 0 end)* 1.0/ count(*)) as arrest from traffic_analysis group by violation;",
  "Driver Demographics by Country (Age, Gender)":"select country_name, driver_age, driver_gender,count(*) as total_drivers from traffic_analysis group by country_name, driver_age, driver_gender order by country_name, driver_age, driver_gender;",
  "Top 5 Violations with Highest Arrest Rates": "select violation, count(*) as total_stops, sum(case when is_arrested = True then 1 else 0 end) as total_arrest, round(sum(case when is_arrested = True then 1 else 0 end) *1.0/ count(*), 2) as arrest_rate from traffic_analysis group by violation order by total_arrest desc limit 5;"
}

if st.button("Run Query"):
    result = fetch_data(select_query[selected_query])
    if not result.empty:
        st.dataframe(result, height=250, width=400)
    else:
        st.warning("No results are found for the options.")

st.divider()


st.header("📋 Display the Predicted outcome and Violation")
st.text("✍️Fill in the details below to predict the outcome based on the existing data.")

# Input form for all fields(excluding outputs)
with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Driver Gender", ['Male','Female'])
    driver_age = st.number_input("Driver Age", min_value= 16, max_value= 100, value= 27)
    search_conducted = st.selectbox("Was a Search Conducted?", ["0","1"])
    search_type = st.text_input("Search Type")
    drugs_related_stop = st.selectbox("Was it Drugs Related", ["0","1"])
    stop_duration = st.selectbox("Stop Duration",df['stop_duration'].dropna().unique())
    vehicle_number = st.text_input("Vehicle Number")
    timestamp = pd.Timestamp.now()
    

# Filtered data for prediction
    if st.form_submit_button("🕵️ Predict Stop Outcome and Violation"):
        filter_data = df[
            (df['driver_gender'] == driver_gender) &
            (df['driver_age'] == driver_age) &
            (df['search_conducted'] == search_conducted) &
            (df['stop_duration'] == stop_duration) &
            (df['drugs_related_stop'] == int(drugs_related_stop))
        ]

        # Predict stop outcome
        if not filter_data.empty:
            predicted_outcome = filter_data['stop_outcome'].mode()[0]
            predicted_violation = filter_data['violation'].mode()[0]
        else:
            predicted_outcome = "Warning" 
            predicted_violation = "Speeding"

        # Natural Language Summary
        Search_text = "A Search was Conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug_related" if int(drugs_related_stop) else "was not 💊 drug_related"

        st.markdown(f"""
                    **Prediction Summary**
                    - **Predicted Violation:** {predicted_violation}
                    - **Predicted Stop Outcome:** {predicted_outcome}
                    
                    🚓 A  **{driver_age}**-year-old 🧍‍♂️ **{driver_gender}** driver in 🌎 **{country_name}** was stopped at 🕒**{stop_time.strftime('%I:%M%p')}** on 📅**{stop_date}**. 
                    {Search_text}, and the stop {drug_text}.
                    stop duration: **{stop_duration}**.
                    Vehicle Number: **{vehicle_number}**.
                    """)

st.divider()
st.header("📚 Police Checkpost Logs Overview")

st.write(df)


