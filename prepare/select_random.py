#!/bin/env python3
#Author: Saurabh Pathak
'''Random set of sentences selector form the corpus for evaluation and puts the rest in training set. - default 10000'''
import getopt, random, sys, os

def sample():
    '''random sampler'''
    os.makedirs(output_dir+'selected_out', mode=0o755, exist_ok=True)

    with open(prefix+'.'+target, encoding='utf-8') as en_ip, open(prefix+'.'+source, encoding='utf-8') as hi_ip, open(output_dir+prefix1+'.train.'+target, 'w', encoding='utf-8') as en_op, open(output_dir+prefix1+'.train.'+source, 'w', encoding='utf-8') as hi_op, open(output_dir+'selected_out/'+prefix1+'.sep.'+source, 'w', encoding='utf-8') as hi_sep_op, open(output_dir+'selected_out/'+prefix1+'.sep.'+target, 'w', encoding='utf-8') as en_sep_op:
        print('Sampling {} random sentence pairs...'.format(k), end='', flush=True)
        num_lines = len(en_ip.readlines())
        en_ip.seek(0)
        selected_lines = random.sample(range(1, num_lines+1), k)
        for i, hi_line, en_line in zip(range(1, num_lines+1),hi_ip, en_ip):
            if i in selected_lines: o_h, o_e = hi_sep_op, en_sep_op
            else: o_h, o_e = hi_op, en_op
            o_h.write(hi_line)
            o_e.write(en_line)
    print('done.')

def usage():
    print('Usage: select_random.py options\n\t-f\tsource language suffix\n\t-e\ttarget language suffix\n\t-k\tnumber of samples to extract\n\t--prefix\tcorpus files common prefix\n\t--output-dir\toutput folder')
    exit(1)
    
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hf:e:k:', ['help', 'prefix=', 'output-dir='])
    k = 10000
    if len(args) > 0 or len(opts) < 4:
        print('Invalid arguments or fewer parameters.')
        usage()
    for o, a in opts:
        if o in ('-h', '--help'): usage()
        elif o == '-f': source = a
        elif o == '-e': target = a
        elif o == '-k': k = int(a)
        elif o == '--prefix': prefix, prefix1 = a, '.'.join(a.split('/')[-1].split('.')[:-1])
        elif o == '--output-dir': output_dir = a if a[-1] == '/' else a + '/'
        else:
            print('Invalid parameters.')
            usage()
    sample()
