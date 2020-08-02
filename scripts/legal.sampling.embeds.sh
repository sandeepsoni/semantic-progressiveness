### For the last 5 years in the legal data (between 2006 to 2010),
### sample the documents at different rates. Also, run the 

dir=/hg191/corpora/legaldata/sc-time
time python text2vectors.py $dir/11.jsonl $dir/1.14.11.model $dir/1.14.11.log -seed 1 -rate 0.14 & #run.sampling-rate.corpusid.{model,log}
time python text2vectors.py $dir/11.jsonl $dir/2.14.11.model $dir/2.14.11.log -seed 2 -rate 0.14 &
time python text2vectors.py $dir/11.jsonl $dir/3.14.11.model $dir/3.14.11.log -seed 3 -rate 0.14 &
time python text2vectors.py $dir/11.jsonl $dir/4.14.11.model $dir/4.14.11.log -seed 4 -rate 0.14 &
time python text2vectors.py $dir/11.jsonl $dir/5.14.11.model $dir/5.14.11.log -seed 5 -rate 0.14 &
time python text2vectors.py $dir/11.jsonl $dir/11.model $dir/11.log -seed 1 -rate 1.0 &
