<<<<<<< HEAD
import argparse
import csv
import sys
from pathlib import Path
from statistics import mean, stdev
from typing import List, Dict, Any, Tuple, Optional

# Constants for file processing
MONTH_COLUMNS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

SEASON_MAP = {
    'December': 'Summer', 'January': 'Summer', 'February': 'Summer',
    'March': 'Autumn', 'April': 'Autumn', 'May': 'Autumn',
    'June': 'Winter', 'July': 'Winter', 'August': 'Winter',
    'September': 'Spring', 'October': 'Spring', 'November': 'Spring'
}

def load_temperature_data(folder_path: Path) -> List[Dict[str, Any]]:
    
    """ It reads and aggregates temperature data from all CSV files in a specified directory.

    Iterates through every .csv file in the target folder, parsing valid temperature
    readings while ignoring missing or malformed values.

    Args:
        folder_path (Path): The file system path to the directory containing CSV files.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents 
        a valid temperature record containing:
            - 'STATION_NAME' (str): The name of the weather station.
            - 'Month' (str): The month of the recording.
            - 'Temperature' (float): The recorded temperature value.
            - 'Season' (str): The Australian season corresponding to the month.  """

    all_records = []
    csv_files = sorted(folder_path.glob("*.csv"))

    if not csv_files:
        print(f"Warning: No .csv files found in '{folder_path}'.")
        return []

    print(f"Processing {len(csv_files)} files from {folder_path}...")

    for file_path in csv_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                # To identify which month columns exist in this specific CSV
                available_months = [col for col in MONTH_COLUMNS if col in headers]

                if not available_months:
                    continue

                for row in reader:
                    station_name = row.get('STATION_NAME', 'Unknown')
                    
                    for month in available_months:
                        temp_str = row.get(month, '')
                        # To parse temperature if valid number
                        if temp_str and temp_str.strip():
                            try:
                                temp_val = float(temp_str)
                                all_records.append({
                                    'STATION_NAME': station_name,
                                    'Month': month,
                                    'Temperature': temp_val,
                                    'Season': SEASON_MAP.get(month, 'Unknown')
                                })
                            except ValueError:
                                # To ignore non-numeric values (NaN/corrupt data)
                                pass
        except Exception as e:
            print(f"Error processing file {file_path.name}: {e}")
            
    return all_records

