DIR=/hg191/corpora/academic-data/semantic-scholar
LAST_SPLIT_NUM=7
SPLITS=8

#1. Create one corpus with documents sorted in time.
#python mkacadcorpus.py '/hg191/corpora/academic-data/semantic-scholar/s2-corpus-*' $DIR/abstracts.jsonl $DIR/tmp
#echo "Finished making corpus in one file" 

#2. Divide the corpus into subcorpora of roughly equal sizes.
python corpus2subcorpora.py docs $DIR/abstracts.jsonl $DIR/sc-docs -n $SPLITS
echo "Finished dividing the corpus into subcorpora"

#3. Tokenize every document in the corpus
for i in `seq 0 1 $LAST_SPLIT_NUM`; do
	python corpus2tokens.py abstract $DIR/sc-docs/$i.jsonl $DIR/sc-docs/$i.tokenized.jsonl -since 1930 -until 2018 &
	pids[${i}]=$!
done

for pid in ${pids[@]}; do
	wait $pid;
done
echo "Finished tokenizing the text"
