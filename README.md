# aitflowtest
* 不支持循环，只支持单向

## 测试
```
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db
export AIRFLOW_HOME=$PWD & airflow webserver
export AIRFLOW_HOME=$PWD & airflow schedular
```

## 安装

```bash
pip install apache-airflow
pip install 'flask-session<0.6'
pip3 install apache-airflow-providers-ssh
airflow db migrate
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
airflow webserver --port 8080
airflow scheduler
```


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

### 属性
* `start_date`
务必设置成一两天前，因为如果时now的话，airflow会不断地重新载入dag.py文件从而导致每次检查时发现start_date都是在以后

* `schedule_interval=""`
可以输入timedelta或者直接输入contab的规则  
timedelta(seconds=60)  "*/6 * * * *"  # 注意这个是按照utc时间来的  
执行任务的时候，execution_date是上一次crontab的时间. 比如今天执行，那么execution_date就是昨天  


    * * * * * 会导致36分的时候，执行35分的任务
    47 * * * * 会导致今天47分的时候执行 1小时前47分的任务
    31 6 * * * 会导致今天14:31时执行昨天14:31的任务

## Operators
* [TriggerDagRunOperator][trigger-dag-run-operator]
```
from airflow.operators.trigger_dagrun import TriggerDagRunLink, TriggerDagRunOperator  # noqa
TriggerDagRunOperator(
    trigger_dag_id=,,
    conf={},  # 配置参数
)
```

#### ExternalTaskSensor
默认情况下，如果一个dag依赖了其他的dag，会找`executiong_date`一致的dag，看他是否成功。

    ExternalTaskSensor(
        external_dag_id="run_python",
        external_task_id="taask1",
        timeout=160
    )


[trigger-dag-run-operator]: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/trigger_dagrun/index.html#airflow.operators.trigger_dagrun.TriggerDagRunOperator

## 设置数据库
```
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
-- PostgreSQL 15 requires additional privileges:
USE airflow_db;
GRANT ALL ON SCHEMA public TO airflow_user;
```

## 配置
* [dag_dir_list_interval](https://airflow.apache.org/docs/apache-airflow/2.8.1/configurations-ref.html#dag-dir-list-interval)
多少秒刷新一次
