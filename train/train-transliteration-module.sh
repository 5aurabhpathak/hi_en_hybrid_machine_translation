#!/bin/bash
#Author: Saurabh Pathak
#Credits: Adapted from moses transliteration training script of the same name.
#This adaptation is specific to my use and is not general purpose like the script.
function usage {
	echo "usage: train-transliteration-module.sh corpus_stem alignmentfile outputdir"
	exit 1
}

if [ $# -ne 3 ]
then usage
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

function main {
	export PYTHONIOENCODING=utf-8
	mkdir -p $3
	OUT_DIR=$(change_absolute $3)
	IN_DIR=$(change_absolute $1)
	ln -s $IN_DIR.hi $OUT_DIR/f
	ln -s $IN_DIR.en $OUT_DIR/e
	ln -s $(change_absolute $2) $OUT_DIR/a
	mine_transliterations
	train_transliteration_module
	retrain_transliteration_module
	rm -rf model # <-- stray empty dir created by train-model.perl
	echo "Training Transliteration Module - End ". $(date)
}

function learn_transliteration_model {
	cp $OUT_DIR/training/corpus$1.en $OUT_DIR/lm/target
	echo Align Corpus
	$SCRIPTS_ROOTDIR/training/train-model.perl -mgiza -mgiza-cpus 16 -dont-zip -last-step 3 -external-bin-dir /opt/mgiza/bin -f hi -e en -alignment grow-diag-final-and -score-options '--KneserNey' -corpus $OUT_DIR/training/corpus$t -corpus-dir $OUT_DIR/training/prepared -giza-e2f $OUT_DIR/training/giza -giza-f2e $OUT_DIR/training/giza-inverse -alignment-file $OUT_DIR/model/aligned -alignment-stem $OUT_DIR/model/aligned -cores 16 -parallel -sort-buffer-size 10G -sort-batch-size 512 -sort-parallel 16
	echo Train Translation Models
	$SCRIPTS_ROOTDIR/training/train-model.perl -dont-zip -first-step 4 -last-step 6 -external-bin-dir /opt/mgiza/bin -f hi -e en -alignment grow-diag-final-and -score-options '--KneserNey' -lexical-file $OUT_DIR/model/lex -alignment-file $OUT_DIR/model/aligned -alignment-stem $OUT_DIR/model/aligned -extract-file $OUT_DIR/model/extract -phrase-translation-table $OUT_DIR/model/phrase-table -corpus $OUT_DIR/training/corpus$t -cores 16 -sort-buffer-size 10G -sort-batch-size 512 -sort-parallel 16
	echo Train Language Models
	lmplz -o 5 --interpolate_unigrams 0 --discount_fallback --text $OUT_DIR/lm/target --arpa $OUT_DIR/lm/targetLM
	build_binary $OUT_DIR/lm/targetLM $OUT_DIR/lm/targetLM.bin
	echo Create Config File
	$SCRIPTS_ROOTDIR/training/train-model.perl -first-step 9 -f hi -e en -phrase-translation-table $OUT_DIR/model/phrase-table -config $OUT_DIR/model/moses.ini -lm 0:5:$OUT_DIR/lm/targetLM.bin:8 -external-bin-dir /opt/mgiza/bin
}

function mine_transliterations {
	echo "Creating Model"
	echo "Extracting 1-1 Alignments"
	1-1-Extraction $OUT_DIR/f $OUT_DIR/e $OUT_DIR/a > $OUT_DIR/1-1.hi-en
	echo "Cleaning the lsit for Miner"
	$SCRIPTS_ROOTDIR/Transliteration/clean.pl $OUT_DIR/1-1.hi-en > $OUT_DIR/1-1.hi-en.cleaned
	test -s $OUT_DIR/1-1.hi-en.pair-probs && echo 1-1.hi-en.pair-probs in place, reusing || (echo Extracting Transliteration Pairs && TMining $OUT_DIR/1-1.hi-en.cleaned > $OUT_DIR/1-1.hi-en.pair-probs)
	echo Selecting Transliteration Pairs with threshold 0.5
	echo 0.5 | $SCRIPTS_ROOTDIR/Transliteration/threshold.pl $OUT_DIR/1-1.hi-en.pair-probs > $OUT_DIR/1-1.hi-en.mined-pairs
}

function train_transliteration_module {
	mkdir -p $OUT_DIR/model $OUT_DIR/lm
	echo Preparing Corpus
	$SCRIPTS_ROOTDIR/Transliteration/corpusCreator.pl $OUT_DIR 1-1.hi-en.mined-pairs hi en
	test -e $OUT_DIR/training/corpusA.en && learn_transliteration_model A || learn_transliteration_model
	echo Running Tuning for Transliteration Module
	touch $OUT_DIR/tuning/moses.table.ini
	$SCRIPTS_ROOTDIR/training/train-model.perl  -mgiza -mgiza-cpus 16 -dont-zip -first-step 9 -external-bin-dir /opt/mgiza/bin -f hi -e en -alignment grow-diag-final-and -score-options '--KneserNey' -phrase-translation-table $OUT_DIR/model/phrase-table -config $OUT_DIR/tuning/moses.table.ini -lm 0:5:$OUT_DIR/tuning/moses.table.ini:8
	$SCRIPTS_ROOTDIR/training/filter-model-given-input.pl $OUT_DIR/tuning/filtered $OUT_DIR/tuning/moses.table.ini $OUT_DIR/tuning/input  -Binarizer processPhraseTableMin
	rm $OUT_DIR/tuning/moses.table.ini
	$SCRIPTS_ROOTDIR/ems/support/substitute-filtered-tables.perl $OUT_DIR/tuning/filtered/moses.ini < $OUT_DIR/model/moses.ini > $OUT_DIR/tuning/moses.filtered.ini
	$SCRIPTS_ROOTDIR/training/mert-moses.pl $OUT_DIR/tuning/input $OUT_DIR/tuning/reference /opt/moses/bin/moses $OUT_DIR/tuning/moses.filtered.ini --nbest 100 --working-dir $OUT_DIR/tuning/tmp --rootdir /opt/moses/bin --decoder-flags "-threads 16 -drop-unknown -v 0 -distortion-limit 0" -mertdir /opt/moses/bin -threads=16 --no-filter-phrase-table
	cp $OUT_DIR/tuning/tmp/moses.ini $OUT_DIR/tuning/moses.ini
	$SCRIPTS_ROOTDIR/ems/support/substitute-weights.perl $OUT_DIR/model/moses.ini $OUT_DIR/tuning/moses.ini $OUT_DIR/tuning/moses.tuned.ini
}

function retrain_transliteration_module {
	if [ -s $OUT_DIR/training/corpusA.en ]
	then
		cd $OUT_DIR
		rm -rf model/* lm/* training/giza training/giza-inverse training/prepared
		cd ..
		learn_transliteration_model
	fi
}

main $1 $2 $3
exit 0
