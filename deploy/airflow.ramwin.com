server {
    listen 80;
    server_name airflow.ramwin.com;
    location / {
        proxy_pass http://127.0.0.1:8080/;
    }
}
