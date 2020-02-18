#!/usr/bin/env bash

N="${STATICE_NUM_WORKERS:-1}"

for i in `seq 1 $N`
do
    # Use current unix time as random name.
    flask rq worker --name "worker_$(date +%s%N)" &
done

wait
