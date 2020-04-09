#-*- coding:utf-8 -*-
"""preverb1.py

We can tell if string x is less than string y:
 x.translate(slp_from_to) < y.translate(slp_from_to)

If 'a' is a list of Sanskrit words, we can sort by:
 sort(a,key = lambda x: x.translate(slp_from_to))

 
"""
from __future__ import print_function
import sys, re,codecs
#from parseheadline import parseheadline
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('transcoder')

slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
slp_from_to = str.maketrans(slp_from,slp_to)

class Burmap(object):
 def __init__(self,out):
  self.out = out.rstrip('\r\n')
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',out)
  self.L,self.k1,self.k2,self.code,self.mwfield = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  parts = self.mwfield.split(',')
  self.mwhw = parts[0]
  self.mwcat = parts[1]
  if len(parts) == 3:
   self.mwparse = parts[2]
  else:
   self.mwparse = None
 def transcode(self,tranin,tranout):
  k1 = transcoder_processString(self.k1,tranin,tranout)
  k2 = transcoder_processString(self.k2,tranin,tranout)
  mwhw = transcoder_processString(self.mwhw,tranin,tranout)
  #ans = 'L=%s, k1=%s, k2=%s, code=%s, mw=%s,%s'%(
  #       self.L,k1,k2,self.code,mwhw,self.mwcat)
  Ljust = str.ljust(self.L,5)
  #ans = 'L=%s, k1=%s, code=%s, mw=%s,%s'%(
  #       Ljust,k1,self.code,mwhw,self.mwcat)
  k1just = str.ljust(k1,10)
  code = self.code
  codejust = str.ljust(code,3)
  ans = 'L=%s k1=%s code=%s mw=%s,%s'%(
         Ljust,k1just,codejust,mwhw,self.mwcat)

  if self.mwparse != None:
   mwparse = transcoder_processString(self.mwparse,tranin,tranout)
   ans = '%s,%s' %(ans,mwparse)
  return ans

def init_burmaprecs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Burmap(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Group(object):
 def __init__(self,verb):
  self.verb = verb
  self.verbrecs = []
  self.othrrecs = []

def init_verbgroups(recs):
 d = {}
 groups = []
 for rec in recs:
  #k1 = rec.k1
  if rec.mwcat == 'verb':
   verb = rec.mwhw
   if verb.startswith('?'):
    verb = verb[1:] # drop initial ?
  elif rec.mwparse == None:
   print('skipping:',rec.out)
   continue
  else:
   mwparse = rec.mwparse # assume not None
   parts = mwparse.split('+')
   verb = parts[-1]
  if verb not in d:
   group = Group(verb)
   groups.append(group)
   d[verb] = group
  group = d[verb]
  if rec.mwcat == 'verb':
   group.verbrecs.append(rec)
  elif rec.mwcat == 'preverb':
   group.othrrecs.append(rec)
  else: # does not happen
   print('unknown mwcat=%s. line = %s'%(rec.mwcat,rec.out))
  if False and (verb == 'yuj'): # debug
   n1 = len(group.verbrecs)
   n2 = len(group.othrrecs)
   print('(%d,%d) '%(n1,n2),rec.transcode('slp1','slp1'))
 return groups

def order_verbrecs(recs):
 if len(recs) < 2:
  # nothing to do
  return recs,[]
 recs1 = [r for r in recs if r.k2.startswith('*')] # 'True' verbs
 recs2 = [r for r in recs if r not in recs1]
 return recs1,recs2
def write(fileout,groups,tranout):
 tranin = 'slp1'
 n = 0
 outm = ''
 with codecs.open(fileout,"w","utf-8") as f:
  for group in groups:
   n = n + 1
   outarr = []
   mother = len(group.othrrecs)
   verbrecs1,verbrecs2 = order_verbrecs(group.verbrecs)
   tverb = transcoder_processString(group.verb,tranin,tranout)
   out = '; Verb %04d: %s (%d uninflected, %d inflected, %d prefix entries)' % (n,tverb,len(verbrecs1),len(verbrecs2),mother)
   outarr.append(out)
   for rec in verbrecs1:
    c = rec.code
    rec.code = '*'+c
    out = '  %s' % rec.transcode(tranin,tranout)
    rec.code = c
    outarr.append(out)
   for rec in verbrecs2:
    out = '  %s' % rec.transcode(tranin,tranout)
    outarr.append(out)
  
   for iother,othrrec in enumerate(group.othrrecs):
    out = '  %s' % othrrec.transcode(tranin,tranout)
    outarr.append(out)
   outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
   #f.write(group.verb + '\n')
   continue
 print(len(groups),"records written to",fileout)

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx_verb_filter_map.txt
 fileout = sys.argv[3] # 
 
 recsin = init_burmaprecs(filein)
 groups = init_verbgroups(recsin)
 groups.sort(key = lambda group: group.verb.translate(slp_from_to))
 write(fileout,groups,tranout)
