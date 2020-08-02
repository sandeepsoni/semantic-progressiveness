#!/bin/bash

OPS=ops
DIR=/hg191/corpora/semantic-progressiveness/legal-data/processed

python -u courtlistener_feat_aggregate.py $DIR $OPS.complete -docid $OPS.list -indeg $OPS.ind -outdeg $OPS.outd -year $OPS.dates -nuniqs $OPS.nuniqs -ntokens $OPS.ntokens -bows $OPS.bowscores -sems $OPS.semscores
