#!/bin/bash
#Author: Saurabh Pathak
#binarize all the language models created with step 1
#Step 4
#long process - run with sudo if you want to alter priorities
#uses moses/bin in $PATH and default arguments (Probing table 1.5 ratio)
cd $HOME/src/python/nlp/mtech-thesis/data/train
echo Starting binarization process. This will take long. If you close the window at any time, the remaining models will be left unbinarized but the model under progess will be completed in the background.\nCheck nohup.out anytime to see detailed progress.
c=$(ls -l lm | grep arpa | wc -l)
i=0
echo Remaining models: $c
for x in $(ls -1 lm | grep arpa)
do
	i=$(($i+1))
	nohup build_binary -T . lm/$x lm/$(echo $x | grep -o '^.*\.')probing.1.5.blm &
	y=$(pgrep build_binary)
	echo "PID $y is binarizing $x...[Remaining: $(($c-$i))]"
	if [ $UID -eq 0 ]
	then
		renice -n -5 -p $y
		ionice -c 1 -n 0 -p $y
	fi
	rm -f nohup.out
done
echo finished execution.
