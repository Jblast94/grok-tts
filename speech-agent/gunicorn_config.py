bind = "0.0.0.0:8000"
workers = 4  # Increased for production
threads = 4
worker_class = "sync"
timeout = 120
keepalive = 5
accesslog = "/var/log/gunicorn-access.log"
errorlog = "/var/log/gunicorn-error.log"
loglevel = "info"
