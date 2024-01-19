#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

import datetime
from pathlib import Path

import pendulum
import random

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


@task(depends_on_past=True)
def random_fail(ti=None):
    if random.random() > 0.5:
        raise ValueError("error")


with DAG(
    "test_error_true",
    start_date=pendulum.now()-datetime.timedelta(minutes=5),
    tags=["test"],
    max_active_runs=4,
    schedule_interval="* * * * *",
) as dag:
    bash1 = BashOperator(
        task_id="task1",
        bash_command=r"date  +%Y-%m-%d\ %H:%M:%S",
        depends_on_past=True,
    )
    bash2 = BashOperator(
        task_id="task2",
        bash_command=r"date  +%Y-%m-%d\ %H:%M:%S",
        depends_on_past=True,
    )
    bash3 = BashOperator(
        task_id="task3",
        bash_command=r"date  +%Y-%m-%d\ %H:%M:%S",
        depends_on_past=True,
    )
    bash1 >> random_fail() >> bash2 >> bash3
