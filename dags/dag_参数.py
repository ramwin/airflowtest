#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


with DAG(
    # 必要参数
    "dag_params",
    start_date=pendulum.datetime(
        2022, 4, 20, 1, 1, 1, tz=pendulum.local_timezone()
    ),
    # 可选常用参数
    tags=["test", "params"],
    # max_active_runs=1,
    params={
        "taskid": 0,
    },
    schedule_interval=None,
) as dag:
    simple_output = BashOperator(
        task_id="task",
        bash_command="echo '任务id: {{params['taskid']}}'",
    )

    @task
    def change(*args, **kwargs):
        print(kwargs["params"])
        kwargs["params"]["taskid"] += 3
        print(kwargs["params"])

    simple_output2 = BashOperator(
        task_id="simple_output2",
        bash_command="echo '任务id: {{params['taskid']}}'",
    )

    simple_output >> change() >> simple_output2
