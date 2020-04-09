#-*- coding:utf-8 -*-
"""verb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
#from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Burmap(object):
 def __init__(self,out):
  self.out = out
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
  ans = 'L=%s, k1=%s, k2=%s, code=%s, mw=%s,%s'%(
         self.L,k1,k2,self.code,mwhw,self.mwcat)

  if self.mwparse != None:
   mwparse = transcoder_processString(self.mwparse,tranin,tranout)
   ans = '%s,%s' %(ans,mwparse)
  return ans

def init_burmaprecs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Burmap(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 m = 0 # maximum line length
 outm = ''
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   assert rec.L == entry.metad['L']
   assert rec.k1 == entry.metad['k1']
   outarr = []
   line = rec.line
   line = re.sub('k2=.*?code=','code=',line)
   outarr.append(line)
   for x in entry.datalines:
    y = transcode_line(x,tranin,tranout)
    outarr.append(y)
   outarr.append(';' + ('-'*70))
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
    if (m < len(out)) and (not out.startswith(';------')):
     m = len(out)
     outm = out
 print(n,"records written to",fileout)
 print(m,"is the longest line length")
 print('one of the longest lines')
 print(outm)


if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx_verb_filter_map.txt
 fileout = sys.argv[3] # 
 
 recs = init_burmaprecs(filein)
 exit(1)
 write(fileout,recs,tranout)
