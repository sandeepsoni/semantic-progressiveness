#!/bin/bash

source constants.sh

python progressiveness.py $MODELS_DIR/$DBLP.$LIM.early.model $MODELS_DIR/$DBLP.$LIM.later.model $STATS_DIR/$DBLP.pruned_changelist $STATS_DIR/$DBLP.tokens $STATS_DIR/$DBLP.scores
