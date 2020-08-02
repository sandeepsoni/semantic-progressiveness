### run the script to divide the corpus into smaller subcorpora

# Legal data
python corpus2subcorpora.py time /hg191/corpora/legaldata/casetext.tokenized.jsonl /hg191/corpora/legaldata/sc-time -s 1951 -u 2010 -p 5 &
python corpus2subcorpora.py docs /hg191/corpora/legaldata/casetext.tokenized.jsonl /hg191/corpora/legaldata/sc-docs -s 1951 -u 2010 -n 12 &

# Academic data
python corpus2subcorpora.py time /hg191/corpora/academic-data/semantic-scholar/abstracts.tokenized.jsonl /hg191/corpora/academic-data/semantic-scholar/sc-time -s 1952 -u 2017 -p 5 &
python corpus2subcorpora.py docs /hg191/corpora/academic-data/semantic-scholar/abstracts.tokenized.jsonl /hg191/corpora/academic-data/semantic-scholar/sc-docs -s 1952 -u 2017 -n 13 &
