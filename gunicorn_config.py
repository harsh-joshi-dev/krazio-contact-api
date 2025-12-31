# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
# Use 1 worker for free tier, 2 for paid tier
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # Increased timeout for slow startups (5 minutes)
graceful_timeout = 120
keepalive = 5
preload_app = False  # Don't preload to avoid startup issues

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'krazio-email-api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
# keyfile = None
# certfile = None

