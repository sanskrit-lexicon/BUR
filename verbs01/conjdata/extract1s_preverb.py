#-*- coding:utf-8 -*-
"""extract1s_preverb.py
 Extract 1-singular present tense forms from old conjugation tables.
 This specifically for normprev-conj-spcl.txt
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

def init_conj(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Conj(x) for x in f]
 print(len(recs),"records read from",filein)
 return recs

def write(fileout,recs):
 d = {}
 a = []

 for rec in recs: # a Conj element
  k1 = rec.k1
  for conjtab in rec.conjtabs:
   if not conjtab.tenseinfo.startswith('pre-'):
    continue
   table = conjtab.table
   pre1s_list = table[6]  # 1st singular present tense
   for pre1s in pre1s_list:  # normally just one in this list
    v = (k1,pre1s)
    if v not in d:
     d[v] = True
     a.append(v)
 with codecs.open(fileout,"w","utf-8") as f:
  for k1,pre1s in a:
   f.write('%s %s P\n'%(k1,pre1s))
 n=len(a)
 print(n,"items written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  
 fileout = sys.argv[2]
 recs = init_conj(filein)
 write(fileout,recs)
