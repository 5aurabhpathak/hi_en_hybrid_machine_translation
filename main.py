#!/bin/env python3
#Author: Saurabh Pathak
#Main program: Stiches the pipeline together
#Usage: (main.py sourcefileneame) or (main.py sourcefile referencefile) for BLEU and METEOR or just (main.py) for a text cli :)
from subprocess import Popen, PIPE, DEVNULL
from sys import argv, stderr
import ebmt, rulebaseprior, xml_input, data, transliterate, os, shutil

def filter_rules(text):
    return #uncomment to diable filtering of rule-table
    print('Filtering rule table for faster translation (approx 10 minutes)\nThis will only happen if the file is being decoded for the first time...', end='', flush=True, file=stderr)
    shutil.rmtree(run + '/filetable', ignore_errors=True)
    #uncomment for hierarchical model
    Popen('{0}/training/filter-model-given-input.pl {1}/filetable {1}/moses.file.ini {2} -Binarizer'.format(os.environ['SCRIPTS_ROOTDIR'], run, text).split() + ['CreateOnDiskPt 1 1 4 100 2', '-Hierarchical'], stdout=DEVNULL, stderr=DEVNULL).communicate()
    #uncomment For phrase-based model
    #Popen('{0}/training/filter-model-given-input.pl {1}/filetable {1}/moses.phrase.ini {2} -Binarizer processPhraseTableMin'.format(os.environ['SCRIPTS_ROOTDIR'], run, text).split(), stdout=DEVNULL, stderr=DEVNULL).communicate()
    with open('{}/filetable/forfile'.format(run), 'w') as forfile: forfile.write(text)
    print('Done', flush=True, file=stderr)

def make_chunkset(text, tags, l, verbose=True):
    if verbose: print('Applying rules...', sep='', end='', flush=True, file=stderr)
    #chunkset = rulebaseprior.apply_rules(text, tags, l)
    chunkset = [] #uncomment this to disable rule base
    if verbose: print('Done\nEBMT is running...', sep='', end='', flush=True, file=stderr)
    #Comment following two lines to disable EBMT
    #try: chunkset.extend(ebmt.run(text, bm, l))
    #except ebmt.ExactMatchException as e: return e.info
    if verbose: print('Done', flush=True, file=stderr)
    return chunkset

def translate_sent(text, p): #interactive handler
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
    xml = xml_input.construct(chunkset, text, l, tags)
    print('Partially translated xml input:', xml, file=stderr)
    p.stdin.write('{}\n'.format(xml))
    p.stdin.flush()
    print('Moses is translating...', flush=True, file=stderr)
    smt = p.stdout.readline()
    print('Done\nTransliterating OOVs...', flush=True, file=stderr)
    print('Translated:', transliterate.translit_sent(smt))

def translate_file(text): #file handler.
    data.infofile = open('{}/info.txt'.format(run), 'w')
    data.infofile.write('Source File: {}\n'.format(text))
    print('Tagging input...', sep='', end='', flush=True, file=stderr)
    tags = rulebaseprior.tag_input_file(text)
    print('Done\nHave patience. run \'tail-f data/run/xml.out\' if you dont. :)\nApplying RBMT followed by EBMT followed by recombination on each sentence...', flush=True, file=stderr)

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
            xmltxt = xml_input.construct(chunkset, line, l, tags[i])
            if isinstance(xmltxt, list):
                sp.update({i: len(xmltxt)})
                for s in xmltxt: xml.write('{}\n'.format(s))
                continue
            xml.write('{}\n'.format(xmltxt))
    
    mlen, splen = len(exact), len(sp)
    print('\033[KDone.\nFound', mlen, 'direct matches\n{}'.format(rulebaseprior.j), 'rule(s) fired', flush=True, file=stderr)
    data.infofile.write('Sentences: {}\nEBMT found {} direct matches\n{} rule(s) fired by RBMT\n'.format(i+1, mlen, rulebaseprior.j))

    if os.path.exists('{}/filetable/forfile'.format(run)):
        forfile = open('{}/filetable/forfile'.format(run))
        if forfile.read().strip() not in {text, '*'}:
            forfile.close()
            filter_rules(text)
    else: filter_rules(text)

    print('Have patience. run \'tail-f data/run/smt.out\' if you dont. :)\nMoses is translating...', sep='', end='', flush=True, file=stderr)
    with open('{}/smtsplit.out'.format(run), 'w', encoding='utf-8') as smt: Popen('moses -f {0}/filetable/moses.ini -xml-input inclusive -mp -i {0}/xml.out'.format(run).split(), universal_newlines=True, stdout=smt).communicate()

    if splen > 0:
        print('Done\nMerging split points...', sep='', end='', flush=True, file=stderr)
        key, i, j, k, queue = list(sp.keys()), 0, 0, 0, []
        key.sort()
        with open('{}/smtsplit.out'.format(run)) as smtsplit, open('{}/smt.out'.format(run), 'w', encoding='utf-8') as smt:
            for x in smtsplit:
                if i < splen and key[i] == j:
                    if k == 0: l = sp.pop(key[i])
                    if k < l:
                        queue.append(x.strip())
                        k += 1
                    if k == l:
                        smt.write(' '.join(queue)+'\n')
                        j += 1
                        i += 1
                        k = 0
                        queue = []
                else:
                    smt.write(x)
                    j += 1
        assert len(sp) == 0
    else: shutil.copy2('{}/smtsplit.out'.format(run), '{}/smt.out'.format(run))

    #comment the following 4 lines to disable translaiteration and uncomment the fifth line
    print('Done\nTransliterating OOVs...', sep='', end='', flush=True, file=stderr)
    transliterate.translit_file('{}/smt.out'.format(run))
    data.infofile.write('OOVs: {}\n'.format(transliterate.j))
    print('Done', flush=True, file=stderr)

    #shutil.copy2('{}/smt.out'.format(run), '{}/transliterated.out'.format(run)) #uncomment this line to disable transliteration
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
        assert len(exact) == 0
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
bm = ebmt._BestMatch(data.dbdir, thresh=0.4, mx=5)
print('Done', flush=True, file=stderr)
run  = data.run
ini, exact, sp = '{}/moses.ini'.format(run), {}, {}
try: translate_file(os.path.abspath(argv[1]))
except IndexError:
    print('Starting moses...', sep='', end='', flush=True, file=stderr)
    p = Popen('moses -inputtype 0 -f {} -xml-input include -mp'.format(ini).split(), universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    while 'input-output' not in p.stderr.readline(): pass
    print('Ready\nWelcome to the SILP Hindi to English Translator!', flush=True, file=stderr)
    while True:
        try:
            text = input('Enter one Hindi sentence or ctrl+d to exit:\n')
            translate_sent(text, p)
        except EOFError:
            print('Bye!', file=stderr)
            exit(0)
