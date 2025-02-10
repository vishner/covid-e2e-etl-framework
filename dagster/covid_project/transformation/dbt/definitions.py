import dagster as dg


@dg.asset
def dbt_asset() -> None: ...

dbt_assets = [dbt_asset]