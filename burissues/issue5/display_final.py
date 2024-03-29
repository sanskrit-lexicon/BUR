# coding=utf-8
""" display_final.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"from",filein)
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')  
 print(len(lines),"lines written to",fileout)

class AB_BUR:
 def __init__(self,line):
  self.line = line
  (self.ab,self.body) = line.split('\t')
  m = re.search(r'^<id>(.*?)</id> <disp>(.*?)</disp>',self.body)
  if m == None:
   print('WAAB_BUR format error',line)
   exit(1)
  self.abid = m.group(1)
  self.disp = m.group(2)
  if self.ab != self.abid:
   print('error: "%s" != "%s"' % (self.ab,self.abid))
   exit(1)
  self.count = 0
  self.contexts = []
  
def init_ab_input(lines):
 recs = []
 for line in lines:
  rec = AB_BUR(line)
  recs.append(rec)
 # dictionary on rec.ab
 d = {}
 for rec in recs:
  ab = rec.ab
  if ab in d:
   print('duplicate ab: "%s"' %ab)
  d[ab] = rec
 return recs,d

def get_abbrevs(lines):
 d = {}  # count of all abbrevs
 for line in lines:
  for m in re.finditer(r'<ab>(.*?)</ab>',line):
   ab = m.group(1)
   if ab not in d:
    d[ab] = 0
   d[ab] = d[ab] + 1
 return d

def update_contexts(entries,tipdict):
 for ientry,entry in enumerate(entries):
  lines = entry.datalines
  for iline,line in enumerate(lines):
   for m in re.finditer(r'<ab>(.*?)</ab>',line):
    ab = m.group(1)
    if ab not in tipdict:
     print('ERROR: tip not found',ab,entry.metaline)
     exit(1)
    tiprec = tipdict[ab]
    tiprec.count = tiprec.count + 1
    # gather information for context
    iline1 = max(0,iline - 1)
    nlines = len(entry.datalines)
    iline2 = min(nlines-1,iline + 1)
    contextlines = entry.datalines[iline1:iline2+1]
    context = (entry.metaline,contextlines)
    tiprec.contexts.append(context)

def write_tooltips(fileout,tiprecs):
 tips = sorted(tiprecs,key = lambda rec: rec.ab.lower())
 outarr = []
 for tip in tips:
  out = '%s\t<id>%s</id> <disp>%s</disp>' %(tip.ab,tip.ab,tip.disp)
  out = '%s\t<id>%s</id> <disp>%s</disp> <count>%s</count>' %(tip.ab,tip.ab,tip.disp,tip.count)
  outarr.append(out)
 write_lines(fileout,outarr)

def tiprecs_used(alltips):
 tips_used = []
 tips_unused = []
 for tip in alltips:
  if tip.count == 0:
   tips_unused.append(tip)
  else:
   tips_used.append(tip)
 print(len(tips_unused),"unused tips removed")
 for tip in tips_unused:
  print(tip.line)
 return tips_used

if __name__=="__main__":
 filein = sys.argv[1]   # bur.txt
 filein1 = sys.argv[2] # burab_input
 fileout = sys.argv[3]  # a display of TODO tooltips
 entries = digentry.init(filein)
 lines1 = read_lines(filein1)
 tiprecs,tipdict = init_ab_input(lines1)
 # abbrevs_dict = get_abbrevs(lines)  # all <ab>X</ab> with counts
 update_contexts(entries,tipdict)  # revises tiprec records for 'TODO'
 tiprecs = tiprecs_used(tiprecs)
 write_tooltips(fileout,tiprecs)
 #write_contexts(fileout,tiprecs)

