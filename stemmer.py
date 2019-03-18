import sys
import os
import argparse
import re

class PorterStemmer: 
    mapping = {'p':'b','t':'d','c':'g','r':'rh','l':'ll','b':'f','m':'f'}
    unvoiced_stop = ['p','t','c']
    voiced_stop = ['b','d','g']
    dau_letters = ['ph','rh','ll','th','dd']
    
    def isCons(self, letter):
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u' or letter == 'y' or letter == 'w':
            return False            
        else:
            return True

    def isConsonant(self, word, i):
        letter = word[i]
        if self.isCons(letter):
            if letter == 'w':
                if(word[i-1]=='y'):
                    return False
                if(isCons(word[i-1]) and isCons(word[i+1])):
                    return False
                if(word[i-1]=='g' and word[i+1]=='y'):
                    return True
            else:
                return True
        else:
            return False

    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))
    
    # S*
    def startsWith(self, stem, letter):
        if stem.startswith(letter):
            return True
        else:
            return False

    # *S
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False

    # *v*
    def containsVowel(self, stem):
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def getForm(self, word):
        form = []
        formStr = ''
        for i in range(len(word)):
            if self.isConsonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for j in form:
            formStr += j
        return formStr

    def getM(self, word):
        form = self.getForm(word)
        m = form.count('VC')
        return m

    def replace(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced
    
    def replaceStart(self, orig, rem, rep):
        result = orig.find(rem)+len(rem)
        base = orig[result:]
        replaced = rep + base
        return replaced

    def replaceM0(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replaceM1(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig
    
    def valid_unmutated(self,unmutated):
        #print('Is valid? ',unmutated)
        if(unmutated[:2] in self.dau_letters):
            if(self.isVowel(unmutated,3) or unmutated[3] in ('r','l')):
                return True
            else:
                return False
        elif(unmutated[0] in self.unvoiced_stop and unmutated[1] in self.voiced_stop):
            return False
        elif(unmutated[0]=='g' and self.isConsonant(unmutated,1)):
            return False
        else:
            return True            
           
    
    def choose_unmutated(self, word,unmutated_candidates):
        unmutated = unmutated_candidates[0][0]
        if(len(unmutated_candidates) > 1):
            for candidate in unmutated_candidates:
               #print('Candidate: ',candidate)
               if(not self.valid_unmutated(candidate[0])):
                   continue
               elif(candidate[1]=='sm' and candidate[0].startswith('g')):
                   if(self.isVowel(word,0) or word[0]=='w' or word[0]=='y'):
                       unmutated = candidate[0]
                       break
                   else:
                       continue                     
               elif(candidate[1]=='sm' and candidate[0].startswith('b')):
                   unmutated = candidate[0]
                   continue
               elif(candidate[1]=='sm' and candidate[0].startswith('m')):
                   unmutated += '|'+candidate[0]
                   break
               else:
                   unmutated = candidate[0]
                   break       
        return unmutated  
           

    def step1a(self, word):
        for punct in ['!','.',',',';','?']:
            if(word.endswith(punct)):
                word = self.replace(word,punct[0] ,'')
        if(self.getM(word)>1):
            if(word.startswith('cyd') or word.startswith('gwrth') or word.startswith('hunan') or word.startswith('rhag') or word.startswith('ym') or word.startswith('af') or word.startswith('di') or word.startswith('an') or word.startswith('am') or word.startswith('ad') or word.startswith('cyf') or word.startswith('tra')):
                if(word.startswith('cyd-') or word.startswith('gwrth-') or word.startswith('hunan-') or word.startswith('rhag-') or word.startswith('ym-') or word.startswith('af-') or word.startswith('di-') or word.startswith('an-') or word.startswith('am-') or word.startswith('ad-') or word.startswith('cyf-') or word.startswith('tra-')):
                    if(word.startswith('cyd-')):
                        word = self.replaceStart(word,'cyd-','')
                    elif(word.startswith('gwrth-')):
                        word = self.replaceStart(word,'gwrth-','')
                    elif(word.startswith('hunan-')):
                        word = self.replaceStart(word,'hunan-','')
                    elif(word.startswith('rhag-')):
                        word = self.replaceStart(word,'rhag-','')
                    elif(word.startswith('ym-')):
                        word = self.replaceStart(word,'ym-','')
                    elif(word.startswith('af-')):
                        word = self.replaceStart(word,'af-','')
                    elif(word.startswith('di-')):
                        word = self.replaceStart(word,'di-','')
                    elif(word.startswith('an-')):
                        if(word.startswith('an-gh')):
                            word = self.replaceStart(word,'an-gh','ngh')
                        else:
                            word = self.replaceStart(word,'an-','')
                    elif(word.startswith('am-')):
                        if(word.startswith('am-h')):
                            word = self.replaceStart(word,'am-h','mh')
                    elif(word.startswith('ad-')):
                        word = self.replaceStart(word,'ad-','')
                    elif(word.startswith('cyf-')):
                        word = self.replaceStart(word,'cyf-','')
                    elif(word.startswith('tra-')):
                        word = self.replaceStart(word,'tra-','')
                    else:
                        pass
                else:
                    if(word.startswith('cyd')):
                        word = self.replaceStart(word,'cyd','')
                    elif(word.startswith('gwrth')):
                        word = self.replaceStart(word,'gwrth','')
                    elif(word.startswith('hunan')):
                        word = self.replaceStart(word,'hunan','')
                    elif(word.startswith('rhag')):
                        word = self.replaceStart(word,'rhag','')
                    elif(word.startswith('ym')):
                        word = self.replaceStart(word,'ym','')
                    elif(word.startswith('af')):
                        word = self.replaceStart(word,'af','')
                    elif(word.startswith('di')):
                        word = self.replaceStart(word,'di','')
                    elif(word.startswith('an')):
                        if(word.startswith('angh')):
                            word = self.replaceStart(word,'angh','ngh')
                        else:
                            word = self.replaceStart(word,'an','')
                    elif(word.startswith('am')):
                        if(word.startswith('amh')):
                            word = self.replaceStart(word,'amh','mh')
                    elif(word.startswith('ad')):
                        word = self.replaceStart(word,'ad','')
                    elif(word.startswith('cyf')):
                        word = self.replaceStart(word,'cyf','')
                    elif(word.startswith('tra')):
                        word = self.replaceStart(word,'tra','')
                    else:
                        pass
               
                unmutated_candidates = self.lookup_mutation(word)
                #print(unmutated_candidates)
                word = self.choose_unmutated(word,unmutated_candidates)
        else:
            pass
        return word

    def step2(self, word):
        if word.endswith('ational'):
            word = self.replaceM0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replaceM0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replaceM0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replaceM0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replaceM0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replaceM0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replaceM0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replaceM0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replaceM0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replaceM0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replaceM0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replaceM0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replaceM0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replaceM0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replaceM0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replaceM0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replaceM0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replaceM0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replaceM0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replaceM0(word, 'biliti', 'ble')
        return word

    def step3(self, word):
        if word.endswith('icate'):
            word = self.replaceM0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replaceM0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replaceM0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replaceM0(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            word = self.replaceM0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replaceM0(word, 'ness', '')
        return word

    def step4(self, word):
        if word.endswith('al'):
            word = self.replaceM1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replaceM1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replaceM1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replaceM1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replaceM1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replaceM1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replaceM1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replaceM1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replaceM1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replaceM1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replaceM1(word, 'ent', '')
        elif word.endswith('ou'):
            word = self.replaceM1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replaceM1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replaceM1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replaceM1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replaceM1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replaceM1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replaceM1(word, 'ize', '')
        elif word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.getM(base) > 1 and (self.endsWith(base, 's') or self.endsWith(base, 't')):
                word = base
            word = self.replaceM1(word, '', '')
        return word
    
    def lookup_mutation(self,input_token):
        """ Return a list of all possible Welsh mutations of a given token """
        token = input_token.lower()
        unmutated = []
        if token[:2] == "ch":
            unmutated.append(("c{}".format(token[2:]), "am"))
        if token[:2] == "ph":
            unmutated.append(("p{}".format(token[2:]), "am"))
        if token[:2] == "th":
            unmutated.append(("t{}".format(token[2:]), "am"))
        if token[:3] == "ngh":
            unmutated.append(("c{}".format(token[3:]), "nm"))
        if token[:2] == "mh":
            unmutated.append(("p{}".format(token[2:]), "nm"))
        if token[:2] == "nh":
            unmutated.append(("t{}".format(token[2:]), "nm"))
        if token[:2] == "ng":
            unmutated.append(("g{}".format(token[2:]), "nm"))
        if token[:1] == "m":
            unmutated.append(("b{}".format(token[1:]), "nm"))
        if token[:1] == "n":
            unmutated.append(("d{}".format(token[1:]), "nm"))
        if token[:2] == "rh":
            unmutated.append(("tr{}".format(token[2:]), "nm"))
        if token[:1] == "g":
            unmutated.append(("c{}".format(token[1:]), "sm"))
        if token[:1] == "b":
            unmutated.append(("p{}".format(token[1:]), "sm"))
        if token[:1] == "d":
            unmutated.append(("t{}".format(token[1:]), "sm"))
        if token[:1] == "f":
            unmutated.append(("b{}".format(token[1:]), "sm"))
            unmutated.append(("m{}".format(token[1:]), "sm"))
        if token[:1] == "l":
            unmutated.append(("ll{}".format(token[1:]), "sm"))
        if token[:1] == "r":
            unmutated.append(("rh{}".format(token[1:]), "sm"))
        if token[:2] == "dd":
            unmutated.append(("d{}".format(token[2:]), "sm"))
        if token[:2] == "ha":
            unmutated.append(("a{}".format(token[2:]), "hm"))
        if token[:2] == "he":
            unmutated.append(("e{}".format(token[2:]), "hm"))
        if token[:2] == "hi":
            unmutated.append(("i{}".format(token[2:]), "hm"))
        if token[:2] == "ho":
            unmutated.append(("o{}".format(token[2:]), "hm"))
        if token[:2] == "hu":
            unmutated.append(("u{}".format(token[2:]), "hm"))
        if token[:2] == "hw":
            unmutated.append(("w{}".format(token[2:]), "hm"))
        if token[:2] == "hy" and token != "hyn":
            unmutated.append(("y{}".format(token[2:]), "hm"))
        unmutated.append(("g{}".format(token), "sm"))
        if input_token[0].isupper():
            capitals = []
            for mutation in unmutated:
                    capitals.append(("{}{}".format(mutation[0][:1].upper(), mutation[0][1:]), mutation[1]))
            unmutated = unmutated + capitals
        return(unmutated)

    def stem(self, word):
        word = self.step1a(word)
        return word

stemmer = PorterStemmer()
with open(sys.argv[1],"r") as f:
    content = f.read().strip().split()
    for token in content:
        token = token.lower()
        stem_output = stemmer.stem(token)
        print('Token :',token,' ==> Stem: ',stem_output)
