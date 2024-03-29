#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    # 必要参数
    "每小时运行一次",
    start_date=pendulum.now() - datetime.timedelta(days=1),
    # schedule=timedelta(hours=1),
    schedule="1 * * * *",
    # 可选常用参数
    tags=["test"],
    max_active_runs=1,
) as dag:
    bash1 = BashOperator(
        task_id="daily_date",
        bash_command="date",
    )
    bash2 = BashOperator(
        task_id="daily_node",
        bash_command="node -v",
    )
    bash1 >> bash2
