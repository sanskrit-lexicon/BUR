#-*- coding:utf-8 -*-
"""prep_burab.py
 
"""
from __future__ import print_function
import sys,re,codecs

class ABtip:
 def __init__(self,line):
  self.ab,self.data = line.split('\t')
  m = re.search(r'<id>(.*?)</id> *<disp>(.*?)</disp>',self.data)
  self.data_id = m.group(1)
  self.data_disp = m.group(2)
  # check
  if self.ab != self.data_id:
   print('ABtip warning: ',line)
  self.count = None
  
def init_burab(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [ABtip(line.rstrip('\r\n'))for line in f]
 print(len(recs),"tooltips read from",filein)
 # return dictionary
 d = {}
 for rec in recs:
  ab = rec.ab
  if ab in d:
   print('init_burab: duplicate',ab)
  d[ab] = rec
 return d

class ABcount:
 def __init__(self,line):
  # 0037 == 0037 <ab>A.</ab>
  m = re.search(r'([0-9]+) (..) ([0-9]+) <ab>(.*?)</ab>',line)
  self.count = m.group(1)
  self.ab = m.group(4)
  status = m.group(2)
  n = m.group(3)
  if (n != self.count) or (status != '=='):
   print('ABcount warning:',line)

def init_abc(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [ABcount(line.rstrip('\r\n'))for line in f]
 print(len(recs),"abbreviation counts",filein)
 # return dictionary
 d = {}
 for rec in recs:
  ab = rec.ab
  if ab in d:
   print('init_abc: duplicate',ab)
  d[ab] = rec
 return d

def check1(tipsd,abcd):
 nprob = 0
 for ab in tipsd:
  if ab not in abcd:
   tip = tipsd[ab]
   print('check1 warning:',tip.ab, tip.data)
   nprob = nprob + 1
 print('check1 identifies %s problems' % nprob)

def get_allabs(tipsd,abcd):
 keys1 = set(tipsd.keys())
 keys2 = set(abcd.keys())
 keys = keys1.union(keys2)
 print(len(keys1),len(keys2),len(keys))
 if True:
  a = []
  for key in keys:
   x = re.sub(r'[a-zA-Z. 123?-]','',key)
   for y in x:
    if y not in a:
     a.append(y)
  print('extra characters',a)

 newkeys = {}
 replacements = [
   ('à','a'), ('é','e'), ('ç','c'), ('â','a'), ('É','E'), ('Ê','E'), ('ë','e'),
  ]
 for key in keys:
  newkey = key
  for old,new in replacements:
   newkey = newkey.replace(old,new)
  newkeys[key] = newkey
  
 keys = sorted(keys, key = lambda x: newkeys[x].lower())
 return keys

def write_abedit(fileout,tipsd,abcd):
 allabs = get_allabs(tipsd,abcd)
 outarr = []
 for ab in allabs:
  if ab in abcd:
   count = int(abcd[ab].count)
  else:
   count = 0
  if ab in tipsd:
   disp = tipsd[ab].data_disp
   tip = 'tip'
  else:
   disp = ''
   tip = 'TIP'
  out = '%s <%s>%s</%s> (%s)' %(ab.ljust(10),tip,disp,tip,count)
  outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for line in outarr:
   f.write(line+'\n')
 print(len(outarr),"abbreviations written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] # burab_input
 filein1 = sys.argv[2] # prep5_bur5
 fileout = sys.argv[3] #  

 tipsd = init_burab(filein)
 abcd = init_abc(filein1)  # abbreviation counts
 check1(tipsd,abcd)  # are all tip abbreviations used?
 write_abedit(fileout,tipsd,abcd)

