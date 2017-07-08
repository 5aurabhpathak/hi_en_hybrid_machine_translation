#!/bin/env python3
#Author: Saurabh Pathak
#Main program: Stiches the pipeline together
#Usage: (main.py sourcefileneame) or just (main.py) for a text cli :)
from subprocess import Popen, PIPE, DEVNULL
from sys import argv, stderr
import ebmt, rulebaseprior, xml_input, data, transliterate, os, shutil

def make_chunkset(text, tags, l, verbose=True):
    if verbose: print('Applying rules...', sep='', end='', flush=True, file=stderr)
    chunkset = rulebaseprior.apply_rules(text, tags, l)
    if verbose: print('Done\nEBMT is running...', sep='', end='', flush=True, file=stderr)
    chunkset.extend(ebmt.run(text, bm, l))
    if verbose: print('Done', flush=True, file=stderr)
    return chunkset

def translate_sent(text, p):
    print('Tagging input...', sep='', end='', flush=True, file=stderr)
    tags = rulebaseprior.tag_input(text)
    print('Done', flush=True, file=stderr)
    text = text.split()
    l = len(text)
    xml = xml_input.construct(make_chunkset(text, tags, l), text, l)
    print('Partially translated xml input:', xml, file=stderr)
    p.stdin.write('{}\n'.format(xml))
    p.stdin.flush()
    print('Moses is translating...', flush=True, file=stderr)
    smt = p.stdout.readline()
    print('Done\nTransliterating OOVs...', flush=True, file=stderr)
    print('Translated:', transliterate.translit_sent(smt))

def translate_file(text):
    print('Tagging input...', sep='', end='', flush=True, file=stderr)
    tags = rulebaseprior.tag_input_file(text)
    print('Done\nHave patience. run \'tail-f data/run/xml.out\' if you dont. :)\nApplying rules followed by EBMT followed by recombination on each sentence...', flush=True, file=stderr)

    with open(text) as f, open('{}/xml.out'.format(run), 'w', encoding='utf-8') as xml:
        for i, line in enumerate(f):
            print('processing sentence:', i+1, end='\r', flush=True, file=stderr)
            line = line.split()
            l = len(line)
            xml.write('{}\n'.format(xml_input.construct(make_chunkset(line, tags[i], l, False), line, l)))

    with open('{}/smt.out'.format(run), 'w', encoding='utf-8') as smt:
        print('Filtering rule table for faster translation (approx 10 minutes)...', end='', flush=True, file=stderr)
        shutil.rmtree(run + '/filetable', ignore_errors=True)
        Popen('{0}/training/filter-model-given-input.pl {1}/filetable {1}/moses.file.ini {2} -Binarizer "CreateOnDiskPt 1 1 4 0 2" -Hierarchical'.format(os.environ['SCRIPTS_ROOTDIR'], run, text), shell=True, stdout=DEVNULL, stderr=DEVNULL).wait()
        print('Done\nHave patience. run \'tail-f data/run/smt.out\' if you dont. :)\nMoses is translating...', sep='', end='', flush=True, file=stderr)
        Popen('moses -inputtype 0 -f {0}/filetable/moses.ini -xml-input inclusive -mp -i {0}/xml.out'.format(run).split(), universal_newlines=True, stdout=smt, stderr=DEVNULL).wait()

    print('Done\nTransliterating OOVs...', sep='', end='', flush=True, file=stderr)
    transliterate.translit_file('{}/smt.out'.format(run))
    print('Done', flush=True, file=stderr)

    if len(argv) == 3:
        with open('{}/en.out'.format(run)) as out:
            p = Popen('{}/generic/multi-bleu.perl {}'.format(os.environ['SCRIPTS_ROOTDIR'], os.path.abspath(argv[2])).split(), universal_newlines=True, stdin=out, stdout=PIPE, stderr=DEVNULL)
            out, err = p.communicate()
        print('BLEU score: {}'.format(out.split()[2][:-1]), flush=True, file=stderr)
    print('Check en.out in data/run. Bye!'.format(out.split()[2][:-1]), flush=True, file=stderr)

print('Loading example-base...', sep='', end='', flush=True, file=stderr)
data.load()
print('Done\nLoading suffix arrays...', sep='', end='', flush=True, file=stderr)
bm = ebmt._BestMatch(data.dbdir)
print('Done', flush=True, file=stderr)
run  = data.run
ini = '{}/moses.ini'.format(run)
try: translate_file(os.path.abspath(argv[1]))
except IndexError:
    print('Starting moses...', sep='', end='', flush=True, file=stderr)
    p = Popen('moses -inputtype 0 -f {} -xml-input inclusive -mp'.format(ini).split(), universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    while 'input-output' not in p.stderr.readline(): pass
    print('Ready\nWelcome to the SILP Hindi to English Translator!', flush=True, file=stderr)
    while True:
        try:
            text = input('Enter one Hindi sentence or ctrl+d to exit:\n')
            translate_sent(text, p)
        except EOFError:
            print('Bye!', file=stderr)
            exit(0)
