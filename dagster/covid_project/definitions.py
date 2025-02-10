from dagster import Definitions
from ingestion.dlt.definitions import dlt_assets
from transformation.dbt.definitions import dbt_assets
from transformation.adhoc.definitions import adhoc_assets

all_assets = dlt_assets + dbt_assets + adhoc_assets

definitions = Definitions(assets=all_assets)
