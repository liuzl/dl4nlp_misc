config_file=buddha.json gunicorn -w 2 -b 0.0.0.0:6700 gserver:app