def calculate_seasonal_averages(data: List[Dict[str, Any]], output_file: str) -> None:
    
    """ Calculates the mean temperature for each season and writes the result to a file.

    Aggregates data across all stations and years to determine a global average 
    for Summer, Autumn, Winter, and Spring.

    Args:
        data (List[Dict[str, Any]]): The loaded temperature data records.
        output_file (str): The filename to write the results to. """
    
    seasonal_temps = {}
    
    # For grouping temperatures by season
    for record in data:
        season = record['Season']
        if season not in seasonal_temps:
            seasonal_temps[season] = []
        seasonal_temps[season].append(record['Temperature'])

    # For calculating means
    seasonal_means = {s: mean(temps) for s, temps in seasonal_temps.items()}

    # To write to file in standard order
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
                if season in seasonal_means:
                    f.write(f"{season}: {seasonal_means[season]:.1f}°C\n")
        print(f"Generated: {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

def find_largest_temperature_range(data: List[Dict[str, Any]], output_file: str) -> None:
    
    """    Identifies station(s) with the maximum temperature range and writes the result to a file.

    The range is defined as the difference between the absolute maximum and absolute minimum 
    temperature recorded at a specific station.

    Args:
        data (List[Dict[str, Any]]): The loaded temperature data records.
        output_file (str): The filename to write the results to.    """
    
    # map: station_name -> {'min': float, 'max': float}
    station_extremes = {}

    for record in data:
        station = record['STATION_NAME']
        temp = record['Temperature']
        
        if station not in station_extremes:
            station_extremes[station] = {'min': temp, 'max': temp}
        else:
            if temp < station_extremes[station]['min']:
                station_extremes[station]['min'] = temp
            if temp > station_extremes[station]['max']:
                station_extremes[station]['max'] = temp

    # To calculate ranges
    results = []
    max_range_val = -1.0

    for station, stats in station_extremes.items():
        temp_range = stats['max'] - stats['min']
        if temp_range > max_range_val:
            max_range_val = temp_range
        
        results.append({
            'station': station,
            'range': temp_range,
            'max': stats['max'],
            'min': stats['min']
        })

    # Removeing all stations that do not match max range (to handle ties)
    top_stations = [r for r in results if abs(r['range'] - max_range_val) < 0.001]

    try:
        with open(output_file, "w", encoding='utf-8') as f:
            for item in top_stations:
                f.write(f"{item['station']}: Range {item['range']:.1f}°C "
                        f"(Max: {item['max']:.1f}°C, Min: {item['min']:.1f}°C)\n")
        print(f"Generated: {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

def analyze_temperature_stability(data: List[Dict[str, Any]], output_file: str) -> None:
    
    """     Analyzes temperature stability using standard deviation and writes the result to a file.

    Identifies the most stable (lowest std dev) and most variable (highest std dev) 
    stations. Requires at least two data points per station to calculate deviation.

    Args:
        data (List[Dict[str, Any]]): The loaded temperature data records.
        output_file (str): The filename to write the results to.    """
    
    # Grouping temperatures by station
    station_temps = {}
    for record in data:
        station = record['STATION_NAME']
        if station not in station_temps:
            station_temps[station] = []
        station_temps[station].append(record['Temperature'])

    # To calculate Standard Deviations
    station_stds = {}
    for station, temps in station_temps.items():
        if len(temps) > 1:
            station_stds[station] = stdev(temps)

    if not station_stds:
        print("Insufficient data to calculate stability (need >1 record per station).")
        return

    min_std = min(station_stds.values())
    max_std = max(station_stds.values())

    # To find the most stable and most variable stations
    most_stable = [s for s, v in station_stds.items() if abs(v - min_std) < 0.001]
    most_variable = [s for s, v in station_stds.items() if abs(v - max_std) < 0.001]

    try:
        with open(output_file, "w", encoding='utf-8') as f:
            for s in most_stable:
                f.write(f"Most Stable: {s}: StdDev {station_stds[s]:.1f}°C\n")
            for s in most_variable:
                f.write(f"Most Variable: {s}: StdDev {station_stds[s]:.1f}°C\n")
        print(f"Generated: {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

def main() -> None:
    
    """     Main entry point for the Weather Analysis Application.

    Parses command-line arguments to locate the data directory, validates the input,
    and orchestrates the data loading and analysis tasks.    """
      
        # Argument Parsing
    parser = argparse.ArgumentParser(description="Analyze Australian weather station data.")
    parser.add_argument('data_dir', nargs='?', default=None, 
                        help='Path to the folder containing "temperatures" CSV files.')
    args = parser.parse_args()

    # Determining folder's path
    if args.data_dir:
        folder_path = Path(args.data_dir).expanduser()
    else:
        folder_path = Path(__file__).parent / "temperatures"

    # Validate folder existence
    if not folder_path.exists():
        print(f"Error: The folder '{folder_path}' does not exist.")
        print("Please ensure a 'temperatures' folder exists in the script directory or provide a path.")
        sys.exit(1)

    # Executing Logic
    data = load_temperature_data(folder_path)

    if not data:
        print("No valid temperature data found. Exiting.")
        sys.exit(1)

    # TO perform output tasks
    calculate_seasonal_averages(data, "average_temp.txt")
    find_largest_temperature_range(data, "largest_temp_range_station.txt")
    analyze_temperature_stability(data, "temperature_stability_stations.txt")

    print("\nAnalysis Complete.")

if __name__ == "__main__":
=======
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
>>>>>>> 852cebb86b1c1d7e398d79059b9b80b8c92ca94e
    main()