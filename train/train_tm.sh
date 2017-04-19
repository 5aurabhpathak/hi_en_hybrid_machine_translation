#!/bin/bash
#Author: Saurabh Pathak
#trains the translation models along with transliteration module
cores=16
sbsize=512
sbuffsize=10G
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
mkdir -p $OUT_DIR/model/$3
if [ ! -s $OUT_DIR/model/aligned.grow-diag-final-and ]
then
	nohup $THESISDIR/train/align.sh $OUT_DIR $IN_DIR >& $OUT_DIR/align.out || exit 2
	nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment grow-diag-final-and -score-options '--KneserNey' -first-step 4 -last-step 4 -external-bin-dir /opt/mgiza/bin -cores $cores -sort-buffer-size $sbuffsize -sort-batch-size $sbsize -sort-parallel $cores >& $OUT_DIR/lex.out
fi
nohup $THESISDIR/train/train-transliteration-module.sh $IN_DIR $OUT_DIR/model/aligned.grow-diag-final-and $OUT_DIR/model/$3/transliterate $3 >& $OUT_DIR/model/$3/translit.out || exit 3
#train model
if [ "$3" = "hpb" ]
then h="-hierarchical -glue-grammar"
elif [ "$3" = "pb" ]
then h="-reordering msd-bidirectional-fe"
else echo Wrong model requested. && exit 4
fi
nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment-file $OUT_DIR/model/aligned -alignment grow-diag-final-and -model-dir $OUT_DIR/model/$3 -lexical-file $OUT_DIR/model/lex -first-step 5 -score-options '--KneserNey' -lm 0:5:$THESISDIR/data/lm/lm.en.5.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -max-phrase-length 5 -cores $cores -sort-buffer-size $sbuffsize -sort-batch-size $sbsize -sort-parallel $cores $h >& $OUT_DIR/model/$3/training.out
exit 0
