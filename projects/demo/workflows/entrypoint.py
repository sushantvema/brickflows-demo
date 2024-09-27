# Databricks notebook source

from brickflow import Project, PypiTaskLibrary, MavenTaskLibrary  # make sure brickflow imports are at the top

import workflows

def main() -> None:
    """Project entrypoint"""
    with Project(
        "demo",
        git_repo="https://github.com/sushantvema/brickflows-demo",
        provider="github",
        libraries=[
            MavenTaskLibrary(coordinates="com.cronutils:cron-utils:9.2.0"),
            # PypiTaskLibrary(package="spark-expectations==0.5.0"), # Uncomment if spark-expectations is needed
        ],
        enable_plugins=True
    ) as f:
        f.add_pkg(workflows)


if __name__ == "__main__":
    main()
