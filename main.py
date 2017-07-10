#!/bin/env python3
#Author: Saurabh Pathak
#Main program: Stiches the pipeline together
#Usage: (main.py sourcefileneame) or (main.py sourcefile referencefile) for BLEU and METEOR or just (main.py) for a text cli :)
from subprocess import Popen, PIPE, DEVNULL
from sys import argv, stderr
import ebmt, rulebaseprior, xml_input, data, transliterate, os, shutil

def filter_rules(text):
    print('Filtering rule table for faster translation (approx 10 minutes)\nThis will only happen if the file is being decoded for the first time...', end='', flush=True, file=stderr)
    shutil.rmtree(run + '/filetable', ignore_errors=True)
    Popen('{0}/training/filter-model-given-input.pl {1}/filetable {1}/moses.file.ini {2} -Binarizer "CreateOnDiskPt 1 1 4 100 2" -Hierarchical'.format(os.environ['SCRIPTS_ROOTDIR'], run, text), shell=True, stdout=DEVNULL, stderr=DEVNULL).communicate()
    with open('{}/filetable/forfile'.format(run), 'w') as forfile: forfile.write(text)
    print('Done', flush=True, file=stderr)

def make_chunkset(text, tags, l, verbose=True):
    if verbose: print('Applying rules...', sep='', end='', flush=True, file=stderr)
    chunkset = rulebaseprior.apply_rules(text, tags, l)
    if verbose: print('Done\nEBMT is running...', sep='', end='', flush=True, file=stderr)
    try: chunkset.extend(ebmt.run(text, bm, l))
    except ebmt.ExactMatchException as e: return e.info
    if verbose: print('Done', flush=True, file=stderr)
    return chunkset

def translate_sent(text, p): #interactive handler. Might be broken. Not tested
    print('Tagging input...', sep='', end='', flush=True, file=stderr)
    tags = rulebaseprior.tag_input(text)
    print('Done', flush=True, file=stderr)
    text = text.split()
    l = len(text)
    chunkset = make_chunkset(text, tags, l)
    if isinstance(chunkset, str):
        print('Found exact match:', file=stderr)
        print(chunkset)
        return
    xml = xml_input.construct(chunkset, text, l)
    print('Partially translated xml input:', xml, file=stderr)
    p.stdin.write('{}\n'.format(xml))
    p.stdin.flush()
    print('Moses is translating...', flush=True, file=stderr)
    smt = p.stdout.readline()
    print('Done\nTransliterating OOVs...', flush=True, file=stderr)
    print('Translated:', transliterate.translit_sent(smt))

def translate_file(text): #file input. works fine.
    data.infofile = open('{}/info.txt'.format(run), 'w')
    data.infofile.write('Source File: {}\n'.format(text))
    print('Tagging input...', sep='', end='', flush=True, file=stderr)
    tags = rulebaseprior.tag_input_file(text)
    print('Done\nHave patience. run \'tail-f data/run/xml.out\' if you dont. :)\nApplying rules followed by EBMT followed by recombination on each sentence...', flush=True, file=stderr)

    with open(text) as f, open('{}/xml.out'.format(run), 'w', encoding='utf-8') as xml:
        for i, line in enumerate(f):
            print('processing sentence:', i+1, end='\r', flush=True, file=stderr)
            line = line.split()
            l = len(line)
            chunkset = make_chunkset(line, tags[i], l, False)
            if isinstance(chunkset, str):
                exact.update({i: chunkset})
                print('\033[KExact match at line', i+1, flush=True, file=stderr)
                continue
            xml.write('{}\n'.format(xml_input.construct(chunkset, line, l)))
    
    mlen = len(exact)
    print('\033[KDone.\nFound', mlen, 'direct matches\n{}'.format(rulebaseprior.j), 'rule(s) fired', flush=True, file=stderr)
    data.infofile.write('Sentences: {}\nEBMT found {} direct matches\n{} rule(s) fired by RBMT\n'.format(i+1, mlen, rulebaseprior.j))
    print(mlen)

    if os.path.exists('{}/filetable/forfile'.format(run)):
        forfile = open('{}/filetable/forfile'.format(run))
        if forfile.read().strip() not in {text, '*'}:
            forfile.close()
            filter_rules(text)
    else: filter_rules(text)

    print('Have patience. run \'tail-f data/run/smt.out\' if you dont. :)\nMoses is translating...', sep='', end='', flush=True, file=stderr)
    with open('{}/smt.out'.format(run), 'w', encoding='utf-8') as smt: Popen('moses -inputtype 0 -f {0}/filetable/moses.ini -xml-input inclusive -mp -i {0}/xml.out'.format(run).split(), universal_newlines=True, stdout=smt).communicate()

    print('Done\nTransliterating OOVs...', sep='', end='', flush=True, file=stderr)
    transliterate.translit_file('{}/smt.out'.format(run))
    data.infofile.write('OOVs: {}\n'.format(transliterate.j))
    print('Done', flush=True, file=stderr)

    if mlen > 0:
        key, i, j = list(exact.keys()), 0, 0
        key.sort()
        with open('{}/transliterated.out'.format(run)) as translited, open('{}/en.out'.format(run), 'w', encoding='utf-8') as out:
            for x in translited:
                while i < mlen and key[i] == j:
                    out.write(exact.pop(key[i])+'\n')
                    i += 1
                    j += 1
                out.write(x)
                j += 1
            while i < mlen:
                out.write(exact.pop(key[i])+'\n')
                i += 1
    else: shutil.copy2('{}/transliterated.out'.format(run), '{}/en.out'.format(run))

    if len(argv) == 3:
        with open('{}/en.out'.format(run)) as out:
            p = Popen('{}/generic/multi-bleu.perl {}'.format(os.environ['SCRIPTS_ROOTDIR'], os.path.abspath(argv[2])).split(), universal_newlines=True, stdin=out, stdout=PIPE, stderr=DEVNULL)
            out, err = p.communicate()
            bleu = out.split()[2][:-1]
        print('BLEU score: {}'.format(bleu), flush=True, file=stderr)
        p = Popen('{}/meteor.sh {} {}'.format(os.environ['THESISDIR'], '{}/en.out'.format(run), os.path.abspath(argv[2])).split(), universal_newlines=True, stdout=PIPE)
        out, err = p.communicate()
        meteor = round(float(out)*100, 2)
        print('METEOR score: {}'.format(meteor), flush=True, file=stderr)
        data.infofile.write('BLEU: {}\nMETEOR: {}\n'.format(bleu, meteor))
    print('Check en.out in data/run. Bye!', flush=True, file=stderr)
    data.infofile.close()

print('Loading example-base...', sep='', end='', flush=True, file=stderr)
data.load()
print('Done\nLoading suffix arrays...', sep='', end='', flush=True, file=stderr)
bm = ebmt._BestMatch(data.dbdir)
print('Done', flush=True, file=stderr)
run  = data.run
ini, exact = '{}/moses.ini'.format(run), {}
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
