#!/bin/env python3.6
#Author: Saurabh Pathak
'''parallel corpus cleaner -- three stage'''
import getopt, sys, os, collections

def clean():
    '''stage 1 - removes duplicate source AND translation pairs. Keeps same source but different translations.
    stage 2 - source sentences containing hindi letters are dropped based on unicode codepoint range for devanagari and vice versa.
    stage 3 - heuristic: sentence pairs differing greatly in size are probably misaligned and/or malformed. Prefer over moses's clean-corpus-n script. This function handles size difference more elaborately.'''
    prohibited_hi = 'abcdefghijklmnopqrstuvwxyz'
    os.makedirs(output_dir+'filtered_out', mode=0o755, exist_ok=True)
    unique_dict = collections.defaultdict(set)

    with open(prefix+'.'+target, encoding='utf-8') as en_ip, open(prefix+'.'+source, encoding='utf-8') as hi_ip, open(output_dir+prefix1+'.clean.'+target, 'w', encoding='utf-8') as en_op, open(output_dir+prefix1+'.clean.'+source, 'w', encoding='utf-8') as hi_op, open(output_dir+'filtered_out/'+prefix1+'.err.'+source, 'w', encoding='utf-8') as hi_err_op, open(output_dir+'filtered_out/'+prefix1+'.err.'+target, 'w', encoding='utf-8') as en_err_op:

        print('Cleaning...', end='', flush=True)
        for hi_line, en_line in zip(hi_ip, en_ip):
            #stage 1
            translations = unique_dict[hi_line]
            if en_line in translations: #<-- removes duplicate source and translation but keeps multiple translations of same source if any
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            translations.add(en_line)

            #stage 2
            flag = False
            for c in hi_line:
                if c in prohibited_hi or c.lower() in prohibited_hi or (not 2304 <= ord(c) <= 2431 and not 0 <= ord(c) < 128):
                    flag = True
                    break
            if flag:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            else:
                for c in en_line:
                    if 2304 <= ord(c) <= 2431:
                        flag = True
                        break
            if flag:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            
            #stage 3
            e, h = en_line.split(), hi_line.split()
            j, k = len(h), len(e)
            i = max(j, k)
            if not 0 < j <= 65 or not 0 < k <= 65 or (i > 10 and not 1 / 2 < j / k < 2) or (i <= 10 and not 1 / 9 < j / k < 9): #<--required by giza
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue

            hi_op.write(' '.join(h).replace('\u007C', '.').replace('\u0964', '.')+'\n') #<--removes redundant spaces and replaces poornaviram with .
            en_op.write(' '.join(e).replace('\u007C', '.').replace('\u0964', '.')+'\n')
    print('complete')

def usage():
    print('Usage: clean_bilingual_corpus.py -f <source_language_suffix> -e target_language_suffix --prefix <corpus_files_common_prefix> --output-dir <output_folder>')
    exit(1)

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hf:e:', ['help', 'prefix=', 'output-dir='])
    if len(args) > 0 or len(opts) < 4:
        print('Invalid arguments or fewer parameters.')
        usage()
    for o, a in opts:
        if o in ('-h', '--help'): usage()
        elif o == '-f': source = a
        elif o == '-e': target = a
        elif o == '--prefix': prefix, prefix1 = a, '.'.join(a.split('/')[-1].split('.')[:-1])
        elif o == '--output-dir': output_dir = a if a[-1] == '/' else a + '/'
        else:
            print('Invalid parameters.')
            usage()
    clean()
