# dagster/covid_data_project/definitions.py

from dagster import Definitions, load_assets_from_modules, op, job, In, Nothing, asset
import assets
import os
import subprocess

# Get the current directory where definitions.py is located
CURRENT_DIR = os.path.dirname(__file__)
DBT_PROJECT_DIR = os.path.join(CURRENT_DIR, "dbt_project")

@op(ins={"us_data": In(Nothing), "global_data": In(Nothing)})
def wait_for_source_data(context):
    """
    This op ensures that the source data assets are materialized
    before proceeding with dbt operations.
    """
    context.log.info("Source data assets have been materialized")

@op(ins={"wait_for_source_data": In(Nothing)})
def dbt_deps(context):
    """
    Run dbt deps to install dependencies.
    """
    context.log.info("Starting dbt deps...")
    result = subprocess.run(
        ["dbt", "deps"], 
        cwd=DBT_PROJECT_DIR, 
        check=True,
        env={**os.environ, "DBT_PROFILES_DIR": DBT_PROJECT_DIR},
        capture_output=True,
        text=True
    )
    context.log.info(result.stdout)

@op(ins={"wait_for_deps": In(Nothing)})
def dbt_run(context):
    """
    Run dbt models.
    """
    context.log.info("Starting dbt run...")
    result = subprocess.run(
        ["dbt", "run"], 
        cwd=DBT_PROJECT_DIR, 
        check=True,
        env={**os.environ, "DBT_PROFILES_DIR": DBT_PROJECT_DIR},
        capture_output=True,
        text=True
    )
    context.log.info(result.stdout)

@job
def covid_etl():
    """
    Job that runs the complete ETL pipeline:
    1. Load both US and global COVID data assets
    2. Wait for materialization to complete
    3. Run dbt deps
    4. Run dbt models
    """
    us_data = assets.raw_csse_covid_19_daily_reports_us()
    global_data = assets.raw_csse_covid_19_daily_reports()
    
    wait = wait_for_source_data(us_data=us_data, global_data=global_data)
    # Pass the output to both dbt_deps and dbt_run
    wait_deps = dbt_deps(wait_for_source_data=wait)
    dbt_run(wait_for_deps=wait_deps)

# Load all assets
all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[covid_etl]
)