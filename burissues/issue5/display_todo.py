# coding=utf-8
""" display_todo.py
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
  self.countprev = 0 # number of instances in bur.txt
  m = re.search(r' TODO <count>(.*?)</count>',self.line)
  self.todo = (m != None)
  if self.todo:
   self.countprev = int(m.group(1))
  # contexts is array of 2-tuples: (metaline,contextlines)
  self.contexts = []
  self.count = 0
  self.done =  'DONE' in self.line
  
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

def write_tiprecs(fileout,tiprecs):
 tips = sorted(tiprecs,key = lambda rec: rec.ab.lower())
 outarr = []
 for tip in tips:
  out = '%s <count>%s</count>' %(tip.line, tip.count)
  outarr.append(out)
 write_lines(fileout,outarr)

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
    if not tiprec.todo:
     # we're only interested in the TODO cases
     continue
    tiprec.count = tiprec.count + 1
    # gather information for context
    iline1 = max(0,iline - 1)
    nlines = len(entry.datalines)
    iline2 = min(nlines-1,iline + 1)
    contextlines = entry.datalines[iline1:iline2+1]
    context = (entry.metaline,contextlines)
    tiprec.contexts.append(context)

def get_lines_of_length(a,nlen):
 # remove <>
 b = re.sub(r'<.*?>',' ',a)
 c = re.sub(r'{[%#@]','',b)
 c = re.sub(r'[%#@]}','',c)
 c = re.sub(r'  +',' ',c)
 words = c.split(' ')
 current_line = ''
 output_lines = []
 for word in words:
  if len(current_line) + len(word) + 1 <= nlen:
   # Add the word to the current line
   current_line += word + ' '
  else:
   # Start a new line
   output_lines.append(current_line.strip())
   current_line = word + ' '
 # Add any remaining content to the output
 if current_line:
  output_lines.append(current_line.strip())
 # fold -s -w40 your_long_line.txt > output.txt
 return output_lines

def write_contexts(fileout,tiprecs0):
 tips_todo = [rec for rec in tiprecs0 if rec.todo]
 tips = sorted(tips_todo,key = lambda rec: rec.ab.lower())
 outrecs = []
 for tip in tips:
  if tip.countprev != tip.count:
   print('WARNING for ab=%s, %s != %s' %(tip.ab,tip.countprev,tip.count))
  outarr = []
  outarr.append('; **************************************')
  if tip.done:
   done = '(DONE)'
  else:
   done = '?'
  if tip.done:
   outarr.append('* DONE %s  tip="%s" %s (# instances = %s) ' % (tip.ab,tip.disp,done,tip.count))
  else:
   outarr.append('* TODO %s  tip="%s" %s (# instances = %s) ' % (tip.ab,tip.disp,done,tip.count))
  outarr.append('; **************************************')
  for ic,c in enumerate(tip.contexts):
   metaline,contextlines = c
   outarr.append('Case %s of %s: %s' %(ic+1,tip.count,metaline))
   a = ' '.join(contextlines)
   nlen = 60
   outputlines = get_lines_of_length(a,nlen)
   for temp in outputlines:
    outarr.append(temp)
   outarr.append('; -------------------------------')

  outrecs.append(outarr)
 write_recs(fileout,outrecs,printflag=True,blankflag=False)

if __name__=="__main__":
 filein = sys.argv[1]   # bur.txt
 filein1 = sys.argv[2] # burab_input
 fileout = sys.argv[3]  # a display of TODO tooltips
 entries = digentry.init(filein)
 lines1 = read_lines(filein1)
 tiprecs,tipdict = init_ab_input(lines1)
 # abbrevs_dict = get_abbrevs(lines)  # all <ab>X</ab> with counts
 update_contexts(entries,tipdict)  # revises tiprec records for 'TODO'
 write_contexts(fileout,tiprecs)

