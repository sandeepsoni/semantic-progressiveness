#!/bin/bash

source constants.sh

### make one file as complete corpus
#python mkcorpus.py '/hg191/corpora/historical_newspapers/accessible/*/*/*.txt' $FILES_DIR/$CORPUS_FILENAME $FILES_DIR/tmp
#echo 'corpus creation ... done'

### tokenize the text from the corpus
#/bin/bash corpus2tokens.sh
#echo 'text tokenization ... done'

### make a file of token frequencies
#python mkTokenFreqs.py $FILES_DIR/$CORPUS_TOKENIZED_FILE $FILES_DIR/$NEWS.token_freqs.tsv
#echo 'token frequencies ... done'

### standardize the tokens
#python standardizeTokensUsingNGrams.py $FILES_DIR/$CORPUS_TOKENIZED_FILE /$DRIVE/corpora/google-ngrams/en.1M.filtered.1g /$DRIVE/corpora/google-ngrams/en.filtered.2g $FILES_DIR/$NEWS.token_subs.txt $FILES_DIR/$NEWS.standardized.tokenized.jsonl

python standardizeTokensUsingNGrams.py $FILES_DIR/$CORPUS_TOKENIZED_FILE /$DRIVE/corpora/google-ngrams/en.1M.filtered.1g /$DRIVE/corpora/google-ngrams/en.1M.filtered.2g /$DRIVE/corpora/google-ngrams/en.1M.filtered.3g $FILES_DIR/$NEWS.token_subs.txt $FILES_DIR/$NEWS.standardized.tokenized.jsonl

mv $FILES_DIR/$NEWS.standardized.tokenized.jsonl $FILES_DIR/$CORPUS_TOKENIZED_FILE
echo 'standardizing tokens ... done'

### make stats files
#/bin/bash mkstats.sh
#echo 'stats creation ... done'

### create two files (subcorpora) from the original corpus (use when equal number of documents in both periods are needed)
#python subcorpora.py $LIM_NUM $STATS_DIR/$NEWS.uncased $STATS_DIR/$NEWS.$LIM.early.docs
#python subcorpora.py $LIM_NUM $STATS_DIR/$NEWS.uncased $STATS_DIR/$NEWS.$LIM.later.docs -tail
#echo 'text subcorpora ... done'

### create two files (subcorpora) from the original corpus (use when the periods are defined by time)
#python subcorpora_bydate.py 18270101 18400512 $STATS_DIR/$NEWS.filename $STATS_DIR/$NEWS.tokens $STATS_DIR/$NEWS.$DATE.early.docs
#python subcorpora_bydate.py 18500918 18651231 $STATS_DIR/$NEWS.filename $STATS_DIR/$NEWS.tokens $STATS_DIR/$NEWS.$DATE.later.docs
#python subcorpora_bydate.py 18270101 18400512 $STATS_DIR/$NEWS.filename $STATS_DIR/$NEWS.uncased $STATS_DIR/$NEWS.$DATE.early.texts
#python subcorpora_bydate.py 18500918 18651231 $STATS_DIR/$NEWS.filename $STATS_DIR/$NEWS.uncased $STATS_DIR/$NEWS.$DATE.later.texts
#echo 'text subcorpora ... done'

### train separate SGNS models to learn word embeddings from two different periods.
#/bin/bash text2vectors.sh
#echo 'vectors creation ... done'

### obtain the semantically shifted words. 
#python semshiftwords.py $MODELS_DIR/$NEWS.$DATE.early.model $MODELS_DIR/$NEWS.$DATE.later.model $STATS_DIR/$NEWS.$DATE.orig_changelist
#echo 'list generation ... done'

### (used in post-processing) PoS tags for tokens by sampling.
#/bin/bash corpus2postags.sh 
#echo 'pos tagging ... done'

### post-pruning of the list
#/bin/bash postpruning.sh
#echo 'list pruning ... done'

### nearest neighbors of the words in a file
#python nearest_neighbors.py $MODELS_DIR/$NEWS.$DATE.early.model $MODELS_DIR/$NEWS.$DATE.later.model $STATS_DIR/$NEWS.$DATE.name_pruned_changelist $STATS_DIR/$NEWS.$DATE.nearest_neighbors
#echo 'nearest neighbors ... done'
