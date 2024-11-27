bind = "127.0.0.1:8000" 
workers = 4 
timeout = 120 

# Logging configuration
accesslog = "-" 
errorlog = "-"  
access_log_format = '%(t)s %(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
