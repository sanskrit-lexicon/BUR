#-*- coding:utf-8 -*-
"""prep3.py
 
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

def write_changes(fileout,changes):
 outrecs = []
 for change  in changes:
  outarr = []
  metaline = change.metaline
  meta = re.sub(r'<k2>.*$','',metaline)
  outarr.append('; %s (sections = %s)' % (meta,change.sections))
  lnum = change.lnum
  outarr.append('%s old %s' % (lnum,change.old))
  outarr.append(';')
  outarr.append('%s new %s' % (lnum,change.new))
  outarr.append('; ========================================================')
  outrecs.append(outarr)

 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for line in outarr:
     f.write(line+'\n')
 print(len(changes),"changes written to",fileout)


if __name__=="__main__":
 #option = int(sys.argv[1])
 #assert option in range(1,8) # 1,2,..,7
 filein = sys.argv[1] # bur csl-orig
 fileout = sys.argv[2] #  

 entries = digentry.init(filein)
 changes = get_changes(entries)
 write_changes(fileout,changes)
 exit(1)
 regexes = ['[0-9]o', '[0-9]e','1re', '1er','2d','ae','AE']
 dchanges = {}
 for regex in regexes:
  dchanges[regex] = get_changes(entries,regex)
 
