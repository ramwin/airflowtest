#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    "simplest_dag",
    start_date=datetime.datetime(2021, 1, 1, 0, 0, 0),
    tags=["test"]
) as dag:

    BashOperator(
        task_id="task",
        bash_command="date",
    )
