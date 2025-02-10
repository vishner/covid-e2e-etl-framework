import dagster as dg


@dg.asset
def adhoc_asset() -> None: ...

adhoc_assets = [adhoc_asset]