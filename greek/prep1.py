#-*- coding:utf-8 -*-
"""prep1.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class ABdata:
 def __init__(self,lines0,iline0):
  lnum0 = iline0 + 1
  self.lnum0 = lnum0
  lines = []
  self.comments = []
  for line in lines0:
   if line.strip() == '':
    continue
   if line.startswith('<P>'):
    continue
   if line.startswith(';'):
    self.comments.append(line)
    continue
   lines.append(line)

  if (len(lines) % 2) != 1:
   print('ABdata error 1 at %s' % lnum0)
   for line in lines:
    print(line)
   exit(1)
  m = re.search(r'^<L>(.*)$',lines[0])
  if m == None:
   print('ABdata error 2 at %s' % lnum0)
   for line in lines:
    print(line)
   exit(1)
  self.L = m.group(1).rstrip()
  self.status = True
  ## old-new pairs
  nchg = (len(lines) - 1) // 2
  changes = []
  changelines = lines[1:]
  for ichg in range(nchg):
   lineold = changelines[2*ichg]
   #m = re.search(r'^old ([^:]*): (<lang n="greek">.*?</lang>)',lineold)
   m = re.search(r'^old ([^:]*): (.*)$',lineold)
   if m == None:
    self.status = False
    print('%s ABdata error 3a' % iline0)
    return
   lnum = m.group(1)
   old = m.group(2)

   linenew = changelines[2*ichg + 1]
   m = re.search(r'^new ([^:]*): (.*)$',linenew)
   if m == None:
    self.status = False
    print('%s ABdata error 3b' % iline0)
    return
   if m.group(1) != lnum:
    self.status = False
    return
   new = m.group(2)
   changes.append((int(lnum),old,new))
  self.changes = changes
 
def generate_abdata(lines):
 iline0 = None
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   if iline0 == None:
    group = [line]
    iline0 = iline
   else:
    rec = ABdata(group,iline0)
    yield rec
    group = [line]
    iline0 = iline
  else:
   group.append(line)
 # last record
 rec = ABdata(group,iline0)
 yield rec
   
def init_abdata(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
  abrecs = generate_abdata(lines)
 recs = list(abrecs)
 print(len(recs),"records from",filein)
 return recs

class Change:
 def __init__(self,metaline,lonarr,comments):
  self.metaline = metaline
  self.lonarr = lonarr  # array lnum,oldline,newline
  self.comments = comments
  
def get_changes(abdata,entries,Ldict):
 changes = []
 problems = []
 for rec in abdata:
  if not rec.status:
   problems.append(rec)
   continue
  L = rec.L
  entry = Ldict[L]
  metaline = entry.metaline
  lnum0 = entry.linenum1
  entrylines = entry.datalines
  nentrylines = len(entrylines)
  lonarr = []
  for changerec in rec.changes:
   lnum,old,new = changerec
   ientryline = lnum - lnum0 - 1
   if not (0<=ientryline<nentrylines):
    print('ERROR: L=%s, changerec=%s' %(L,changerec))
    print(metaline)
    print('entry lnum0 = %s, nentrylines = %s' %(lnum0,nentrylines))
    print('ientryline = %s' %ientryline)
    print()
    exit(1)
   oldline = entry.datalines[ientryline]
   newline = oldline.replace(old,new)
   if newline == oldline:
    print('line unchanged',metaline)
    print('old %s %s' %(lnum,oldline))
    #print('abdata: %s' % changerec)
    continue
   lonarr.append((lnum,oldline,newline))
  change = Change(metaline,lonarr,rec.comments)
  changes.append(change)
 print(len(changes),'Change records generated')
 print(len(problems),'Change problems')
 return changes

def write_changes(fileout,changes):
 outrecs = []
 for change in changes:
  outarr = []
  outarr.append('; =====================================================')
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  outarr.append('; %s' % metaline)
  for comment in change.comments:
   outarr.append('; %s (COMMENT)' %comment)
  for lnum,old,new in change.lonarr:
   outarr.append('%s old %s' %(lnum,old))
   outarr.append('%s new %s' %(lnum,new))
   outarr.append(';')
  outrecs.append(outarr)
  
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for line in outarr:
    f.write(line+'\n')
 print(len(outrecs),"records written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1] # bur csl-orig
 fileab = sys.argv[2] # greek text from Andhrabharati
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict

 abdata = init_abdata(fileab)
 changes = get_changes(abdata,entries,Ldict)
 write_changes(fileout,changes)
 
