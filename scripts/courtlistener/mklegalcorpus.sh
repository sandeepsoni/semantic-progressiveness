#! /bin/bash

source constants.sh

# filter out the required fields and aggregate all files in one jurisdiction.
parallel --max-procs $MAX_PROCS python filterAndAggregate.py $FILES_DIR ::: $(cat $JURS_FILE)
echo "Filter and aggregate done, `date`"

# sort the records by their date of filing
parallel --max-procs $MAX_PROCS python sortRecords.py $FILES_DIR ::: $(cat $JURS_FILE)
echo "Sorting done, `date`"
wait

# tokenize and tag the text using spacy
parallel --max-procs $MAX_PROCS python tokenizeText.py $FILES_DIR ::: $(cat $JURS_FILE)
echo "Tokenization done, `date`"
