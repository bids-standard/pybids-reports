#!/bin/bash

rc=0;
for pre in  asl ds00 eeg meg ieeg pet; do
    for i in $(find tools/bids-examples -maxdepth 1 -type d -name "${pre}*"); do
        if [ "$i" == "bids-examples" ]; then
            continue
        fi
        echo
        echo "running on dataset" $i
        CMD="pybids_reports ${i%%/} ${PWD} --verbosity 0"
        echo "$CMD"
        $CMD || rc=$?
    done
done
exit $rc;
