#!/bin/bash

source constants.sh

### create corpus and tokenize the text.
#/bin/.sh 
#echo 'corpus creation ... done'

### make stats files
#python mkstats.py $FILES_DIR $STATS_DIR $JURS_FILE $PARENT_DIR/cites.csv
#echo 'stats creation ... done'

### create two files (subcorpora) from the original corpus (TODO)
#echo 'text subcorpora ... done'

### train separate SGNS models to learn word embeddings from
#/bin/bash text2vectors.sh
#echo 'vectors creation ... done'

### (used in post-processing) PoS tags for tokens by sampling (TODO).
#/bin/bash corpus2postags.sh 
#echo 'pos tagging ... done'

### Progressiveness score for each document
python progressiveness.py $MODELS_DIR/sgns.$LIM.early.100.model $MODELS_DIR/sgns.$LIM.later.100.model $STATS_DIR/$OPS.1K.feats_manual $STATS_DIR/$OPS.docs $STATS_DIR/$OPS.semscores
