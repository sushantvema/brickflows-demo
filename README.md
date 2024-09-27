# Databricks x Brick Flows Demo

## Features to Show:
  - [x] Dependent tasks
  - [x] Trigger rules, and tasks-conditional logic (included ALL_SUCCESS)
  - [x] cron scheduling
  - [] User permissions + notifications
  - [X] SQL tasks
  - [] Custom cluster configuration in code for any task
  - [] If else, conditional logic
  - [] "Airflow operators"
  - [] notebook task -> can run a specific notebook, similar to dbutils.run() API
  - [] Run Job Task -> run a toy job with specified parameters
  - [] Python Task
  - [] inbuilt task parameters (useful for logging)
  - [] custom prefix and suffix -> synergize with naming conventions
  - [] workflow dependency sensor -> poll and wait for another deployed workflow to finish
  - [] workflow task dependency sensor -> poll and wait for a specific task in another workflow to finish before launching.

## Scope of Friday Sept 27th Demo  
- Notebook task with ETL process
- All task success -> reconciliation talking about data quality. Spark expectations. Or sql task at the end

### Sushant, Sagar, Cyrus Checkin 2024-09-26T15:00:00
- Sushant put together the monorepo of multiple projects with an example project of one workflow called demo_workflow.
- Sushant was able to successfully deploy a workflow using the General Purpose Cluster
- Notebooks as github scripts and jobs/clusters generated around

### Example ETL Process Design
- All tasks in one cluster
- Create some workflow level parameters which all of the tasks can inherit.
  - catalog, schema of dev application
- first use SQL task to check if a table exists. If it doesn't exist, create it with a certain schema. 
- Generate sample data according to this table schema
- Add it to the table

## Scope of Monday Sept 30th Demo
- Think about how this gets integrated with CI/CD. This is good to show local development, think 
- Environment -. pipeline -> reconciliation -> integration tests, etc

## Development Process  
- standard monorepo development process
- everyone needs databricks cli with admin permissions
- feature branches per workflow per project?

