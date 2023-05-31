#!/bin/bash

rc=0;
for pre in asl ds00; do
    for i in $(find bids-examples -maxdepth 1 -type d -name "${pre}*"); do
        if [ "$i" == "bids-examples" ]; then
            continue
        fi
        echo "running on dataset" $i
        CMD="pybids_reports ${i%%/} ${PWD}"
        echo "$CMD"
        $CMD || rc=$?
    done
done
exit $rc;
