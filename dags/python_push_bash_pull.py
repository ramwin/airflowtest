#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
from pathlib import Path

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.models.taskinstance import TaskInstance


@task
def python_push(ti: TaskInstance=None):
    print(type(ti))
    ti.xcom_push(key="value from push", value=datetime.datetime.now().strftime("%H:%M:%S"))


@task
def python_pull(ti=None):
    print("value from pull: " + ti.xcom_pull(key="value from push"))
    print("value from pull: " + ti.xcom_pull(key="value from push", task_ids="python_push"))


@task
def change(ti=None):
    ti.xcom_push(key="value from push", value="new")


with DAG(
    Path(__file__).stem,
    start_date=pendulum.now() - datetime.timedelta(days=1),
    tags=["test"]
) as dag:
    bash_pull = BashOperator(
        task_id="bash_pull",
        # bash_command="echo {{ti.xcom_pull('value_from push')}}",  # 直接pull不行
        # bash_command="echo {{ti.xcom_pull('value_from push', task_ids='python_pull')}}",  # 加taskids也不行
        bash_command="echo {{ task_instance.xcom_pull(key='value from push', task_ids='python_push') }}",  # 加taskids也不行
        # do_xcom_push=False,
    )

    # python_push() >> python_pull() >> bash_pull
    # python_push() >> [bash_pull, python_pull()]  # 这样bash_pull拿不到结果
    python_push() >> bash_pull >> change() >> python_pull()
