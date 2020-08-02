#!/bin/bash

source constants.sh

python namesremoval.py $STATS_DIR/$NEWS.$DATE.orig_changelist $STATS_DIR/$NEWS.$DATE.nounprob $STATS_DIR/$NEWS.$DATE.name_pruned_changelist -percentile 75 -topk 250
