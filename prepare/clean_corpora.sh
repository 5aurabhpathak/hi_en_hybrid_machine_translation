#!/bin/bash
#Author: Saurabh Pathak
#Third Step
#cleaning of parallel corpus - uses (my own) python scripts.
#monolingual corpus was not cleaned. However, certain literatures suggest that such a cleaning might benefit the translation system. (Ref. topic 'Controlled Language rules in MT'). I am not much inclined towards it as of now because of the nature and proportion of my work. Furthermore, we also have the post edition option to correct any errors introduced by noise in the corpus.
cd $HOME/src/python/nlp/mtech-thesis/prepare
./clean_bilingual_corpus.py --prefix ../data/corpus/bilingual/parallel/IITB.en-hi.true --output-dir ../data/corpus/bilingual/parallel/ -f hi -e en
exit 0
#future: may add cleaning of monolingual corpora if necessary.
#My hypothesis at this point is that it shouldn't be.
