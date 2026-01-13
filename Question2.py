import argparse
import csv
import sys
from pathlib import Path
from statistics import mean, stdev


#    Constants for file processing
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

def load_temperature_data(folder_path: Path):
    
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
    main()