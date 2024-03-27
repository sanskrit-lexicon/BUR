#-*- coding:utf-8 -*-
"""prep2.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  


class Change:
 def __init__(self,metaline,lnum,old,new):
  self.metaline = metaline
  self.lnum = lnum
  self.old = old
  self.new = new

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

def change_line(line):
 # a2. is abbreviation for 2nd aoriste
 line = line.replace('ạ.','<ab>a2.</ab>')
 line = line.replace('ạ','<ab>a2.</ab>')
 line = line.replace('Ạ.','<ab>A2.</ab>')
 # one instance
 line = line.replace("A'ler","Aller") # stfkz
 return line

def get_changes(entries,regex):
 changes = []
 for entry in entries:
  metaline = entry.metaline
  lnum0 = entry.linenum1
  for iline,line in enumerate(entry.datalines):
   if re.search(regex,line):
    lnum = lnum0 + iline + 1
    change = Change(metaline,lnum,line,line)
    changes.append(change)
 print(len(changes),'instances of regex=',regex)
 return changes

def write_changes(fileout,regexes,dchanges):
 outregs = []
 for iregex,regex in enumerate(regexes):
  changes = dchanges[regex]
  outrecs = []
  outrecs.append('; =====================================================')
  nchanges = len(changes)
  outrecs.append('; Section %s: %s instances of regex %s' %
                 (iregex+1,nchanges,regex))
  if nchanges > 10:
   outrecs.append(';  (first 10 instances shown)')
   changes1 = changes[0:10]
  else:
   changes1 = changes
  outrecs.append('; =====================================================')
  prevmeta = None
  for change  in changes1:
   metaline = change.metaline
   if prevmeta != metaline:
    meta = re.sub(r'<k2>.*$','',metaline)
    outrecs.append('; %s' % meta)
    prevmeta = metaline
   line = change.old
   outrecs.append(line)
   outrecs.append(';')

  outregs.append(outrecs)
 
 with codecs.open(fileout,"w","utf-8") as f:
  for outrecs in outregs:
   for line in outrecs:
     f.write(line+'\n')
 print(len(outregs),"record groups written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1] # bur csl-orig
 fileout = sys.argv[2] #  

 entries = digentry.init(filein)
 regexes = ['[0-9]o', '[0-9]e','1re', '1er','2d','ae','AE']
 dchanges = {}
 for regex in regexes:
  dchanges[regex] = get_changes(entries,regex)
 write_changes(fileout,regexes,dchanges)
 
