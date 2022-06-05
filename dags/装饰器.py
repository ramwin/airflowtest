#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


@task
def python_call():
    logging.info("调用python")


with DAG(
    # 必要参数
    "test_decorators",
    start_date=pendulum.datetime(
        2022, 4, 20, 1, 1, 1, tz=pendulum.local_timezone()
    ),
    # 可选常用参数
    tags=["test"],
    # max_active_runs=1,
) as dag:
    start = BashOperator(
        task_id="task",
        bash_command="date",
    )
    start >> python_call()
