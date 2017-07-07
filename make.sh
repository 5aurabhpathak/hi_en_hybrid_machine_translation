#!/bin/bash
#Author: Saurabh Pathak
#Port of POS tagger's makefile to bash script
#Plus it does not use intermediate disk I/O and can deal with both file and string input. :)
#Also, my sentence boundary detection is better (SBD)-- can handle abbreviations and big text files ;)
TAGGERDIR="$THESISDIR/data/downloaded/hindi-part-of-speech-tagger"
TAGGER="$TAGGERDIR/bin/tnt -v0 -H models/hindi"  # Use option -u1 for speed at a slight cost of precision. For more options use ./bin/tnt -h
LEMMATIZER="$TAGGERDIR/bin/lemmatiser.py models/hindi.lemma"
TAG2VERT="$TAGGERDIR/bin/tag2vert.py"
NORMALIZE="$TAGGERDIR/bin/normalize_vert.py"
POSMOD="$TAGGERDIR/bin/modify_pos.py"
TOKENIZER="$TAGGERDIR/bin/unitok.py -l hindi -n"

if [ -f $1 ] >& /dev/null
then IN=$(cat $1)
else IN="$1"
fi

cd $TAGGERDIR
$TAGGER <( echo "$IN" | sed 's/$/EOL/g' | $TOKENIZER | sed -e 's/।/./g' |  $NORMALIZE ) | sed -e 's/\t\+/\t/g' | $LEMMATIZER | $TAG2VERT
exit 0
