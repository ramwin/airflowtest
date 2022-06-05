#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import random

import pendulum

from airflow import DAG
from airflow.decorators import branch_task, task
from airflow.operators.bash import BashOperator


@branch_task
def random_task():
    if random.random() > 0.5:
        return "up"
    return "down"


@task
def up():
    logging.info("up")


@task
def down():
    logging.info("down")


with DAG(
    # 必要参数
    "test_loop",
    start_date=pendulum.datetime(
        2022, 5, 20, 1, 1, 1, tz=pendulum.local_timezone()
    ),
    # 可选常用参数
    tags=["test"],
    # max_active_runs=1,
) as dag:
    a = random_task()
    d = down()
    a >> [up(), d]
    # d >> a 不支持
