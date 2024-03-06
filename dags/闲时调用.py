#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime

import pendulum
import psutil

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator


with DAG(
        "闲时调用",
        start_date=pendulum.now() - datetime.timedelta(hours=1)
) as dag:

    def check_cpu():
        cpu_percent = psutil.cpu_percent()
        if cpu_percent > 80:
            print("CPU占用过高", cpu_percent)
            return False
        print("CPU占用不高", cpu_percent)
        return True

    check_cpu_task = ShortCircuitOperator(
            task_id="check_cpu",
            python_callable=check_cpu,
    )
    final = BashOperator(task_id="final", bash_command="date")
    check_cpu_task >> final
