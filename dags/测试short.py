#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import pendulum
import random

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator


def check():
    if random.random() >= 0.5:
        return False
    return True


with DAG(
    # 必要参数
    "测试短路",
    start_date=pendulum.datetime(
        2022, 4, 20, 1, 1, 1,
        tz=pendulum.local_timezone()
    ),
) as dag:
    first = ShortCircuitOperator(
        task_id="first",
        python_callable=check,
    )
    parrel = BashOperator(
        task_id="parrel",
        bash_command="date && sleep 10 && date",
    )
    final = BashOperator(
        task_id="final",
        bash_command="date",
    )
    [first, parrel] >> final
