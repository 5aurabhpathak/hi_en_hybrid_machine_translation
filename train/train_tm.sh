#!/bin/bash
#Author: Saurabh Pathak
#trains the translation models along with transliteration module
if [[ $(ps -o stat= -p $$) =~ "+"  || $# -ne 2 ]]
then
	echo "usage: train_tm.sh trainrootdir corpusprefix &"
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
nohup $THESISDIR/train/train-transliteration-module.sh $IN_DIR $OUT_DIR/model/aligned.grow-diag-final-and $OUT_DIR/transliterate >& $OUT_DIR/translit.out || exit 3
#train model
nohup $SCRIPTS_ROOTDIR/training/train-model.perl -root-dir $OUT_DIR -corpus $IN_DIR -f hi -e en -alignment grow-diag-final-and -first-step 4 -reordering msd-bidirectional-fe -lm 0:4:$THESISDIR/lm/lm.en.4.probing.1.5.blm:8 -external-bin-dir /opt/mgiza/bin -post-decoding-translit yes -transliteration-phrase-table transliterate/model/phrase-table.gz -max-phrase-length 5 -cores 16 -sort-buffer-size 10G -sort-batch-size 512 -sort-parallel 16 >& $OUT_DIR/training.out
exit 0
