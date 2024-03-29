# coding=utf-8
""" cap_ab.py
"""
from __future__ import print_function
import sys, re,codecs

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
  self.count = 0 # number of instances in bur.txt
  
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

def write_changes_helper(c):
 outarr = []
 #outarr.append('; %s cat=%s' % (c.metaline,c.cat))
 outarr.append('; %s' % c.metaline)
 # auto-comment-out some changes
 if c.cat.endswith('nochg'):
  outarr.append('; %s old %s' %(c.lnum,c.old))
  outarr.append(';')
  outarr.append('; %s new %s' %(c.lnum,c.new))
 else:
  outarr.append('%s old %s' %(c.lnum,c.old))
  outarr.append(';')
  outarr.append('%s new %s' %(c.lnum,c.new))
 outarr.append('; ----------------------------------------------')
 return outarr

def write_changes(fileout,changes,option):
 outrecs = []
 cats = []
 for c in changes:
  if c.cat not in cats:
   cats.append(c.cat)
 cats = sorted(cats)
 for cat0 in cats:
  changes1 = [c for c in changes if c.cat == cat0]
  outarr = [] # header
  outarr.append('; ******************************************************')
  if cat0.endswith('nochg'):
   outarr.append('; cat=%s: %s changes NOT MADE' % (cat0,len(changes1)))
   print('; cat=%s: %s' % (cat0,len(changes1)))
  else:
   outarr.append('; cat=%s: %s changes' % (cat0,len(changes1)))
   print('; cat=%s: %s changes' % (cat0,len(changes1)))
  outarr.append('; ******************************************************')
  outrecs.append(outarr)
  for c in changes1:
   outarr = write_changes_helper(c)
   outrecs.append(outarr)
 write_recs(fileout,outrecs,blankflag=False)

def write_recs(fileout,outrecs,printflag=True,blankflag=True):
 # outrecs is array of array of lines
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
   if blankflag:
    out = ''  # blank line separates recs
    f.write(out+'\n')
 if printflag:
  print(len(outrecs),"records written to",fileout)


def get_abbrevs(lines):
 d = {}  # count of all abbrevs
 for line in lines:
  for m in re.finditer(r'<ab>(.*?)</ab>',line):
   ab = m.group(1)
   if ab not in d:
    d[ab] = 0
   d[ab] = d[ab] + 1
 return d

def check_tips(abbrevs_dict,tipdict,tiprecs):
 nf = 0
 nok  = 0  # tip not found, but lower-case tip found
 ntodo = 0 
 for abbrev in abbrevs_dict:
  count = abbrevs_dict[abbrev]
  if abbrev in tipdict:
   tiprec = tipdict[abbrev]
   tiprec.count = count
   continue
  nf = nf + 1
  # make a new tip
  abbrevlow = abbrev.lower()
  if abbrevlow in tipdict:
   tiprec_low = tipdict[abbrevlow]
   newdisp = tiprec_low.disp  
   line = "%s\t<id>%s</id> <disp>%s</disp> ADDED" % (abbrev,abbrev,newdisp)
   nok = nok + 1
  else:
   line = "%s\t<id>%s</id> <disp>NEW</disp> TODO" % (abbrev,abbrev)
   ntodo = ntodo + 1
  tiprec = AB_BUR(line)
  tiprec.count = count
  tiprecs.append(tiprec)
 print(nf,"abbrevs without tooltip")
 print(nok,"abbrevs with ADDED lower-case version")
 print(ntodo,"abbrevs tooltips TODO")
 
def write_tiprecs(fileout,tiprecs):
 tips = sorted(tiprecs,key = lambda rec: rec.ab.lower())
 outarr = []
 for tip in tips:
  out = '%s <count>%s</count>' %(tip.line, tip.count)
  outarr.append(out)
 write_lines(fileout,outarr)
if __name__=="__main__":
 filein = sys.argv[1]   # bur.txt
 filein1 = sys.argv[2] # burab_input
 fileout = sys.argv[3]  # ?
 lines = read_lines(filein)
 lines1 = read_lines(filein1)
 tiprecs,tipdict = init_ab_input(lines1)
 abbrevs_dict = get_abbrevs(lines)  # all <ab>X</ab> with counts
 check_tips(abbrevs_dict,tipdict,tiprecs)  # revise tiprecs
 write_tiprecs(fileout,tiprecs)

