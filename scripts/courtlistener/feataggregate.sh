#!/bin/bash

source constants.sh

FEATS_TYPE=feats_manual

python -u feataggregate.py $STATS_DIR $STATS_DIR/$OPS.$FEATS_TYPE.complete -docid $OPS.list -indeg $OPS.ind -outdeg $OPS.outd -year $OPS.dates -nuniqs $OPS.nuniqs -ntokens $OPS.ntokens -bows $OPS.bowscores -sems $OPS.1K.$FEATS_TYPE.semscores
