#-*- coding:utf-8 -*-
"""prep1.py
 
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
def get_changes(entries):
 changes = []
 for entry in entries:
  metaline = entry.metaline
  lnum0 = entry.linenum1
  for iline,line in enumerate(entry.datalines):
   newline = change_line(line)
   lnum = lnum0 + iline + 1
   newline = change_line_lnum(lnum,newline)
   if newline != line:
    lnum = lnum0 + iline + 1
    change = Change(metaline,lnum,line,newline)
    changes.append(change)
 print(len(changes),'Change records generated')
 return changes

def write_changes(fileout,changes):
 outrecs = []
 for change in changes:
  outarr = []
  outarr.append('; =====================================================')
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  outarr.append('; %s' % metaline)
  lnum = change.lnum
  old = change.old
  new = change.new
  outarr.append('%s old %s' %(lnum,old))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,new))
  outrecs.append(outarr)
  
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for line in outarr:
    f.write(line+'\n')
 print(len(outrecs),"records written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1] # bur csl-orig
 fileout = sys.argv[2] #  

 entries = digentry.init(filein)
 #Ldict = digentry.Entry.Ldict

 changes = get_changes(entries)
 write_changes(fileout,changes)
 
