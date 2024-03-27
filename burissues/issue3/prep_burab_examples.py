#-*- coding:utf-8 -*-
"""prep_burab_examples.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class ABtip:
 def __init__(self,line):
  
  m = re.search(r'^(.*)<(.*?)>(.*)</.*?> *\(([0-9]+)\)$',line)
  self.ab = m.group(1).rstrip()
  self.tipcode = m.group(2)
  assert self.tipcode in ['tip','TIP']
  self.tip = m.group(3)
  self.count = int(m.group(4))
  
def init_burab(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [ABtip(line.rstrip('\r\n'))for line in f]
 print(len(recs),"tooltips read from",filein)
 return recs

def simplify(x):
 removals = ['{%','%}','{#','#}','<ab>','</ab>','<lbinfo.*?/>',
             '<lang n="greek">','</lang>','{@','@}']
 for regex in removals:
  x = re.sub(regex,'',x)
 return x

def entrylines(entry,abmatch):
 outarr = []
 text = ' '.join(entry.datalines)
 # first match
 index = text.find(abmatch)
 if index == -1:
  return outarr
 a = text[0:index]
 b = text[index+len(abmatch):]
 a1 = simplify(a)
 b1 = simplify(b)
 a2 = a1[-30:]
 b2 = b1[0:30]
 meta = re.sub('<k2>.*$','',entry.metaline)
 outarr.append(meta)
 outarr.append(a2 + abmatch + b2)
 outarr.append(';')
 return outarr

def init_examples(abrecs,entries):
 outrecs = []
 abrecs1 = [rec for rec in abrecs if rec.tipcode == 'TIP']
 for irec,rec in enumerate(abrecs1):
  abmatch = '<ab>%s</ab>' % rec.ab
  outarr = []
  outarr.append('; ' + ('"'*70))
  outarr.append('')
  outarr.append('; ' + ('"'*70))
  count = rec.count
  n = 0
  for entry in entries:
   lines = entrylines(entry,abmatch)
   if lines != []:
    for line in lines:
     outarr.append(line)
    n = n + 1
    if n == count:
     break
    if n == 10: # stop at 10 examples per abbreviation
     break
   case = irec + 1
   if count == 1:
    outarr[1] = '; Case %s: Abbreviation %s occurs %s time' % (case,rec.ab,count)
   else:
    outarr[1] = '; Case %s: Abbreviation %s occurs %s times' % (case,rec.ab,count)
  outrecs.append(outarr)
 return outrecs

def write_examples(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for line in outarr:
    f.write(line+'\n')
 print(len(outrecs),"examples written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] # prep_burab
 filein1 = sys.argv[2] # temp_bur_6
 fileout = sys.argv[3] #  

 abrecs = init_burab(filein)
 entries = digentry.init(filein1)
 outrecs = init_examples(abrecs,entries)
 write_examples(fileout,outrecs)

