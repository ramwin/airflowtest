# aitflowtest
* 不支持循环，只支持单向

## [装饰器](./dags/装饰器.md)

## DAG
```
import pendulum
from airflow import DAG
with DAG(
    # 必要参数
    "simplest_dag",
    start_date=pendulum.datetime(
        2022, 4, 20, 1, 1, 1, tz=pendulum.local_timezone()
    ),
    schedule_interval=None,
    # 可选常用参数
    tags=["test"],
    # max_active_runs=1,
    params={
        "taskid": 0,  # 触发的时候设置，所有task复制后使用, 互不影响
    },
) as dag:
    BashOperator(
        task_id="task",
        bash_command="date",
    )
```

## Operators
* [TriggerDagRunOperator][trigger-dag-run-operator]
```
from airflow.operators.trigger_dagrun import TriggerDagRunLink, TriggerDagRunOperator  # noqa
TriggerDagRunOperator(
    trigger_dag_id=,,
    conf={},  # 配置参数
)
```


[trigger-dag-run-operator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/trigger_dagrun/index.html#airflow.operators.trigger_dagrun.TriggerDagRunOperator)
