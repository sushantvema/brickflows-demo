from datetime import timedelta
from brickflow import (
    Workflow, 
    Cluster, 
    WorkflowPermissions, 
    User, 
    TaskType,
    TaskSettings, 
    # EmailNotifications, 
    PypiTaskLibrary, 
    # MavenTaskLibrary, 
    # JobsParameters, 
    ctx,
    BrickflowTriggerRule, 
    SparkPythonTask
)

# from brickflow_plugins import BashOperator

DEMO_EMAIL = "svema@influential.co"

wf = Workflow(  
    "demo_workflow",  
    default_cluster=Cluster.from_existing_cluster("0528-193256-wffsknlq"),  

    # Optional parameters below
    schedule_quartz_expression="0 0/20 0 ? * * *",  
    timezone="UTC",  
    schedule_pause_status="PAUSED",  
    # TODO: Figure out the new API for this object
    # default_task_settings=TaskSettings(  
    #         email_notifications=EmailNotifications(
    #         on_start=[DEMO_EMAIL],
    #         on_success=[DEMO_EMAIL],
    #         on_failure=[DEMO_EMAIL],
    #         on_duration_warning_threshold_exceeded=[DEMO_EMAIL]
    #      ),
    #      timeout_seconds=timedelta(hours=2).seconds
    #),
    # libraries=[  
    #     PypiTaskLibrary(package="requests"),
    #     MavenTaskLibrary(coordinates="com.cronutils:cron-utils:9.2.0"),
    # ],
    tags={  
        "product_id": "brickflow_demo",
        "slack_channel": "as-assisted-search"
    },
    max_concurrent_runs=1,
    # permissions=WorkflowPermissions(  
    #     can_manage_run=[User(DEMO_EMAIL)],
    #     can_view=[User(DEMO_EMAIL)],
    #     can_manage=[User(DEMO_EMAIL)],
    # ),
    prefix="feature-",  
    suffix="_dev1",  
    common_task_parameters={  
        "catalog": "dev",
        "schema": "bronze_mariadb_social_hoarder"
    },
    # TODO: Broken health field
    # health = { 
    #     "metric": "RUN_DURATION_SECONDS",
    #     "op": "GREATER_THAN",
    #     "value": 7200
    # },
    # parameters=[JobsParameters(default="INFO", name="jp_logging_level")],  
)


@wf.task()  
def demo_start_task(*, test="test"):
    print(f"This is a configuration variables called {test}")
    return "hello world"

@wf.task(depends_on=demo_start_task, task_type=TaskType.SPARK_PYTHON_TASK, libraries=[
            PypiTaskLibrary(
                package="pytz"
            )
        ]
) 
def datetime_task():
    return SparkPythonTask(
        python_file="./scripts/get_current_datetime.py",
        source="GIT",
        # parameters=["--param1", "World!"],
    )

@wf.task(depends_on=datetime_task)
def test_table_ingest():
    # ctx.spark.sql(
    #     f"""
    #     CREATE TABLE IF NOT EXISTS 
    #     {ctx.dbutils_widget_get_or_else(key="catalog", debug="development")}.\
    #     {ctx.dbutils_widget_get_or_else(key="database", debug="dummy_database")}.\
    #     {ctx.dbutils_widget_get_or_else(key="brickflow_env", debug="local")}_lending_data_ingest
    #     USING DELTA -- this is default just for explicit purpose
    #     SELECT * FROM parquet.`dbfs:/databricks-datasets/samples/lending_club/parquet/`
    # """
    
    # TODO: ctx.dbutils_widget_get_or_else is a deprecated function?
    # sdf = ctx.spark.sql(
    #    f"""
    #    SELECT * FROM 
    #         {ctx.dbutils_widget_get_or_else(key="catalog", debug="debug")}. \
    #         {ctx.dbutils_widget_get_or_else(key="schema", debug="debug")}. \
    #         cippus_text
    #    USING DELTA -- this is default just for explicit purposes
    #    LIMIT 10
    #    """
    # )
    sdf = ctx.spark.sql(
       f"""
       SELECT * FROM 
            {ctx.dbutils.widgets.get("catalog")}. \
            {ctx.dbutils.widgets.get("schema")}. \
            cippus_text
       LIMIT 10
       """
    )
    print(sdf.count()) 
    return sdf.count()

@wf.task(depends_on=test_table_ingest, trigger_rule=BrickflowTriggerRule.ALL_SUCCESS)
def all_success_task():
    print("Everything went well!")
    pass
