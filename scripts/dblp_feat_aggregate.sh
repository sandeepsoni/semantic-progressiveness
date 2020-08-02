#!/bin/bash

DBLP=dblp
DIR=/hg191/corpora/semantic-progressiveness/acad-data/processed

python -u dblp_feat_aggregate.py $DIR $DBLP.complete -docid $DBLP.id -indeg $DBLP.nincites -outdeg $DBLP.noutcites -year $DBLP.year -authors $DBLP.nauthors -nuniqs $DBLP.nuniqs -ntokens $DBLP.ntokens -lang $DBLP.langid -bows $DBLP.bowscores -sems $DBLP.semscores
