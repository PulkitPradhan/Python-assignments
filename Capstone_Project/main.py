import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
    
    def add_reading(self, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.meter_readings.append(reading)
    
    def calculate_total_consumption(self):
        total = sum(r.kwh for r in self.meter_readings)
        return total
    
    def generate_report(self):
        count = len(self.meter_readings)
        total = self.calculate_total_consumption()
        avg = total / count if count > 0 else 0
        return {
            "Building": self.name,
            "Total_kWh": total,
            "Average_kWh": avg,
            "Readings_Count": count
        }

class BuildingManager:
    def __init__(self):
        self.buildings = {}
    
    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

def ingest_data(data_dir):
    all_data = []
    
    if not os.path.exists(data_dir):
        logging.error(f"Directory {data_dir} not found.")
        return pd.DataFrame()

    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(filepath, on_bad_lines='skip')
                
                building_name = os.path.splitext(filename)[0]
                df['Building'] = building_name
                
                all_data.append(df)
                logging.info(f"Successfully loaded {filename}")
                
            except FileNotFoundError:
                logging.error(f"File {filename} not found.")
            except Exception as e:
                logging.error(f"Error reading {filename}: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
        return combined_df
    else:
        return pd.DataFrame()

def calculate_daily_totals(df):
    return df.set_index('timestamp').groupby('Building').resample('D')['kwh'].sum().reset_index()

def building_wise_summary(df):
    summary = df.groupby('Building')['kwh'].agg(['mean', 'min', 'max', 'sum']).reset_index()
    return summary

def create_dashboard(df, daily_totals, building_summary):
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    
    for building in daily_totals['Building'].unique():
        subset = daily_totals[daily_totals['Building'] == building]
        axes[0].plot(subset['timestamp'], subset['kwh'], label=building, marker='o')
    axes[0].set_title("Daily Energy Consumption Trends")
    axes[0].set_ylabel("kWh")
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].bar(building_summary['Building'], building_summary['sum'], color=['blue', 'orange'])
    axes[1].set_title("Total Energy Consumption per Building")
    axes[1].set_ylabel("Total kWh")
    
    for building in df['Building'].unique():
        subset = df[df['Building'] == building]
        axes[2].scatter(subset['timestamp'], subset['kwh'], label=building, alpha=0.6)
    axes[2].set_title("Consumption Events (Scatter)")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("kWh")
    axes[2].legend()
    
    plt.tight_layout()
    if not os.path.exists('output'):
        os.makedirs('output')
    plt.savefig('output/dashboard.png')
    print("Dashboard saved to output/dashboard.png")

def generate_outputs(df, building_summary, manager):
    if not os.path.exists('output'):
        os.makedirs('output')
        
    df.to_csv('output/cleaned_energy_data.csv', index=False)
    building_summary.to_csv('output/building_summary.csv', index=False)
    
    total_consumption = df['kwh'].sum()
    highest_building = building_summary.loc[building_summary['sum'].idxmax()]
    
    report_content = (
        "=== Campus Energy Executive Summary ===\n"
        f"Total Campus Consumption: {total_consumption:.2f} kWh\n"
        f"Highest Consuming Building: {highest_building['Building']} ({highest_building['sum']:.2f} kWh)\n"
        f"Average Consumption per Reading: {df['kwh'].mean():.2f} kWh\n"
        "\n--- Building OOP Reports ---\n"
    )
    
    for name, b_obj in manager.buildings.items():
        report_content += str(b_obj.generate_report()) + "\n"

    with open('output/summary.txt', 'w') as f:
        f.write(report_content)
        
    print(report_content)

def main():
    print("Starting Campus Energy Dashboard Pipeline...")
    
    df_combined = ingest_data('data')
    
    if df_combined.empty:
        print("No data found. Exiting.")
        return

    manager = BuildingManager()
    for index, row in df_combined.iterrows():
        b_obj = manager.get_or_create_building(row['Building'])
        b_obj.add_reading(row['timestamp'], row['kwh'])

    daily_stats = calculate_daily_totals(df_combined)
    summary_stats = building_wise_summary(df_combined)
    
    create_dashboard(df_combined, daily_stats, summary_stats)
    
    generate_outputs(df_combined, summary_stats, manager)
    
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
