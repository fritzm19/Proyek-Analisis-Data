import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set Seaborn style
sns.set(style='darkgrid')

# Load the data
all_df = pd.read_csv("./dashboard/main_data.csv")

# Convert 'dteday' to datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Separate the DataFrames based on 'hr' column
day_df = all_df[all_df['hr'].isna()]
hour_df = all_df[all_df['hr'].notna()]

# Drop unnecessary columns from both DataFrames
day_df = day_df.drop(columns=['hr'], errors='ignore')
hour_df = hour_df.drop(columns=['week', 'year'], errors='ignore')

# Streamlit application layout
st.title("Bike Sharing Business Performance Analysis")

# Sidebar for user input
st.sidebar.title("Filters")
compare_both = st.sidebar.checkbox("Compare 2011 and 2012", value=False)

# Year selection based on comparison choice
if compare_both:
    year_selection = "Compare Both"
else:
    year_selection = st.sidebar.selectbox("Select Year", options=[2011, 2012])

# Calculate average number of customers
if year_selection == "Compare Both":
    average_customers_2011 = day_df[day_df.yr == 0]['cnt'].mean()
    average_customers_2012 = day_df[day_df.yr == 1]['cnt'].mean()
    overall_average = (average_customers_2011 + average_customers_2012) / 2

    st.markdown(f"### Average Number of Customers in 2011: {average_customers_2011:.2f}")
    st.markdown(f"### Average Number of Customers in 2012: {average_customers_2012:.2f}")
    st.markdown(f"### Overall Average Number of Customers (2011 & 2012): {overall_average:.2f}")
else:
    average_customers = day_df[day_df.yr == (year_selection - 2011)]['cnt'].mean()
    st.markdown(f"### Average Number of Customers in {year_selection}: {average_customers:.2f}")

# Monthly Performance Analysis
st.header("Monthly Performance Comparison")
if year_selection == "Compare Both":
    monthly_performance_2011 = day_df[day_df.yr == 0].groupby('mnth')['cnt'].sum()
    monthly_performance_2012 = day_df[day_df.yr == 1].groupby('mnth')['cnt'].sum()

    # Plotting Monthly Performance Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_performance_2011.index, monthly_performance_2011.values, marker='o', label='2011', color='blue')
    plt.plot(monthly_performance_2012.index, monthly_performance_2012.values, marker='o', label='2012', color='orange')
    plt.title('Comparison of Business Performance: 2011 vs 2012 (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Number of Customers')
    plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend()
    plt.grid()
else:
    monthly_performance = day_df[day_df.yr == (year_selection - 2011)].groupby('mnth')['cnt'].sum()

    # Plotting Monthly Performance for the selected year
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_performance.index, monthly_performance.values, marker='o', label=str(year_selection), color='blue' if year_selection == 2011 else 'orange')
    plt.title(f'Business Performance in {year_selection} (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Number of Customers')
    plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend()
    plt.grid()

st.pyplot(plt)

# Weekly Performance Analysis
st.header("Weekly Performance Comparison")
day_df['week'] = day_df['dteday'].dt.isocalendar().week

if year_selection == "Compare Both":
    weekly_performance_2011 = day_df[day_df.yr == 0].groupby('week')['cnt'].sum()
    weekly_performance_2012 = day_df[day_df.yr == 1].groupby('week')['cnt'].sum()

    # Plotting Weekly Performance Comparison
    plt.figure(figsize=(24, 6))
    plt.plot(weekly_performance_2011.index, weekly_performance_2011.values, marker='o', label='2011', color='blue')
    plt.plot(weekly_performance_2012.index, weekly_performance_2012.values, marker='o', label='2012', color='orange')
    plt.title('Comparison of Business Performance: 2011 vs 2012 (Weekly)')
    plt.xlabel('Week Number')
    plt.ylabel('Number of Customers')
    plt.xticks(ticks=range(1, 53), labels=list(range(1, 53)))
    plt.legend()
    plt.grid()
else:
    weekly_performance = day_df[day_df.yr == (year_selection - 2011)].groupby('week')['cnt'].sum()

    # Plotting Weekly Performance for the selected year
    plt.figure(figsize=(24, 6))
    plt.plot(weekly_performance.index, weekly_performance.values, marker='o', label=str(year_selection), color='blue' if year_selection == 2011 else 'orange')
    plt.title(f'Business Performance in {year_selection} (Weekly)')
    plt.xlabel('Week Number')
    plt.ylabel('Number of Customers')
    plt.xticks(ticks=range(1, 53), labels=list(range(1, 53)))
    plt.legend()
    plt.grid()

st.pyplot(plt)

# Hourly Performance Analysis
st.header("Hourly Performance Analysis")
hourly_performance = hour_df.groupby(['hr', 'workingday'])['cnt'].sum().unstack()

# Plotting Hourly Performance
plt.figure(figsize=(12, 6))
hourly_performance.plot(kind='line', marker='o')
plt.title('Comparison of Bike Rentals on Weekdays and Weekends by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Rentals')
plt.xticks(range(len(hourly_performance)))
plt.grid()
plt.legend(['Weekdays', 'Weekends'], title='Working Day', loc='upper right')
st.pyplot(plt)

# Correlation Analysis
st.header("Correlation Analysis")
cnt_correlation = day_df.corr()['cnt'].sort_values(ascending=False)

# Plotting Correlation
# Set the aesthetics for the plots
sns.set(style="whitegrid")

# Create a figure with subplots
plt.figure(figsize=(15, 5))

# Humidity (hum)
plt.subplot(1, 3, 1)
sns.regplot(x='hum', y='cnt', data=day_df, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plt.title('Humidity vs. Bike Rentals')
plt.xlabel('Humidity')
plt.ylabel('Count of Rentals')

# Windspeed (windspeed)
plt.subplot(1, 3, 2)
sns.regplot(x='windspeed', y='cnt', data=day_df, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plt.title('Windspeed vs. Bike Rentals')
plt.xlabel('Windspeed')
plt.ylabel('Count of Rentals')

# Weather Situation (weathersit)
plt.subplot(1, 3, 3)
sns.regplot(x='weathersit', y='cnt', data=day_df, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plt.title('Weather Situation vs. Bike Rentals')
plt.xlabel('Weather Situation')
plt.ylabel('Count of Rentals')

# Adjust layout
plt.tight_layout()
st.pyplot(plt)

# Display the data frame for user insight
st.subheader("Data Overview")
st.dataframe(day_df)


