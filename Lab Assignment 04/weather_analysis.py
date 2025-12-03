import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def create_dummy_csv(filename='weather_data.csv'):
    start_date = "2024-01-01"
    days = 365
    date_range = pd.date_range(start=start_date, periods=days)
    x = np.linspace(0, 2 * np.pi, days)
    base_temp = 25
    season_swing = 15 * np.sin(x - 2.5)
    noise = np.random.normal(0, 2, days)
    temperature = base_temp + season_swing + noise
    rainfall = []
    for day_num, temp in enumerate(temperature):
        if 180 < day_num < 270:
            rain = np.random.choice([0, np.random.uniform(5, 50)], p=[0.4, 0.6])
        else:
            rain = np.random.choice([0, np.random.uniform(1, 10)], p=[0.9, 0.1])
        rainfall.append(rain)
    humidity = []
    for r, t in zip(rainfall, temperature):
        base_hum = 40
        if r > 0:
            hum = np.random.uniform(70, 95)
        else:
            hum = np.random.uniform(30, 60)
        humidity.append(hum)
    df = pd.DataFrame({
        'Date': date_range,
        'Temperature': np.round(temperature, 1),
        'Rainfall': np.round(rainfall, 1),
        'Humidity': np.round(humidity, 1)
    })
    df.loc[10, 'Temperature'] = np.nan
    df.loc[50, 'Rainfall'] = np.nan
    df.to_csv(filename, index=False)
    print(f"[SUCCESS] Generated '{filename}' with {days} days of realistic weather data.")

def load_and_inspect_data(filename):
    print("\n--- Task 1: Loading Data ---")
    try:
        df = pd.read_csv(filename)
        print("First 5 rows:")
        print(df.head())
        print("\nInfo:")
        print(df.info())
        print("\nDescription:")
        print(df.describe())
        return df
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def clean_data(df):
    print("\n--- Task 2: Cleaning Data ---")

    df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
    df['Rainfall'] = df['Rainfall'].fillna(0)


    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    print("Missing values handled and Date converted.")
    return df

def analyze_statistics(df):
    print("\n--- Task 3: Statistical Analysis ---")

    temps = df['Temperature'].to_numpy()

    print(f"Mean Temperature: {np.mean(temps):.2f}")
    print(f"Max Temperature: {np.max(temps):.2f}")
    print(f"Min Temperature: {np.min(temps):.2f}")
    print(f"Std Dev Temperature: {np.std(temps):.2f}")

def visualize_data(df):
    print("\n--- Task 4: Visualization ---")

    if not os.path.exists('plots'):
        os.makedirs('plots')

    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Temperature'], label='Temp (°C)', color='red')
    plt.title('Daily Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.legend()
    plt.savefig('plots/temp_trend.png')
    plt.show()

    df['Month'] = df['Date'].dt.month_name()
    monthly_rain = df.groupby('Month')['Rainfall'].sum()

    plt.figure(figsize=(10, 5))
    monthly_rain.plot(kind='bar', color='blue')
    plt.title('Monthly Rainfall Totals')
    plt.xlabel('Month')
    plt.ylabel('Rainfall (mm)')
    plt.savefig('plots/rainfall_bar.png')
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.scatter(df['Temperature'], df['Humidity'], color='green', alpha=0.5)
    plt.title('Humidity vs. Temperature')
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.grid(True)
    plt.savefig('plots/hum_vs_temp.png')
    plt.show()

def group_and_aggregate(df):
    print("\n--- Task 5: Grouping & Aggregation ---")

    monthly_stats = df.groupby('Month').mean(numeric_only=True)

    print("\nMonthly Averages:")
    print(monthly_stats)
    return monthly_stats

def export_results(df):
    print("\n--- Task 6: Exporting Data ---")
    df.to_csv('cleaned_weather_data.csv', index=False)
    print("Cleaned data saved to 'cleaned_weather_data.csv'.")
    print("Plots saved in 'plots/' folder.")

if __name__ == "__main__":
    create_dummy_csv()

    weather_df = load_and_inspect_data('weather_data.csv')

    if weather_df is not None:
        weather_df = clean_data(weather_df)

        analyze_statistics(weather_df)

        visualize_data(weather_df)

        group_and_aggregate(weather_df)

        export_results(weather_df)