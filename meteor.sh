#!/bin/bash
#Author: Saurabh Pathak
#Runs meteor and produces final score
cd $THESISDIR/data/downloaded/meteor-1.5
java -Xmx2G -jar meteor-1.5.jar $1 $2 -l en -q #2>/dev/null
exit 0
