#-*- coding:utf-8 -*-
"""prep5a.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class Change:
 def __init__(self,metaline,lnum,old,new,sections):
  self.metaline = metaline
  self.lnum = lnum
  self.old = old
  self.new = new
  self.sections = sections  # index the changes to this line
  
def change_line_lnum(lnum,line):
 d = {
  130990: ("A'ler","Aller"),
  663: ('agrata(s)sara','agratassara'),
  18798: ('(s)','{%s%}'),
  31161:('pṛṣṭhata(s)','pṛṣṭhatas'),
  73410:('sukhadu(s)kānām','sukhaduskānām'),  # ODDity of BUR 
  79159:('yatas(s) pravṛtti(s)','yatas pravṛttis'),
  86888: ('mana(s)prasāda','manasprasāda'),
  86890: ('mana(s)śila','manasśila'), 
  86892: ('mana(s)sila','manassila'), 
  88419: ('bhuva(s)','bhuvas'),   
 107281: ('vilubhila(s)','vilubhilas'), 
 114875: ('daṇḍa(s)','daṇḍas'),  
 119369: ('śloka(s)','ślokas'), 
 119371: ('divya(s) pāyu(s)','divyas pāyus'), 
 120094: ('sadya(s)śotā','sadyasśotā'), 
 122503: ('aha(s)','ahas'), 
 125035: ('ka(s)','kas'), 
 131758: ('eka(s)','ekas'),  
 132038: ('śira(s)','śiras'),
 132470: ('āpa(s)','āpas'),
 134781: ('ahā(s)','ahās'), 
 134788: ('jabhru(s)','jabhrus'),
     54: ('8c','8e'),
  
 }
 if lnum not in d:
  return line
 old,new = d[lnum]
 newline = line.replace(old,new)
 return newline

num_subs = [(r'([0-9])o',r'\1°',1), # section 1
         (r'1re',r'1ʳᵉ',3), # section 3
         (r'1er',r'1ᵉʳ',4), # section 4
         (r'([0-9])e',r'\1ᵉ',2), # section 2
         (r'2d',r'2ᵈ',5), #Section 5
            (r'AE',r'Æ',7), #section 7
        ]
def change_num_sfx(line):
 sections = []
 newline = line
 for sub in num_subs:
  regold,replace,section = sub
  newline1 = re.sub(regold,replace,newline)
  if newline1 != newline:
   sections.append(section)
  newline = newline1
 return newline,sections

def change_ae(line):
 newline = line.replace('Jaena','Jaïna')
 newline = newline.replace('ae','æ') # some will be manually changed later
 return newline
def get_change_line(line,iline):
 newline,sections = change_num_sfx(line)
 newline1 = change_ae(newline)
 if newline1 != newline:
  sections.append(7)
 newline = newline1
 return newline,sections

def get_changes(entries):
 changes = []
 section_count = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
 for entry in entries:
  metaline = entry.metaline
  lnum0 = entry.linenum1
  for iline,line in enumerate(entry.datalines):
   newline,sections = get_change_line(line,iline)
   if newline != line:
    lnum = lnum0 + iline + 1
    change = Change(metaline,lnum,line,newline,sections)
    changes.append(change)
    for section in sections:
     section_count[section] = section_count[section] + 1
 for section in section_count:
  print('%3d changes of section type %d' %(section_count[section],section))
 return changes

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
  else:
   flag = '!='
  outline = '%04d %s %04d %s' %(n,flag,nab,key)
  outarr.append(outline)

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
def check_L(entries,entriesab):
 n = len(entries)
 nab = len(entriesab)
 assert n == nab
 for i,e in enumerate(entries):
  eab = entriesab[i]
  L = e.metad['L']
  Lab = eab.metad['L']
  assert L == Lab
  #assert k1 == k1ab
 #print('check_L: both files have same sequence of L-numbers')

def get_ablist(e,regex):
 text = '\n'.join(e.datalines)
 ans = re.findall(regex,text)
 return ans

def get_diffs(abbrev,entries,entriesab):
 ans = []
 abbrev1 = abbrev.replace('.','[.]') 
 regexraw = r'<ab>%s</ab>' % abbrev1
 regex = re.compile(regexraw)
 nprob = 0
 for i,e in enumerate(entries):
  eab = entriesab[i]
  x1 = get_ablist(e,regex)
  x2 = get_ablist(eab,regex)
  n1 = len(x1)
  n2 = len(x2)
  if n1 == n2:
   continue
  nprob = nprob + 1
  L = e.metad['L']
  pc = e.metad['pc']
  out = '%s %s %s %s' % (L,n1,n2,pc)
  print(out)
 print('%s problems found for <ab>%s</ab>' %(nprob,abbrev))
if __name__=="__main__":
 abbrev = sys.argv[1]
 filein = sys.argv[2] # bur.txt
 filein1 = sys.argv[3] # AB version of burnouf dictionary
 fileout = sys.argv[4] #  

 entries = digentry.init(filein)
 digentry.Entry.Ldict = {}
 entriesab = init_burab(filein1)
 check_L(entries,entriesab)
 diffs = get_diffs(abbrev,entries,entriesab)
 exit(1)
 freq = abbrev_freq(entries)
 freqab = abbrev_freq(entriesab)
 write_abbrevs(fileout,freq, freqab)

