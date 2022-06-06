#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator

from airflow.providers.ssh.hooks.ssh import SSHHook


hook = SSHHook(remote_host="localhost", username="wangx")

with DAG(
    # 必要参数
    "bash_环境变量",
    start_date=pendulum.datetime(
        2022, 4, 20, 1, 1, 1, tz=pendulum.local_timezone()
    ),
    schedule_interval=None,
    # 可选常用参数
    tags=["bash", "env"],
    # max_active_runs=1,
) as dag:
    empty = BashOperator(
        task_id="task",
        bash_command="env",
    )
    not_empty = BashOperator(
        task_id="not_empty",
        bash_command="env",
        env={
            "RAMWIN": "FROM_AIRFLOW",
        }
    )
    remote = SSHOperator(
        task_id="remote",
        ssh_hook=hook,
        command="env",
    )
    remote_env = SSHOperator(
        task_id="remote_env",
        ssh_hook=hook,
        command="export RAMWIN1=FROM_REMOTE && env",  # 这个更靠谱点
        environment={  # 这个不是很靠谱， 需要ssh设置
            "RAMWIN": "FROM_REMOTE",
        }
    )
    empty >> not_empty >> remote >> remote_env
