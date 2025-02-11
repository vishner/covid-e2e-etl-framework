# dagster/covid_data_project/definitions.py

from dagster import Definitions, load_assets_from_modules, op, job, In, Nothing, ScheduleDefinition
import assets
import os
import subprocess

# Define the directory for the dbt project
CURRENT_DIR = os.path.dirname(__file__)
DBT_PROJECT_DIR = os.path.join(CURRENT_DIR, "dbt_project")

@op(ins={"us_data": In(Nothing), "global_data": In(Nothing)})
def wait_for_source_data(context):
    """
    Op to ensure that source data assets are materialized before proceeding.
    """
    context.log.info("Source data assets have been materialized")

@op(ins={"wait_for_source_data": In(Nothing)})
def dbt_deps(context):
    """
    Op to run dbt deps to install dependencies.
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
    Op to run dbt models.
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
    Job to run the complete ETL pipeline:
    1. Load US and global COVID data assets
    2. Wait for materialization to complete
    3. Run dbt deps
    4. Run dbt models
    """
    us_data = assets.raw_csse_covid_19_daily_reports_us()
    global_data = assets.raw_csse_covid_19_daily_reports()
    
    wait = wait_for_source_data(us_data=us_data, global_data=global_data)
    wait_deps = dbt_deps(wait_for_source_data=wait)
    dbt_run(wait_for_deps=wait_deps)

# Define a daily schedule for the ETL job
daily_schedule = ScheduleDefinition(
    job=covid_etl,
    cron_schedule="0 0 * * *",  # Runs daily at midnight UTC
    execution_timezone="UTC"
)

# Load all assets and define the Dagster definitions
all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[covid_etl],
    schedules=[daily_schedule]
)