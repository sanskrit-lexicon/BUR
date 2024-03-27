#-*- coding:utf-8 -*-
"""prep5.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

def get_keys(d1,d2):
 k1 = set(d1.keys())
 k2 = set(d2.keys())
 keys = k1.union(k2)
 keys1 = sorted(keys,key = lambda x: x.lower())
 return keys1
def write_abbrevs(fileout,freq,freqab):
 keys = get_keys(freq,freqab)
 print(len(keys),'keys')
 outarr = []
 nok = 0
 nprob = 0
 for key in keys:
  if key in freq:
   n = freq[key]
  else:
   n = 0
  if key in freqab:
   nab = freqab[key]
  else:
   nab = 0
  if n == nab:
   flag = '=='
   nok = nok + 1
  else:
   flag = '!='
   nprob = nprob + 1
  outline = '%04d %s %04d %s' %(n,flag,nab,key)
  outarr.append(outline)
 print('%s abbreviations occur same number of times' % nok)
 print('%s abbreviations occur different number of times' % nprob)
 
 with codecs.open(fileout,"w","utf-8") as f:
  for line in outarr:
   f.write(line+'\n')
 print(len(outarr),"abbreviations written to",fileout)

def init_burab(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 newlines = []
 for line in lines:
  parts = line.split('\t')
  for part in parts:
   newlines.append(part)

 entries = digentry.init(filein,linesin = newlines)
 return entries

def abbrev_freq(entries):
 d = {}
 n = 0
 for entry in entries:
  for line in entry.datalines:
   abbrevs = re.findall(r'<ab>.*?</ab>',line)
   n = n + len(abbrevs)
   for abbrev in abbrevs:
    if abbrev not in d:
     d[abbrev] = 0
    d[abbrev] = d[abbrev] + 1
 print('# abbrev codes = %s, Total abbrevs = %s' %(len(d.keys()),n))
 return d
if __name__=="__main__":
 filein = sys.argv[1] # bur.txt
 filein1 = sys.argv[2] # AB version of burnouf dictionary
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 digentry.Entry.Ldict = {}
 entriesab = init_burab(filein1)
 freq = abbrev_freq(entries)
 freqab = abbrev_freq(entriesab)
 write_abbrevs(fileout,freq, freqab)

