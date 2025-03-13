import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

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

# Menyiapkan mothly_rent_df 
def create_monthly_rent_df(df):
    mothly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    }).reset_index()
    return mothly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan holiday_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count' : 'sum'
    }).reset_index()
    return season_rent_df

# Menyiapkan werather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather').agg({
        'count' : 'sum'
    }).reset_index()
    return weather_rent_df

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
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

st.header("Dicoding Bike Sharing Dashboard :bike:")
st.subheader("Data Overview")
st.write(main_df)

# Membuat jumlah penyewaan Bulanan
st.subheader('User Type')  
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

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Pie Chart Distribusi User Type
axes[0].pie(
    [daily_rent_casual, daily_rent_registered],
    labels=['Casual User', 'Registered User'], 
    autopct='%1.1f%%', 
    startangle=90,
    colors=['#ff9999','#66b3ff'],
    explode=(0.1, 0),
    wedgeprops={'edgecolor': 'black'}
)
axes[0].set_title('User Type Distribution')

total_user_type_rent_df = pd.DataFrame({
    'User Type': ['Casual', 'Registered'],
    'Total Users': [daily_casual_rent_df['casual'].sum(), daily_registered_rent_df['registered'].sum()]
})
# Barplot Total Pengguna per Hari
sns.barplot(
    data=total_user_type_rent_df,
    x='User Type', 
    y='Total Users', 
    hue='User Type', 
    palette=['#ff9999', '#66b3ff'],
    ax=axes[1]
)
axes[1].set_xlabel('Tanggal')
axes[1].set_ylabel('Total Users')
axes[1].set_title('Total Pengguna Casual vs Registered per Hari')
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend(title='User Type')
axes[1].grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader('Monthly Rentals')
col1, col2,  col3  = st.columns(3)
with col1:
    monthly_max = monthly_rent_df['count'].idxmax()
    monthly_max_count = monthly_rent_df.loc[monthly_max, 'count']
    st.metric('Most Rented Month', value= monthly_rent_df.loc[monthly_max, 'month'])
    st.metric('Count', value= monthly_max_count)
    
with col2:
    monthly_min = monthly_rent_df['count'].idxmin() 
    monthly_min_count = monthly_rent_df.loc[monthly_min, 'count']
    st.metric('Least Rented Month', value= monthly_rent_df.loc[monthly_min, 'month'])
    st.metric('Count', value= monthly_min_count)

with col3:
    monthly_avg = monthly_rent_df['count'].mean().round(0)
    monthly_total = monthly_rent_df['count'].sum()
    st.metric('Average Rentals', value= monthly_avg)
    st.metric('Total Rentals', value= monthly_total)

# Membuat Line Chart rata-rata jumlah penyewaan per bulan 
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=main_df, x='month', y='count', hue='year', estimator=np.mean,
             marker='o', errorbar=None, palette='tab10')
plt.title('Average Daily Rentals by Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# Membuat Histogram distribusi jumlha penyewa
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=main_df, x='count', kde=True, hue='year', palette='tab10')
plt.xlabel('Jumlah Sepeda yang Dipinjam')
plt.ylabel('Frekuensi')
plt.title('Distribusi Peminjaman Sepeda')
plt.grid(True)
st.pyplot(fig)

# Jumlah Penyewaan Berdasarkan Hari
st.subheader('Daily Rentals')
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
sns.barplot(
    data=df,
    x='weekday',
    y='count',
    hue='year',
    estimator=np.mean,  
    errorbar=None,
    palette='tab10',
    order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
st.pyplot(fig)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].pie(
    workingday_rent_df['count'], 
    labels=['Libur (0)', 'Hari Kerja (1)'],  
    autopct='%1.1f%%', 
    colors=['#ff9999', '#66b3ff'], 
    startangle=140, 
    wedgeprops={'edgecolor': 'black'}
)
axes[0].set_title('Proporsi Peminjaman Sepeda\nBerdasarkan Hari Kerja')

