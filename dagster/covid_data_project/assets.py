import dlt
from dlt.destinations import postgres
import pandas as pd
from dagster import asset
import os
import requests
from datetime import datetime

@asset
def raw_csse_covid_19_daily_reports_us():
    """
    Dagster asset that loads all COVID-19 daily report CSVs from GitHub
    into a PostgreSQL database using pandas and dlt.
    """
    # Fetch list of CSV files from GitHub API
    api_url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports_us'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    files = response.json()

    # Collect and sort CSV files by date
    csv_files = []
    for file in files:
        name = file['name']
        if name.endswith('.csv'):
            date_str = name[:-4]  # Remove .csv extension
            try:
                file_date = datetime.strptime(date_str, '%m-%d-%Y').date()
                csv_files.append({
                    'url': file['download_url'],
                    'date': file_date,
                    'name': name
                })
            except ValueError:
                continue  # Skip files with invalid date formats

    # Sort files chronologically
    csv_files.sort(key=lambda x: x['date'])

    # Load and combine all CSV data
    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file['url'])
            df['report_date'] = csv_file['date']
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {csv_file['name']}: {str(e)}")
            continue

    if not dfs:
        raise ValueError("No valid CSV data could be loaded")

    combined_df = pd.concat(dfs, ignore_index=True)

    # Configure dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name='covid_daily_to_postgres_us',
        destination=postgres(
            f"postgresql://{os.environ['DBT_POSTGRES_USER']}:{os.environ['DBT_POSTGRES_PASSWORD']}"
            f"@{os.environ['DBT_POSTGRES_HOST']}:5432/{os.environ['DBT_POSTGRES_DB']}"
        ),
        dataset_name='dlt_raw'
    )

    # Load data to PostgreSQL
    load_info = pipeline.run(
        data=combined_df,
        table_name='csse_covid_19_daily_reports_us',
        write_disposition="replace"
    )

    print(f"Loaded {len(combined_df)} records")
    return load_info


@asset
def raw_csse_covid_19_daily_reports():
    """
    Dagster asset that loads all COVID-19 daily report CSVs from GitHub
    into a PostgreSQL database using pandas and dlt.
    """
    # Fetch list of CSV files from GitHub API
    api_url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    files = response.json()

    # Collect and sort CSV files by date
    csv_files = []
    for file in files:
        name = file['name']
        if name.endswith('.csv'):
            date_str = name[:-4]  # Remove .csv extension
            try:
                file_date = datetime.strptime(date_str, '%m-%d-%Y').date()
                csv_files.append({
                    'url': file['download_url'],
                    'date': file_date,
                    'name': name
                })
            except ValueError:
                continue  # Skip files with invalid date formats

    # Sort files chronologically
    csv_files.sort(key=lambda x: x['date'])

    # Load and combine all CSV data
    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file['url'])
            
            # Standardize column names
            column_mapping = {
                'Province/State': 'Province_State',
                'Country/Region': 'Country_Region',
                'Last Update': 'Last_Update',
                'Latitude': 'Lat',
                'Longitude': 'Long_',
                'Case-Fatality_Ratio': 'Case_Fatality_Ratio',
                'Incidence_Rate': 'Incident_Rate'
            }
            
            # Rename columns if they exist
            df = df.rename(columns=column_mapping)
            
            # Ensure consistent columns (fill missing ones with None)
            required_columns = [
                'Province_State',
                'Country_Region',
                'Last_Update',
                'Lat',
                'Long_',
                'Confirmed',
                'Deaths',
                'Recovered',
                'Active',
                'Combined_Key'
            ]
            
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
                    
            # Add report date
            df['report_date'] = csv_file['date']
            
            # Select only the columns we want, in a specific order
            df = df[required_columns + ['report_date']]
            
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {csv_file['name']}: {str(e)}")
            continue

    if not dfs:
        raise ValueError("No valid CSV data could be loaded")

    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)

    # Configure dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name='covid_daily_to_postgres',
        destination=postgres(
            f"postgresql://{os.environ['DBT_POSTGRES_USER']}:{os.environ['DBT_POSTGRES_PASSWORD']}"
            f"@{os.environ['DBT_POSTGRES_HOST']}:5432/{os.environ['DBT_POSTGRES_DB']}"
        ),
        dataset_name='dlt_raw'
    )

    # Load data to PostgreSQL
    load_info = pipeline.run(
        data=combined_df,
        table_name='csse_covid_19_daily_reports',  # Changed table name to distinguish from US reports
        write_disposition="replace"
    )

    print(f"Loaded {len(combined_df)} records")
    return load_info