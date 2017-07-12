#!/bin/env python3
#Author: Saurabh Pathak
#Creates some additional test sets from the isolated corpus
import os

workingdir = os.environ['THESISDIR'] + '/data/corpus/bilingual'
testsetdir = workingdir + '/additonaltestsets'
os.makedirs(testsetdir, exist_ok=True)

with open('{}/dev_test_tokenized/test.lc.hi'.format(workingdir)) as hi, open('{}//dev_test_tokenized/test.lc.en'.format(workingdir)) as en, \
        open('{}/s1.hi'.format(testsetdir), 'w', encoding='utf-8') as s1hi, open('{}/s1.en'.format(testsetdir), 'w', encoding='utf-8') as s1en, \
        open('{}/s2.hi'.format(testsetdir), 'w', encoding='utf-8') as s2hi, open('{}/s2.en'.format(testsetdir), 'w', encoding='utf-8') as s2en, \
        open('{}/s3.hi'.format(testsetdir), 'w', encoding='utf-8') as s3hi, open('{}/s3.en'.format(testsetdir), 'w', encoding='utf-8') as s3en, \
        open('{}/s4.hi'.format(testsetdir), 'w', encoding='utf-8') as s4hi, open('{}/s4.en'.format(testsetdir), 'w', encoding='utf-8') as s4en, \
        open('{}/s5.hi'.format(testsetdir), 'w', encoding='utf-8') as s5hi, open('{}/s5.en'.format(testsetdir), 'w', encoding='utf-8') as s5en:
            for hiline, enline in zip(hi, en):
                i = len(hiline.split())
                if 0 < i <= 10:
                    s1hi.write(hiline)
                    s1en.write(enline)
                elif 10 < i <= 20:
                    s2hi.write(hiline)
                    s2en.write(enline)
                elif 20 < i <= 30:
                    s3hi.write(hiline)
                    s3en.write(enline)
                elif 30 < i <= 40:
                    s4hi.write(hiline)
                    s4en.write(enline)
                elif 40 < i <= 50:
                    s5hi.write(hiline)
                    s5en.write(enline)
