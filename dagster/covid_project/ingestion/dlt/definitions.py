import dagster as dg


@dg.asset
def ingestion_asset() -> None: ...

ingestion_assets = [ingestion_asset]