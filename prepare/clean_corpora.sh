#!/bin/bash
#Author: Saurabh Pathak
#Third Step
#cleaning of parallel corpus - uses moses scripts.
#monolingual corpus was not cleaned. However, certain literatures suggest that such a cleaning might benefit the translation system. (Ref. topic 'Controlled Language rules in MT'). I am not much inclined towards it as of now because of the nature and proportion of my work. Furthermore, we also have the post edition option to correct any errors introduced by noise in the corpus.
cd $THESISDIR/prepare
./clean_bilingual_corpus.py --prefix ../data/corpus/bilingual/parallel/IITB.en-hi.true --output-dir ../data/corpus/bilingual/parallel/ -f hi -e en
./clean_bilingual_corpus.py --prefix ../data/corpus/bilingual/dev_test_tokenized/dev.true --output-dir ../data/corpus/bilingual/dev_test_tokenized/ -f hi -e en
./clean_bilingual_corpus.py --prefix ../data/corpus/bilingual/dev_test_tokenized/test.true --output-dir corpus/bilingual/dev_test_tokenized/ -f hi -e en
cd ../data/corpus/bilingual/dev_test_tokenized
rm dev.tok.en test.tok.en dev.true.* test.true.*
mv dev.clean.hi dev.true.hi
mv dev.clean.en dev.true.en
mv test.clean.en test.true.en
mv test.clean.hi test.clean.hi
echo lowercasing dev set...
time $SCRIPTS_ROOTDIR/tokenizer/lowercase.perl < dev.true.en > dev.lc.en
echo lowercasing test set...
time $SCRIPTS_ROOTDIR/tokenizer/lowercase.perl < test.true.en > test.lc.en
exit 0
#future: may add cleaning of monolingual corpora if necessary.
#My hypothesis at this point is that it shouldn't be.