# Barplot Total Peminjaman Sepeda Berdasarkan Hari Kerja
sns.barplot(
    data=df,
    x='workingday',
    y='count',
    hue='year',
    estimator=np.mean,  
    errorbar=None,
    palette='tab10',
    ax=axes[1]
)
axes[1].set_xlabel('Hari Kerja (0 = Libur, 1 = Hari Kerja)')
axes[1].set_ylabel('Rata-rata Peminjaman Sepeda')
axes[1].set_title('Rata-rata Peminjaman Sepeda Berdasarkan Hari Kerja')
axes[1].legend(title="Tahun")
plt.tight_layout()
st.pyplot(fig)


st.subheader('Seasonal Rentals')
col1, col2,  col3  = st.columns(3)
with col1:
    season_max = season_rent_df['count'].idxmax()
    season_max_count = season_rent_df.loc[season_max, 'count']
    st.metric('Most Rented Day', value= season_rent_df.loc[season_max, 'season'])
    st.metric('Count', value= season_max_count)
    
with col2:
    season_min = season_rent_df['count'].idxmin() 
    season_min_count = season_rent_df.loc[season_min, 'count']
    st.metric('Least Rented Day', value= season_rent_df.loc[season_min, 'season'])
    st.metric('Count', value= season_min_count)

with col3:
    season_avg = season_rent_df['count'].mean().round(0)
    season_total = season_rent_df['count'].sum()
    st.metric('Average Rentals', value= season_avg)
    st.metric('Total Rentals', value= season_total)
    
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].pie(
    season_rent_df['count'], 
    autopct='%1.1f%%', 
    labels=['Fall','Spring', 'Summer', 'Winter'],
    colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
    startangle=140, 
    wedgeprops={'edgecolor': 'black'}
)
axes[0].set_title('Proporsi Peminjaman Sepeda Berdasarkan Musim')

# Barplot Total Peminjaman Sepeda Berdasarkan Hari Kerja
sns.barplot(
    data=main_df,
    x='season',
    y='count',
    hue='year',
    estimator=np.mean,  
    errorbar=None,
    palette='tab10',
    ax=axes[1]
)
axes[1].set_title('Rata-Rata Peminjaman Sepeda Berdasarkan Musim')
axes[1].set_ylabel('Rata-Rata Peminjaman Sepeda')
axes[1].set_xlabel('Musim')
axes[1].legend(title="Tahun")
plt.tight_layout()
st.pyplot(fig)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].pie(
    weather_rent_df['count'], 
    autopct='%1.1f%%', 
    labels=['Clear/Few Clouds', 'Mist/Cloudy', 'Light Snow/Rain'],
    colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
    startangle=140, 
    wedgeprops={'edgecolor': 'black'}
)
axes[0].set_title('Proporsi Peminjaman Sepeda Berdasarkan Cuaca')

# Barplot Total Peminjaman Sepeda Berdasarkan Hari Kerja
sns.barplot(
    data=main_df,
    x='weather',
    y='count',
    hue='year',
    estimator=np.mean,  
    errorbar=None,
    palette='tab10',
    ax=axes[1]
)
axes[1].set_title('Rata-Rata Peminjaman Sepeda Berdasarkan Cuaca')
axes[1].set_ylabel('Rata-Rata Peminjaman Sepeda')
axes[1].set_xlabel('Cuaca')
axes[1].legend(title="Tahun")
plt.tight_layout()
st.pyplot(fig)

fig, axes = plt.subplots(figsize=(18, 6))
# Pairplot
pairplot = sns.pairplot(
    main_df[['count', 'temp', 'humidity', 'windspeed']], 
    diag_kind='kde', 
    kind='reg', 
    plot_kws={'line_kws': {'color': 'red'}},
)
pairplot.fig.suptitle('Scatter Plot Antarvariabel', y=1.02)
st.pyplot(pairplot.fig)

fig, axes = plt.subplots(figsize=(18, 10))
# Heatmap Korelasi
sns.heatmap(
    main_df[['count', 'temp', 'humidity', 'windspeed']].corr(), 
    annot=True, 
    cmap='coolwarm', 
    fmt=".2f", 
    linewidths=2,
    annot_kws={"size": 20} 
)
plt.title('Heatmap Korelasi Variabel')
plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright © Muhammad Husni Zahran Nugrahanto 2025')