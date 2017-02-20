#!/bin/bash
#Author: Saurabh Pathak
#trains the translation models along with transliteration module
if [[ $(ps -o stat= -p $$) =~ "+"  || $# -ne 3 ]]
then
	echo "usage: train_tm.sh trainrootdir corpusprefix pb|hpb &"
	exit 1
fi

change_absolute () {
	if [ "${1:0:1}" = "/" ]
	then echo $1
	else echo "$PWD/$1"
	fi
}

export PYTHONIOENCODING=utf-8
mkdir -p $1
OUT_DIR=$(change_absolute $1)
IN_DIR=$(change_absolute $2)
#nohup $THESISDIR/train/align.sh $OUT_DIR $IN_DIR >& $OUT_DIR/align.out || exit 2
#nohup $THESISDIR/train/train-transliteration-module.sh $IN_DIR $OUT_DIR/model/aligned.grow-diag-final-and $OUT_DIR/transliterate >& $OUT_DIR/translit.out || exit 3
#nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment grow-diag-final-and -score-options '--KneserNey' -first-step 4 -last-step 4 -external-bin-dir /opt/mgiza/bin -cores 16 -sort-buffer-size 20G -sort-batch-size 512 -sort-parallel 16 >& $OUT_DIR/lex.out
#train model
if [ $3 = "pb" ]
then
	mkdir -p $OUT_DIR/model/pb
	nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment-file $OUT_DIR/model/aligned -alignment grow-diag-final-and -model-dir $OUT_DIR/model/pb -lexical-file $OUT_DIR/model/lex -first-step 5 -reordering msd-bidirectional-fe -score-options '--KneserNey' -lm 0:5:$THESISDIR/data/lm/lc/lm.en.5.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -post-decoding-translit yes -transliteration-phrase-table $OUT_DIR/transliterate/model/phrase-table.gz -max-phrase-length 5 -cores 16 -sort-buffer-size 20G -sort-batch-size 512 -sort-parallel 16 >& $OUT_DIR/model/pb/training.out
elif [ $3 = "hpb" ]
then
	mkdir -p $OUT_DIR/model/hpb
	nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment-file $OUT_DIR/model/aligned -alignment grow-diag-final-and -model-dir $OUT_DIR/model/hpb -lexical-file $OUT_DIR/model/lex -first-step 5 -hierarchical -glue-grammar -score-options '--KneserNey' -lm 0:5:$THESISDIR/data/lm/lc/lm.en.5.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -post-decoding-translit yes -transliteration-phrase-table $OUT_DIR/transliterate/model/phrase-table.gz -max-phrase-length 5 -cores 16 -sort-buffer-size 20G -sort-batch-size 512 -sort-parallel 16 >& $OUT_DIR/model/hpb/training.out
else echo Wrong model requested. && exit 4
fi
exit 0
