#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    Path(__file__).stem,
    start_date=datetime.datetime(2021, 1, 1, 0, 0, 0),
    tags=["test"]
) as dag:

    bash_push = BashOperator(
        task_id="bash_push",
        bash_command=r"date && echo $HOSTNAME && echo -e '123\n345'",
    )
    bash_pull = BashOperator(
        task_id="bash_pull",
        bash_command=f"echo {bash_push.output}",  # 用 fstring可以的到output, 但是只能得到最后的输出
        do_xcom_push=False,
    )
    bash_push >> bash_pull
