#!/bin/env python3
#Author: Saurabh Pathak
#Web app - Simple
import main, flask as fl, os
app = fl.Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 102400

@app.route('/')
def hello_world(): return fl.render_template('index.html')

@app.route('/file', methods = ['POST', 'GET'])
def trans():
    if fl.request.method == 'POST':
        f = fl.request.files
        f1, f2 = f['f1'], f['f2']
        if f1.filename == '':
            fl.flash('No selected file')
            return fl.redirect('/')
        with open('/tmp/hi.txt', 'w', encoding='utf-8') as inp:
            for i, line in enumerate(f1):
                line = line.decode('utf-8')
                if len(line.split()) > 30:
                    fl.flash('Sentence {} is larger than limit'.format(i+1))
                    return fl.redirect('/')
                inp.write(line)
        if f2.filename != '':
            with open('/tmp/en.txt', 'w', encoding='utf-8') as ref: ref.write(f2.read().decode('utf-8'))
            main.ref = '/tmp/en.txt'
        main.translate_file('/tmp/hi.txt')
    with open(main.run +  '/info.txt') as f: results = f.read().splitlines()
    return fl.render_template('results.html', result=results)

@app.route('/en', methods = ['GET'])
def out():
    with open('/tmp/hi.txt') as f, open(main.run +  '/en.out') as e: inp, out = f.read().splitlines(), e.read().splitlines()
    return fl.render_template('translated.html', out=list(zip(inp, out)))

@app.route('/text', methods = ['POST'])
def txt():
    txt = fl.request.form['text']
    if txt == '':
        fl.flash('No input given')
        return fl.redirect('/')
    if len(txt) > 5000:
        fl.flash('Text input limit exceeded')
        return fl.redirect('/')
    with open('/tmp/hi.txt', 'w', encoding='utf-8') as inp:
        for i, line in enumerate(txt.splitlines()):
            if len(line.split()) > 30:
                fl.flash('Sentence {} is larger than limit'.format(i+1))
                return fl.redirect('/')
            print(line, file=inp)
    main.translate_file('/tmp/hi.txt')
    with open(main.run +  '/info.txt') as f: results = f.read().splitlines()
    return fl.render_template('results.html', result=results)

if __name__ == '__main__':
    main.load_data() #do not run with debug=True with this line. Causes memory issues
    app.run('0.0.0.0', 5000)
    #app.run('172.17.25.252', 5000, debug=True)
