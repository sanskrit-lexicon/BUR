#-*- coding:utf-8 -*-
"""extract2_preverb.py
 Extract 1-singular present tense forms from old conjugation tables.
 This specifically for normprev-conj-spcl.txt
 Make some corrections
"""
from __future__ import print_function
import sys, re,codecs

class Conjtab(object):
 def __init__(self,part):
  m = re.search(r'^(.*?):(.*?) (.*?) (.*)$',part)
  self.k1 = m.group(1)
  self.k2 = m.group(2)
  self.tenseinfo = m.group(3)
  tabstr = m.group(4)
  tab = tabstr.split(':')
  t = []
  for x in tab:
   parts = x.split('/')  # alternates separated by '/'
   t.append(parts)   # 
  self.table = t  # a list of lists; 
  # some checks
  assert len(t) == 9  # conjugation table length
 
class Conj(object):
 def __init__(self,line):
  """
   MW-xxxxxxx.xx\t<form>x1</form><form>x2</form>
  """
  line = line.rstrip()
  m = re.search('MW-(.*?)\t(.*)$',line)
  self.L0= m.group(1)
  data = m.group(2)
  data = re.sub(r'^<form>','',data)
  data = re.sub(r'</form>$','',data)
  parts = data.split('</form><form>')
  
  self.conjtabs = [Conjtab(part) for part in parts]
  # checks
  hws = [tab.k1 for tab in self.conjtabs]
  assert len(set(hws)) == 1
  self.k1 = hws[0]
  k2s = [tab.k2 for tab in self.conjtabs]
  assert len(set(k2s)) == 1
  self.k2 = k2s[0]
  parts = self.k2.split('-')
  self.pfxes = '+'.join(parts[0:-1])
  self.verb = parts[-1]
  self.parse = '+'.join(parts)

def init_conj(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Conj(x) for x in f]
 print(len(recs),"records read from",filein)
 return recs

def corrections(x):
 # correct conjugation errors
 y = x
 regexes = [
  ('praC','pfcC'),
 ]
 for old,new in regexes:
  y1 = re.sub(old,new,y)
  if y1 != y:
   y = y1
   print('Correction: %s -> %s'%(x,y))
   break
 return y

def write(fileout,recs):
 d = {}
 a = []

 for rec in recs: # a Conj element
  k1 = rec.k1
  k2 = rec.k2
  parse = rec.parse
  for conjtab in rec.conjtabs:
   if not conjtab.tenseinfo.startswith('pre-'):
    continue
   table = conjtab.table
   pre1s_list = table[6]  # 1st singular present tense
   for pre1s in pre1s_list:  # normally just one in this list
    pre1s_corr = corrections(pre1s)
    v = (k1,pre1s_corr,parse)
    if v not in d:
     d[v] = True
     a.append(v)
 with codecs.open(fileout,"w","utf-8") as f:
  for k1,pre1s,parse in a:
   f.write('%s %s P %s\n'%(k1,pre1s,parse))
 n=len(a)
 print(n,"items written to",fileout)

def write1(fileout,recs):
 d = {}
 a = []

 e = {}
 for rec in recs: # a Conj element
  k1 = rec.k1
  k2 = rec.k2
  parts = k2.split('-')
  pfxes = parts[0:-1]
  verb = parts[-1]
  rec.pfxes = pfxes
  rec.verb = verb
  if verb not in e:
   e[verb] = []
  e[verb].append(rec)

 verbs = sorted(e.keys())
 for verb in verbs:
  vrecs = e[verb]  # all records with this verb
  
  vpfxes = ['%s+%s'%('+'.join(r.pfxes),verb) for r in vrecs]
  a = a + vpfxes
 with codecs.open(fileout,"w","utf-8") as f:
  for vpfx in a:
   f.write(vpfx + '\n')
 n=len(a)
 print(n,"items written to",fileout)


if __name__=="__main__": 
 filein = sys.argv[1] #  
 fileout = sys.argv[2]
 recs = init_conj(filein)
 write(fileout,recs)
 #write1(fileout,recs)
