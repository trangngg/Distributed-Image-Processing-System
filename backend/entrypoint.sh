#!/bin/sh
# 1) Start master-server
MASTER_PORT=${MASTER_PORT:-5003}
export MASTER_PORT
python master_server.py &

# 2) Spin workers
for i in $(seq 1 $NUM_WORKERS); do
  python worker_client.py &
done

# 3) Start Flask on FLASK_PORT (5006)
export FLASK_PORT=${FLASK_PORT:-5006}
python app.py
