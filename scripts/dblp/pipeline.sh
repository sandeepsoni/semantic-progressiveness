#!/bin/bash

source constants.sh

### make one file as complete corpus
#python mkacadcorpus.py '/hg190/corpora/academic-data/dblp/files/dblp-ref-*.json' $FILES_DIR/$CORPUS_FILENAME $FILES_DIR/tmp
#echo 'corpus creation ... done'

### tokenize the text from the corpus
#/bin/bash corpus2tokens.sh
#echo 'text tokenization ... done'

### make stats files
#/bin/bash mkstats.sh
#echo 'stats creation ... done'

### create two files (subcorpora) from the original corpus
#python subcorpora.py $LIM_NUM $STATS_DIR/$DBLP.tokens $STATS_DIR/$DBLP.$LIM.early.docs
#python subcorpora.py $LIM_NUM $STATS_DIR/$DBLP.tokens $STATS_DIR/$DBLP.$LIM.later.docs -tail

#echo 'text subcorpora ... done'

### train separate SGNS models to learn word embeddings from
#/bin/bash text2vectors.sh
#echo 'vectors creation ... done'

### create subcorpora from original corpus that preserves case
#python subcorpora.py $LIM_NUM $STATS_DIR/$DBLP.abstract $STATS_DIR/$DBLP.$LIM.early.texts
#python subcorpora.py $LIM_NUM $STATS_DIR/$DBLP.abstract $STATS_DIR/$DBLP.$LIM.later.texts -tail
#echo 'uncased subcorpora ... done'

#python semshiftwords.py $MODELS_DIR/$DBLP.$LIM.early.model $MODELS_DIR/$DBLP.$LIM.later.model $STATS_DIR/$DBLP.orig_changelist
#echo 'list generation ... done'

### (used in post-processing) PoS tags for tokens by sampling.
#/bin/bash corpus2postags.sh 
#echo 'pos tagging ... done'

### post-pruning of the list
#python postpruning.py $MODELS_DIR/$DBLP.$LIM.early.model $MODELS_DIR/$DBLP.$LIM.later.model $STATS_DIR/$DBLP.orig_changelist 
#echo 'list pruning done'

### progressiveness
#/bin/bash progressiveness.sh
#echo 'progressiveness calculation ... done'

### bow features
/bin/bash bowfeatures.sh
echo 'bow scores ... done'

#### After this point all the code is in the relevant notebooks.
