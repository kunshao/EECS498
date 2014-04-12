import re
import os, sys
import porterstemmer
    
sub_dir = "fqueryApp"

def openFile(fname):
    fh = None
    try:
        fh = open(fname)
    except:
        print "Cannot open file:", fname
    return fh


def importStopwords():
    fname = "stopwords"
   
    fh = openFile(os.path.join(sub_dir,fname))
    stopwords = list()

    if fh is None: return stopwords

    for stopword in fh:
        stopword = stopword.rstrip()
        stopwords.append(stopword)
    fh.close()
    return stopwords

def stemword(token):
    ps = porterstemmer.PorterStemmer()
    output = ''
    word = ''
    token += ' '
    for c in token:
        if c.isalpha():
            word += c.lower()
        else:
            if not word == ' ':
                output += ps.stem(word, 0, len(word)-1)
                word = ''
            output += c.lower() 
    output = output.rstrip()
    return output

def processLine(line):

    tokens = list()
   # elimination of newline character
    line = line.rstrip()
    # elimination of SGML tags
    if not re.search(r'^<\S+>$', line):
        # get lowercase
        line = line.lower()
        # tokenization of @#%&*\()
        line = re.sub(r'[\[\]<>"@#%&*\\()?!+=]+', r' ', line)
        if re.search(r'[a-z]+[\/.][a-z]+', line):
            line = re.sub(r'\/', r' ', line)
        if re.search(r'--', line):
            line = re.sub(r'--', r' ', line)

        for token in line.split():

            # tokenization of 's and s'         
            if re.search(r'\'s$', token) or re.search(r's\'$', token):
                tokens.append('\'s')

            if re.search(r'\'s$', token):
                token = re.sub(r'\'s', r'', token)
            elif re.search(r's\'$', token):
                token = re.sub(r'\'', r'', token)   

            # tokenization of '' as emphasis
            if re.search(r'\'*.*\'*', token):
                token = re.sub(r'\'', r'', token)

            token = token.strip('[.,-:;/\\]')

            if token == '':
                continue 

            tokens.append(token)  

    return tokens
