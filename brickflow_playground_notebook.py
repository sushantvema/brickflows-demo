import brickflow

from datetime import timedelta
from brickflow import (
    Workflow,
    Cluster,
    WorkflowPermissions,
    User,
    TaskSettings,
    EmailNotifications,
    PypiTaskLibrary,
    MavenTaskLibrary,
    JobsParameters,
)

@wf.notebook_task
# this task runs a databricks notebook
def example_notebook(*, param_1="test"):
    print(param_1)
    return NotebookTask(
        notebook_path="/Workspace/Users/svema@influential.co/brickflows_demo/notebook1.py",
        base_parameters={
            "param_1": "test",  # in the notebook access these via dbutils.widgets.get("some_parameter")
        },
    )

@wf.task(depends_on=example_notebook)  
def bronze_layer():
    pass


wf = Workflow(
    "wf_brickflows_demo",
    default_cluster=Cluster.from_existing_cluster("0528-193256-wffsknlq"), # General Purpose Cluster
    # Optional parameters below
    # schedule_quartz_expression="0 0/20 0 ? * * *", # Example cron expression
    timezone="UTC",
    schedule_pause_status="PAUSED",
    default_task_settings=TaskSettings(
        email_notifications=EmailNotifications(
            on_start=["svema@influential.co"],
            on_success=["svema@influential.co"],
            on_failure=["svema@influential.co"],
            on_duration_warning_threshold_exceeded=["svema@influential.co"],
        ),
        timeout_seconds=timedelta(hours=1).seconds,
    ),
    libraries=[
        PypiTaskLibrary(package="requests"),
        MavenTaskLibrary(coordinates="com.cronutils:cron-utils:9.2.0"),
    ],
    tags={
        "product_id": "brickflow_demo",
         # "slack_channel": "nike-sole-brickflow-support",
    },
    max_concurrent_runs=1,
    permissions=WorkflowPermissions(
        can_manage_run=[User("svema@influential.co")],
        can_view=[User("svema@influential.co")],
        can_manage=[User("svema@influential.co")],
    ),
    prefix="feature-brickflows-demo",
    suffix="_dev1",
    common_task_parameters={"catalog": "influential"},
    health={"metric": "RUN_DURATION_SECONDS", "op": "GREATER_THAN", "value": 7200},
    # parameters=[JobsParameters(default="INFO", name="jp_logging_level")],
)


@wf.task()
def task_function(*, test="var"):
    return "hello world"


def main():
    print("Hello world.")
    return


if __name__ == "__main__":
    main()
