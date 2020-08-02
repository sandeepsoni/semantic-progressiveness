#!/bin/bash

source constants.sh

python postpruning.py $STATS_DIR $DBLP.$LIM.early.casestats $DBLP.$LIM.later.casestats $DBLP.$LIM.besttag $DBLP.orig_changelist $DBLP.pruned_changelist
