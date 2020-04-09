#-*- coding:utf-8 -*-
"""extract2_preverb.py
 Extract 1-singular present tense forms from old conjugation tables.
 This specifically for normprev-conj-spcl.txt
 Make some corrections
"""
from __future__ import print_function
import sys, re,codecs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False
  self.forms = []  # conjugated forms calculated
def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 recs = [r for r in recs if r.cat == 'preverb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"preverbs returned from mwverbs")
 # list of keys that can be verb or preverb,
 # AND a code
 ddup = {

 }
 d = {}
 for rec in recs:
  k1 = rec.k1
  if (k1 in ddup):
   if (rec.cat == ddup[k1]):
    print('Using %s form for %s'%(rec.cat,k1))
    d[k1]=rec
   else:
    #print('Skipping %s form for %s'%(rec.cat,k1))
    pass
   continue
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

class Cform(object):
 def __init__(self,line):
  line = line.rstrip() 
  # self.cat is V (verb) or P (prefixed verb)
  parts = line.split(' ')
  self.k1,self.form,self.cat = parts[0:3]
  if self.cat == 'P':
   self.parse = parts[-1]
  else:
   self.parse = self.k1
  self.used = False

def init_cforms(filein,attr):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Cform(x) for x in f]
 print(len(recs),"conjugated forms read from",filein)
 
 d = {}
 for rec in recs:
  #k1 = rec.k1
  k1 = getattr(rec,attr)
  if k1 not in d:
   d[k1] = []
  #d[k1].append(rec.k1)
  d[k1].append(rec)
 # print records with duplicates
 return d,recs


def write(fileout,recs):
 a = []
 for rec in recs: # a Conj element
  k1 = rec.k1
  #k2 = rec.k2
  parse = rec.parse
  for form in rec.forms:
   v = k1,form,parse
   a.append(v)

 with codecs.open(fileout,"w","utf-8") as f:
  for k1,form,parse in a:
   f.write('%s %s P %s\n'%(k1,form,parse))
 n=len(a)
 print(n,"items written to",fileout)

sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','d'):'Md',
 ('m','D'):'MD',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','y'):'My',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rb',
 ('s','B'):'rB',
 ('s','m'):'rm',
 ('s','n'):'rn',
 ('s','y'):'ry',
 ('s','r'):'rr',
 ('s','l'):'rl',
 ('s','v'):'rv',

 ('d','l'):'ll',
 ('d','h'):'dD',
 ('d','S'):'cC',

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans

def join_pfx_verb(pfxes,form,verb):
 ans = pfxes[0]
 for pfx in pfxes[1:]:
  ans = join_prefix_verb(ans,pfx)
 pfx1 = ans
 if pfx1.endswith('i') and (form == 'sIdAmi'): # verb == 'sad'
  form = 'zIdAmi'
  return pfx1+form
 if pfx1.endswith('pra') and form.startswith('n'):
  form = 'R' + form[1:]  # replace initial 'n' with 'R'
  return pfx1+form
 ans = join_prefix_verb(pfx1,form)
 
 #ans = pfx + form  # no sandhi
 return ans

def main(mwverbrecs,cformsd,cpreformsd):
 nskip = 0
 for rec in mwverbrecs:
  parts = rec.parse.split('+')
  pfxes = parts[0:-1]
  verb = parts[-1]
  if verb not in cformsd:
   #print('verb not found',verb,rec.parse)
   continue
  cform_recs = cformsd[verb]
  for cform_rec in cform_recs:
   form = cform_rec.form
   preverbform = join_pfx_verb(pfxes,form,verb)
   preverbform = preverbform.replace('saMpra','sampra')
   if preverbform in cpreformsd:
    nskip = nskip + 1
   else:
    rec.forms.append(preverbform)
 print(nskip,"forms skipped since already in conjugated preverb forms")
  

if __name__=="__main__": 
 filein = sys.argv[1] # mwverbs
 filein1 = sys.argv[2] # extract1s_verb.txt
 filein2 = sys.argv[3] # extract2_preverb.txt
 fileout = sys.argv[4]
 mwverbrecs,mwverbsd= init_mwverbs(filein)
 cformsd,cforms = init_cforms(filein1,'k1')
 cpreformsd,cpreforms = init_cforms(filein2,'form')
 main(mwverbrecs,cformsd,cpreformsd)
 #recs = init_conj(filein)
 write(fileout,mwverbrecs)
 #write1(fileout,recs)
