from dagster import AssetExecutionContext, Config
from dagster_dbt import DbtCliResource, dbt_assets


from .project import jaffle_shop_project

class MyDbtConfig(Config):
    exclude_stg_models: bool

@dbt_assets(manifest=jaffle_shop_project.manifest_path)
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource,  config: MyDbtConfig):
    dbt_build_args = ["build"]
    if config.exclude_stg_models:
        dbt_build_args += ["--exclude", "jaffle_shop.staging.stg_*"]

    yield from dbt.cli(dbt_build_args, context=context).stream()
