import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set_style('dark')

# Load data
df = pd.read_csv('main_data.csv')

# Ubah nama kolom
df = df.rename(columns={'yr':'year', 'mnth':'month', 'hum':'humidity', 'weathersit':'weather', 'cnt':'count'})

# Ubah kolom menjadi datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Ubah kolom menjadi kategori
df['year'] = df['dteday'].dt.year      
df['month'] = df['dteday'].dt.strftime('%B')
df['weekday'] = df['dteday'].dt.day_name() 

# Ubah kolom menjadi boolean
df['holiday'] = df['holiday'].astype('bool')
df['workingday'] = df['workingday'].astype('bool')

# Mapping season (1 → Spring, 2 → Summer, 3 → Fall, 4 → Winter)
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

# Mengganti angka pada kolom musim dengan label kategori
df['season'] = df['season'].map(season_map)

weather_map = {1: 'Clear/Few Clouds', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}

# Mengganti angka pada kolom cuaca menjadi label kategori
df['weather'] = df['weather'].map(weather_map)


# Fungsi 
# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan holiday_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan daily_avg_temp_df
def create_daily_avg_temp_df(df):
    daily_avg_temp_df = df.groupby(by='dteday').agg({
        'temp': 'mean'
    }).reset_index()
    return daily_avg_temp_df

# Menyiapkan daily_avg_humidity_df
def create_daily_avg_humidity_df(df):
    daily_avg_humidity_df = df.groupby(by='dteday').agg({
        'humidity': 'mean'
    }).reset_index()
    return daily_avg_humidity_df

# Menyiapkan daily_avg_windspeed_df
def create_daily_avg_windspeed_df(df):
    daily_avg_windspeed_df = df.groupby(by='dteday').agg({
        'windspeed': 'mean'
    }).reset_index()
    return daily_avg_windspeed_df

# Filter data
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.title("Bike Sharing Dashboard")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
daily_avg_temp_df = create_daily_avg_temp_df(main_df)
daily_avg_humidity_df = create_daily_avg_humidity_df(main_df)
daily_avg_windspeed_df = create_daily_avg_windspeed_df(main_df)

st.header("Dicoding Bike Sharing Dashboard :bike:")
st.subheader("Data Overview")
st.write(main_df)

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
    
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)

# Membuat Line Chart jumlah penyewaan harian
if len(main_df) > 1:
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(daily_rent_df['dteday'], daily_rent_df['count'], marker='o', color='#90CAF9')
    plt.title('Daily Rentals')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Membuat Pie Chart Distribusi User Type
fig, ax = plt.subplots(figsize=(5, 6))
plt.pie([daily_rent_casual, daily_rent_registered],
        labels=['Casual User', 'Registered User'], 
        autopct='%1.1f%%', 
        startangle=90,
        colors=['#ff9999','#66b3ff'],
        explode=(0.1, 0),
        wedgeprops={'edgecolor': 'black'})
plt.title('User Type Distribution')
st.pyplot(fig)

# Jumlah Penyewaan Berdasarkan Hari
st.subheader('Daily Rentals by Weekday')
col1, col2,  col3  = st.columns(3)
with col1:
    weekday_max = weekday_rent_df['count'].idxmax()
    weekday_max_count = weekday_rent_df.loc[weekday_max, 'count']
    st.metric('Most Rented Day', value= weekday_rent_df.loc[weekday_max, 'weekday'])
    st.metric('Count', value= weekday_max_count)
    
with col2:
    weekday_min = weekday_rent_df['count'].idxmin() 
    weekday_min_count = weekday_rent_df.loc[weekday_min, 'count']
    st.metric('Least Rented Day', value= weekday_rent_df.loc[weekday_min, 'weekday'])
    st.metric('Count', value= weekday_min_count)

with col3:
    weekday_avg = weekday_rent_df['count'].mean().round(0)
    weekday_total = weekday_rent_df['count'].sum()
    st.metric('Average Rentals', value= weekday_avg)
    st.metric('Total Rentals', value= weekday_total)

# Membuat Bar Chart Jumlah Penyewaan Berdasarkan Hari
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weekday_rent_df, y='count', x='weekday',
            order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            palette=['#5faaff','#4f9fff', '#62a8ff','#5fafff','#80c1ff','#6aaeff','#70b0ff'])
plt.title('Daily Rentals by Weekday')
plt.xlabel('Count')
plt.ylabel('Weekday')
plt.grid(True)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
plt.pie(holiday_rent_df['count'], labels=['Non-Holiday', 'Holiday'],
        autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'],
        wedgeprops={'edgecolor': 'black'})
plt.title('Holiday Distribution')
st.pyplot(fig)



# Jumlah Penyewaan Berdasarkan Season
st.subheader('Daily Rentals by Weather')

col1, col2, col3 = st.columns(3)

with col1:
    daily_avg_temp = daily_avg_temp_df['temp'].mean()
    st.metric('Average Temperature', value= f"{daily_avg_temp:.2f} °C")

with col2:
    daily_avg_humidity = daily_avg_humidity_df['humidity'].mean()
    st.metric('Average Humidity', value= f"{daily_avg_humidity:.2f} %")
    
with col3:
    daily_avg_windspeed = daily_avg_windspeed_df['windspeed'].mean()
    st.metric('Average Windspeed', value= f"{daily_avg_windspeed:.2f} km/h")



# Membuat Bar Chart Jumlah Penyewaan Berdasarkan Musim
if main_df['season'].nunique() > 1:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_melted = main_df.melt(id_vars=['season'], value_vars=['registered', 'casual'], 
                             var_name='User Type', value_name='Count')
    sns.barplot(data=df_melted, x='season', y='Count', hue='User Type', 
            estimator=sum, ci=None, palette=['#ff9999','#66b3ff'], dodge=True)
    plt.legend()
    plt.title('Daily Rentals by Season')
    plt.xlabel('Season')
    plt.ylabel('Count')
    plt.grid(True)
    st.pyplot(fig)
    
# Membuat Bar Chart Jumlah Penyewaan Berdasarkan Cuaca
fig, ax = plt.subplots(figsize=(10, 6))
df_melted = main_df.melt(id_vars=['weather'], value_vars=['registered', 'casual'], 
                         var_name='User Type', value_name='Count')
sns.barplot(data=df_melted, x='weather', y='Count', hue='User Type', 
            estimator=sum, ci=None, palette=['#ff9999','#66b3ff'], dodge=True)
plt.legend()
plt.title('Daily Rentals by Weather')
plt.xlabel('Weather')
plt.ylabel('Count')
plt.grid(True)

st.pyplot(fig)

st.caption('Copyright © Muhammad Husni Zahran Nugrahanto 2025')