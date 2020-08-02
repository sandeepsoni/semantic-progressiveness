#!/bin/bash

source constants.sh

FEATS_TYPE=feats_manual

python -u feataggregate.py $STATS_DIR $STATS_DIR/$DBLP.$FEATS_TYPE.complete -docid $DBLP.id -indeg $DBLP.nincites -outdeg $DBLP.noutcites -year $DBLP.year -authors $DBLP.nauthors -nuniqs $DBLP.nuniqs -ntokens $DBLP.ntokens -lang $DBLP.langid -bows $DBLP.bowscores -sems $DBLP.2K.$FEATS_TYPE.semscores
