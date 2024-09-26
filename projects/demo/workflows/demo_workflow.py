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
    BrickflowTriggerRule
)

# from brickflow_plugins import BashOperator

DEMO_EMAIL = "svema@influential.co"

wf = Workflow(  
    "demo_workflow",  
    default_cluster=Cluster.from_existing_cluster("0528-193256-wffsknlq"),  

    # Optional parameters below
    schedule_quartz_expression="0 0/20 0 ? * * *",  
    timezone="UTC",  
    # schedule_pause_status="PAUSED",  
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
    # tags={  
    #     "product_id": "brickflow_demo",
    #     "slack_channel": "nike-sole-brickflow-support"
    # },
    max_concurrent_runs=1,
    # permissions=WorkflowPermissions(  
    #     can_manage_run=[User(DEMO_EMAIL)],
    #     can_view=[User(DEMO_EMAIL)],
    #     can_manage=[User(DEMO_EMAIL)],
    # ),
    # prefix="feature-demo",  
    # suffix="_dev1",  
    # common_task_parameters={  
    #     "catalog": "development",
    #     "database": "your_database"
    # },
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

@wf.task(depends_on=demo_start_task)  
def demo_dependent_task_1():
    return "It's-a me, mario."

# @wf.task
# def bash_task(depends_on=demo_dependent_task_1):
#     return BashOperator(task_id=bash_task.__name__, 
#                         bash_command="ls -ltr")

@wf.task(trigger_rule=BrickflowTriggerRule.ALL_SUCCESS)
def all_success_task():
    print("Everything went well!")
    pass
