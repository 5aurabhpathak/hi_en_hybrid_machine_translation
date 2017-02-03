#!/bin/env python3
#Author: Saurabh Pathak
'''Corpus tokenizer for english'''
import getopt, sys

def tokenize(filename, output):
    '''Sentence boundary detector and tokenizer.'''
    punct, numb = '`!"£$%^&*()-_+÷≈≠×#~|}{][:;@\'\\‘’?¿/>≥…<,≤|¬¦“”¢€¥→↓↑♪•★∞†‡√°ⁿ', '1234567890'
    with open(filename, 'r', encoding='utf-8') as ip, open(output, 'w', encoding='utf-8') as op:
        for line in ip:
            op_line = '  '
            for c in line:
                if c == '.': #special case
                    if op_line[-1].isupper(): continue
                    elif op_line[-1] in numb: op_line += c
                    else: op_line += ' ' + c
                elif c in punct: op_line += ' ' + c + ' '
                elif c in numb: # another special case
                    if op_line[-1] not in numb:
                        if op_line[-1] != '.' or op_line[-2] not in numb+' \n\t': op_line += ' '
                    op_line += c
                elif op_line[-1] in '?.' and c != '\n': op_line += c + '\n'
                else: op_line += c
            op.write(op_line)

def usage():
    print('Usage: tokenize_en.py inputfile output_directory')
    exit(0)

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    if len(opts) > 0 or len(args) < 2: usage()
    tokenize(args[0], args[1])
