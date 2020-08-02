DIR=/hg191/corpora/legaldata

#1. Create one corpus with documents sorted in time.
time python mkacadcorpus.py $DIR/casetext.jsonl $DIR/legaldocs.jsonl $DIR/tmp

#2. Tokenize every document in the corpus 
time python corpus2tokens.py text $DIR/legaldocs.jsonl $DIR/legaldocs.tokenized.jsonl -since 1700 -until 2015
