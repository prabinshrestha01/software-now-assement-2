import csv
from pathlib import Path
from statistics import mean, stdev

def main():
    # Define the folder containing the temperature data
    folder_path = Path(__file__).parent / "temperatures"
    
    # Check if the folder exists
    if not folder_path.exists():
        print(f"Error: The folder '{folder_path}' does not exist.")
        print("Please create the folder and place the .csv files inside it.")
        return

    # Find all CSV files in the folder
    csv_files = sorted(folder_path.glob("*.csv"))
    
    if not csv_files:
        print(f"No .csv files found in '{folder_path}'.")
        return

    # List to hold all processed data
    all_data = []

    # Columns representing the months
    month_columns = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']

    print(f"Processing {len(csv_files)} files...")

    for file in csv_files:
        try:
            # Read the CSV file
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                # Check if the file contains the expected month columns
                available_months = [col for col in month_columns if col in headers]
                
                if not available_months:
                    continue
                
                for row in reader:
                    station_name = row['STATION_NAME']
                    for month in available_months:
                        temp_str = row.get(month, '')
                        if temp_str and temp_str.strip():
                            try:
                                temperature = float(temp_str)
                                all_data.append({'STATION_NAME': station_name, 'Month': month, 'Temperature': temperature})
                            except ValueError:
                                pass
            
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    if not all_data:
        print("No valid data found to process.")
        return

    # ==========================================
    # Task 1: Seasonal Average
    # ==========================================
    # Define season mapping
    season_map = {
        'December': 'Summer', 'January': 'Summer', 'February': 'Summer',
        'March': 'Autumn', 'April': 'Autumn', 'May': 'Autumn',
        'June': 'Winter', 'July': 'Winter', 'August': 'Winter',
        'September': 'Spring', 'October': 'Spring', 'November': 'Spring'
    }

    # Add season to each record
    for record in all_data:
        record['Season'] = season_map[record['Month']]
    
    # Calculate mean temperature per season
    seasonal_temps = {}
    for record in all_data:
        season = record['Season']
        if season not in seasonal_temps:
            seasonal_temps[season] = []
        seasonal_temps[season].append(record['Temperature'])
    
    seasonal_stats = {season: mean(temps) for season, temps in seasonal_temps.items()}
    
    # Save to "average_temp.txt"
    with open("average_temp.txt", "w", encoding='utf-8') as f:
        # Custom order for output: Summer, Autumn, Winter, Spring
        for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
            if season in seasonal_stats:
                f.write(f"{season}: {seasonal_stats[season]:.1f}°C\n")
    
    print("Generated: average_temp.txt")

    # ==========================================
    # Task 2: Temperature Range
    # ==========================================
    # Group by station and calculate global max and min
    station_range = {}
    for record in all_data:
        station = record['STATION_NAME']
        temp = record['Temperature']
        if station not in station_range:
            station_range[station] = {'max': temp, 'min': temp}
        else:
            station_range[station]['max'] = max(station_range[station]['max'], temp)
            station_range[station]['min'] = min(station_range[station]['min'], temp)
    
    # Calculate range for each station
    for station in station_range:
        station_range[station]['range'] = station_range[station]['max'] - station_range[station]['min']
    
    # Find largest range
    max_range_val = max(s['range'] for s in station_range.values())
    largest_range_stations = {st: info for st, info in station_range.items() if info['range'] == max_range_val}

    # Save to "largest_temp_range_station.txt"
    with open("largest_temp_range_station.txt", "w", encoding='utf-8') as f:
        for station in largest_range_stations:
            row = largest_range_stations[station]
            f.write(f"Station {station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")
            
    print("Generated: largest_temp_range_station.txt")

    # ==========================================
    # Task 3: Temperature Stability
    # ==========================================
    # Calculate standard deviation per station
    station_temps = {}
    for record in all_data:
        station = record['STATION_NAME']
        if station not in station_temps:
            station_temps[station] = []
        station_temps[station].append(record['Temperature'])
    
    station_std = {}
    for station, temps in station_temps.items():
        if len(temps) > 1:
            station_std[station] = stdev(temps)
    
    # Find min and max standard deviation
    if station_std:
        min_std_val = min(station_std.values())
        max_std_val = max(station_std.values())
        
        most_stable = {st: std for st, std in station_std.items() if std == min_std_val}
        most_variable = {st: std for st, std in station_std.items() if std == max_std_val}

        # Save to "temperature_stability_stations.txt"
        with open("temperature_stability_stations.txt", "w", encoding='utf-8') as f:
            for station in most_stable:
                f.write(f"Most Stable: Station {station}: StdDev {most_stable[station]:.1f}°C\n")
            for station in most_variable:
                f.write(f"Most Variable: Station {station}: StdDev {most_variable[station]:.1f}°C\n")

        print("Generated: temperature_stability_stations.txt")
    
    print("Analysis Complete.")

if __name__ == "__main__":
    main()