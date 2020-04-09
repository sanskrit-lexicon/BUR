#-*- coding:utf-8 -*-
"""bur_verb_filter.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def lexflag(line):
 return False
 lexpatterns = [
   '¦.*? <ab>m.</ab>',  #masculine
   '¦.*? <ab>f.</ab>',  #feminine
   '¦.*? <ab>n.</ab>',  #neuter
   '¦.*? <ab>a.</ab>',  #adjective
   '¦ <ab>ind.</ab>',  # indeclineable
   '¦ <ab>inter.</ab>',  # interjection
   '¦ <ab>adv.</ab>',  # adverb
 ] 
 for pattern in lexpatterns:
  if pattern in line:
   return True
 return False

R_special_map = {
 'aNgayAmi':'aNg', # 10 c
 'kanayAmi':'kanaya',   #10 
 'kandayAmi':'kand',   #10 
 'kavayAmi':'kav',   #10 Huet
 'kumAlayAmi':'kumAlaya',   #10 
 #'garayAmi':'',   #10 den. of guru (bur). Not in mw
 'gavezayAmi':'gavez',   #10 
 'jIvayAmi':'jIv',   #10 
 'tarhayAmi':'tfh',   #10 
 'tulayAmi':'tul',   #10 
 'darhayAmi':'dfh',   #10 
 'davayAmi':'davaya',   #10 
 'drAGayAmi':'drAG',   #10 
 'patayAmi':'pat',   #10 
 'palyulayAmi':'palyula',   #10 
 'pArayAmi':'pF',   #10 c.
 'BrAmayAmi':'Bram',   #10 c
 'mradayAmi':'mrad',   #10 c
 'yavayAmi':'yavaya',   #10 
 'yAmayAmi':'yam',   #10 c
 'lamBayAmi':'laB',   #10 c
 'vartayAmi':'vft',   #10 c
 'varzayAmi':'vfz',   #10 c  (bur den. of varza)
 'valyulayAmi':'valyula',   # den. mw.
 'vitUstayAmi':'vitUstaya',   #
 'vratayAmi':'vrataya',   #10 den
 'SAvayAmi':'vrataya',   #10 c
 'SrapayAmi':'SrA',   #10 c
 'SvayayAmi':'Svi',   #10 mw has c. SvAyayati  (SvA, not Sva)
 'avaryAmi':'avarya',  # 
 'aSnItapibatIyAmi':'aSnItapibatIya',  # 
 'aSvasyAmi':'aSvasya',  # 
 'aSvAyAmi':'aSvAya',  # 
 'Ard':'ard',  # Ard not mw
 'irajyAmi':'irajya',  # 
 'irasyAmi':'irasya',  # 
 'iryAmi':'iry',  # bur den. not mw
 'IryAmi':'Iry',  # bur den. not mw
 'uruzyAmi':'uruzya',  # 
 'UwAmi':'Uw',  # not mw
 'fkz':'fkz',  # cf. f. Not mw
 'elAyAmi':'elAya',  # den.
 'ez':'ez',  # 
 'gopAyAmi':'gopAya',  # 
 'cakAsmi':'cakAs',  # class 2
 'daSasyAmi':'daSasya',  # 
 'dAmi':'dA',
 'dAsAyAmi':'dAsAya',  # 
 'bapsAmi':'Bap', # redup
 'baBrAmi':'Bram',  # redup
 'BizRajyAmi':'BizRajya',  # 
 'BuraRyAmi':'BuraRya',  # 
 'mandAyAmi':'mandAya',  # 
 'liwyAmi':'liwya',  # 
 'lewyAmi':'lewya',  # 
 'lelAyAmi':'lelAya',  # 
 'lowyAmi':'lowya',  # 
 'vedyAmi':'vedy',  # 
 'vocAmi':'vac',  # vd.
 'samBUyasyAmi':'samBUyasya',  # den
 'suvAmi':'sU',  # 
'tapasyAmi':'tapasya',
 'daSasyAmi':'daSasya',
 'bapsAmi':'Bas',
     'cakAsmi':'cakAs',
     'pA':'pA',
     'ruc':'ruc',
     'aNgayAmi':'aNg',
     'qumB':'qap',  # 
     'panasyAmi':'panasya',  # Den
     'garayAmi':'guru', # 
     'curaRyAmi':'curaRya',  # 
     'garayAmi':'guru', 
 'jage':'gA', # perf
 'asrAye':'asrAya', # den
 'AdDve':'As', # 2p. pl. pr. de As. M.
 'AnaNke':'aNk',
 'AnaNGe':'aNG', # pf. cf mw.
 'Anawwe':'aww', # pf. mw
 'Anambe':'amb', # pf.
 'AnaSe':'aS',   # pf. mw
 'AnaMhe':'aMh', # pf.
 'Anfje':'fj',   # pf. mw
 'iDye':'inD',   # passive
 'Iwwe':'Iq',    # cl.2  mw
 'IDe':'inD',    # mw
 'Imahe':'i',  # 1pl. pr. 'i'  Huet
 'utpucCaye':'utpucCaya',  # den.
 'upye':'vap',   # pass. mw
 'Uce':'vac',    # prf-m Huet
 'Ude':'vad',    # prf-m Huet
 'Uve':'u',      # not sure why long 'U'
 'Eqiqe':'Iq',   # 
 'otAse':'u',    # f1. moy. 
 'kusmaye':'kusmaya',
 'kriye':'kf',
 'garQAhe':'garh',  # f1. vd.
 'gfhye':'grah',    # pre-passive
 'Garkzye':'garh',
 'cakre':'kf',
 'citrIye':'citrIya',  # den de 'citra'
 'jagfBre':'gfB',    # vd. 
 'jagfmBAte':'gfmB', # vd.
 'jagfhe':'grah',    # pf. 
 'jagme':'gam',      # pf
 'jajYire':'jYA',    # pf.
 'jajYe':'jan',      # pf.
 'jarate':'jf',
 'jarante':'jf',
 'jarBe':'jfmB',     # bur hfB (which is not mw)
 'jahre':'hf',       # pf hf
 'jigeve':'gev',  # pf
 'jigye':'ji',  # pf
 'jiGne':'han',  # pf
 'jihILire':'hel',  # vd. pf. 3p. pl.
 'jihye':'hA',  #   #pr. class 3
 'juhure':'hve',  # pf.
 'tizwige':'stig',  # Note: stig NOT in bur, but stiG
 'tizwipe':'stip',  # pf
 'tuzwuce':'stuc',  # pf
 'tuzwuBe':'stuB',  # pf
 'tuzwuve':'stu',  # pf
 'tfpAye':'tfpAya',  # den,
 'tfptAye':'tfptAya',  # den. not mw
 'tene':'tab',  # pr. moy.
 'dadre':'df',  # pf. WhitRoot
 'daDiDve':'DA',  # 2p, pl. pr. moy. vd.
 'daDre':'Df',  # pf.
 'dAsaye':'daMs',  # form ?
 'digye':'de',  # pr. moy.
 'dIrye':'dF',  # passive
 'durmanAye':'durmanAya',  # Denom.
 'dUye':'du',  # passive
 'Datte':'DA',  # 3p. sg. pr. moy.
 'ninye':'nI',  # pf
 'niriRye':'nF',  # vd.  pfx (ni+nF)? or form of nF ?
 'neye':'nI',  #
 'nese':'nay',  #  pr. moy. | Huet pf. middle
 'papye':'pyE',  # pf. mw
 'pUrye':'pF',  # passive
 'pece':'pac',  # pf.
 'pede':'pad',  # pf.
 'peye':'pay',  # pf.
 'prIyAye':'prIyAya',  # den. do priya
 'badbaDe':'banD',  # pf
 'baDye':'banD',  # passive
 'baBre':'Bf',  # pf
 'Barate':'Bf',  # 3p. pr. ps. vd.
 'Beje':'Baj',  # pf
 'Briye':'Bf',  # passive
 'mandraye':'mandraya',  #
 'mame':'mA',  # pf
 'mamre':'mf',  # pf
 'mahIye':'mahIya',  #
 'mimye':'mi',  # pf.
 'mene':'man',  # pf
 'yazwAhe':'yaj',  # f1.
 'yAvaye':'yu',  # # causal
 'yUye':'yu',  # pr. ps.
 'yete':'yat',  # pf.
 'yojaye':'yuj',  # causal
 'rirye':'rI',  # pf.
 'reme':'ram',  # pf.
 'reye':'ray',  # pf.
 'leje':'laj',  # pf
 'leBe':'laB',  # pf
 'leze':'laz',  # pf
 'vavakze':'vac',  # p. moy. vd.
 'vinDe':'vid',  # pr. vd.
 'vfzAye':'vfzAya',  # Den
 've':'ve',  #
 'veye':'vay',  # pf.
 'vErAye':'vErAya',  #
 'vriye':'vf',  # passive
 'SaSye':'SyE',  # pf.
 'Sete':'SI',  # pf.
 'Serate':'SI',  # pf.
 'SrUye':'Sru',  # passive
 'samBARqaye':'samBARqaya',  #
 'svarye':'svarya',  # den. not mw
 'sIye':'so',  # passive
 'sUye':'su',  # passive
 'sece':'sac',  # pf.
 'sehe':'sah',  # pf.
 'skadye':'skand',  # passive
 'stUye':'stu',  # passive
 'sTIyate':'sTA',  # passive
 'have':'hve',  # pr. vd.
 'hIye':'hA',  # passive
 'huve':'hve',  # pr. vd.
 'hUye':'hu',  # passive, also of hve
 'hriye':'hf', # passive
 'jaraDyE':'jf',  # vd. inf.
 'jarasva':'jf',  # vd. imp.
 'DiyaDyE':'DA',  # vd. inf.
 'sahaDyE':'sah',  # vd. inf.
 'sAQyE':'sah',  # vd. inf.
 'etAsmi':'i',  #  f1.
 'ezitAsmi':'iz',  # f1.
 'kurumi':'kf',  # 1p. pr. vd.
 'kOmi':'kU',  # pr. bur has 'ku'
 'goQAsmi':'guh',  # f1.
 'jiharmi':'hf',  # pr. vd.
 'tarQAsmi':'tfh',  # f1.
 'dadmi':'dA',  # pr. épique
 'dezwAsmi':'diS',  # f1.
 'draptAsmi':'dfp',  # f1.
 'drazwAsmi':'dfS',  # f1.
 'droQAsmi':'druh',  # f1.
 'mAtAsmi':'mA',  # f1.
 'meQAsmi':'mih',  # f1.
 'moQAsmi':'muh',  # f1.
 'yantAsmi':'yam',  # f1.
 'roQAsmi':'ruh',  # 
 'lobDAsmi':'luB',  # f1.
 'sizaGmi':'sac',  # pr. vd.
 'sotAsmi':'su',  # f1.
 'startAsmi':'stf',  # f1.
 'sneQAsmi':'snih',  # f1.
 'veda':'vid', #pf.
 'dadasva':'dA', # 2p. sg. imp. épique
 'Datsva':'DA',  # 2p. sg. imp.
 'Dizva':'DA',   # 2p. imp. vd.

 'Apnuhi':'Ap',  # 2p. imp.
 'ihi':'i',  # 2p. imp.
 'ehi':'i',  # 2p. sg. imp.
 'jahi':'han',  # 2p. imp.
 'jahihi':'hA',  # 2p. sg. imp.
 'jAnIhi':'jYA',  # 2p. sg. imp.
 'dehi':'dA',  # 2p. sg. imp.
 'DImahi':'DyE',  # 1p. pl. impf. vd.  (or of DI)
 'Dehi':'DA',  # 2p. sg. imp.
 'DyAhi':'DyE',  # 2p. sg. imp. vd.
 'mimIhi':'mA',  # 2p. imp. vd.

 # verb entries, headword ending in 'am'
 'ajaham':'hA',  # 
 'aYjigam':'aNg',  # 
 'anAtsam':'nah',  # a1
 'aBArkzam':'Brajj',  # a1
 'amaNGam':'majj',  # a1
 'amAsizam':'mI',  # a1  (or 'mi')
 'arIrayam':'rE',  # 
 'alasam':'lI',  # a1
 'alIQam':'lih',  # a1
 'alEzam':'lī',  # 
 'avAkzam':'vah',  # a1
 'avAsizam':'ve',  # a1
 'avedizam':'vid',  # a1
 'avocam':'vac',  # a2
 'avoQam':'vah',  # a2
 'aSrOzam':'Sru',  # a1
 'Acikzam':'akz',  # 
 'AYjigam':'aNg',  # 
 'AYjizam':'aYj',  # a1
 'AYjiham':'aMh',  # 
 'Atizam':'at',  # a1
 'Adam':'ad',  # 
 'Anam':'an',  # 
 'Ayam':'i',  # 
 'Aram':'f',  # a2
 'Arcizam':'arc',  # a1
 'ArDizam':'fD',  # a1
 'Asisam':'as',  # 
 'AsTam':'as',  # a1
 'itam':'i',  # 
 'ucyAsam':'vac',  # o.
 #'eqQvam':'iS',  # There is no 'iS'.  Cannot guess
 'envizam':'inv',  # a1
 'Ecikzam':'Ikz',  # 
 'EwiWam':'eW',  # 
 'Eyaram':'f',  # 
 'Eriram':'Ir',  # 
 'Erkzyizam':'Irkzy',  # a1
 'Ezizam':'iz',  # 
 'Okzam':'ukz',  # 
 'OciKam':'oK',  # 
 'Ojiham':'Uh',  # 
 'OjJizam':'ujJ',  # 
 'ORiRam':'oR',  # 
 'Ondidam':'und',  # 
 'Ondizam':'und',  # a1
 'Objizam':'ubj',  # a1
 'OmBizam':'umB',  # a1
 'Orjijam':'Urj',  # 
 'OrRavizam':'UrRu',  # a1
 'OrRuRuvam':'UrRu',  # 
 'Ozizam':'uz',  # a1
 'jIyAsam':'jyA',  # o.
 'tArizam':'tF',  # 
 'deyam':'dA',  # 
 'deyAsam':'dA',  # 
 'dreyAsam':'drA',  # 
 'DeyAsam':'DA',  # 
 'DmeyAsam':'DmA',  # 
 'peyAsam':'pA',  # a1
 'baBUyAsam':'BU',  # 
 'BriyAsam':'Bf',  # 
 'meyAsam':'mA',  # a1
 'viyAsam':'vye',  # 
 'vIyAsam':'vye',  # 
 'vUryAsam':'vf',  # 
 'SUyAsam':'Svi',  # 
 'supyAsam':'svap',  # 
 'stam':'stam',  # 
 'sTeyAsam':'sTA',  # 
 'sriyAsam':'sf',  # 
 #'saYcIvaraye':'saMcIvaraya',  #consider a verb non-prefixed, as bur no cIvaraya

 
  }
D_special_map = {
 'prez':'prez',
 'vI':'vI',
 'uttizWAmi':'utTA',
 'nirgE':'nirgE',  #  not mw
 'pariveda':'vid',
 'Agahi':'Agam',  # imp. vd.

 'avaroruDam':'avaruD',  # 
 'upaDAkzizam':'upadah',  # a1
 'upaDAkzizam':'upadah',  # a1
 'upADmAsizam':'upaDmA',  # a1
 'nivadDvam':'nivas',  # 
 'vyaDamam':'viDmA',  # 

}

def mark_entries_verb(entries,exclusions,inclusions):
 """ bur verbs: P """
 for entry in entries:
  k1 = entry.metad['k1']
  # first exclude known non-verbs
  if entry.metaline in exclusions:
   exclusions[entry.metaline] = True  # so we know exclusion has been used
   continue 
  if entry.metaline in inclusions:
   if k1 in R_special_map:
    entry.markcode = 'R'
   elif k1 in D_special_map:
    entry.markcode = 'D'
   else:
    print('mark_entries: special inclusion no code. Marking as "D".',k1)
    entry.markcode = 'D'
   continue
  L  = entry.metad['L']
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline
  datalines = entry.datalines
  if lexflag(datalines[0]):
   continue
  patterns = [
   u'^{#[*]',
   u'¦.*<ab>dés.</ab>',
   u'¦.*<ab>aug.</ab>',
   u'¦.*<ab>c.</ab>',
   u'¦.*<ab>f2[.]</ab>',
   u'Ami#}¦',
   u'omi#}¦', # e.g., karomi
   u'e#}¦', # e.g. aticezwe
   u'mi#}¦', # e.g.anuvacmi
  ]
  codes = [None,None,None,None,None,None,None,None,None,None,None]
  pattern_codes = ['R','Des','Aug','C','F','D','D','D','D']
  codeidx={}
  for i,c in enumerate(pattern_codes):
   codeidx[c] = i
  # 3 overrides for 'D' code
  if k1 in D_special_map: #['prez','vI','uttizWAmi',]:
   codes[codeidx['D']] = 'D'
   datalines = [] # so next logic doesn't override
  elif k1 in R_special_map:
   codes[codeidx['R']] = 'R'
   datalines = [] # so next logic doesn't override
  elif k1 in {
    'cAKyAmi':'KyA',
    'jAjYAmi':'jYA',  # Aug
    'tantasyAmi':'taMs',  # Aug
    'SASrAmi':'SrA',  # Aug
    'cAcCAmi':'Co',  # 
    'boBojmi':'Buj',
    'popomi':'pU',
    'caYcUrye':'car',  # Aug
    'carIkfzye':'kfz', # aug
    'calIkalpye':'jxp', #aug
    'jariharmi':'hf',  # aug.
    'jarIGardmi':'gfD',  # aug.
    'jAgAhmi':'gAh',  #  aug.
    'jeGemi':'hi',  # aug.
    'jejayImi':'ji',  # aug.
    'jejremi':'%jri',  # aug
    'jehremi':'hrI',  # aug
    'jogohmi':'guh',  # aug
    'lelehmi':'lih',  # aug.
    'sAsahmi':'sah',  # aug
    #'apaSoSucAmi':'apaSuc', # aug
    #'ASoSucAmi':'ASuc',
    }:
   codes[codeidx['Aug']] = 'Aug'
   datalines = [] # so next logic doesn't override
  elif k1 in {  }:  # currently always fails. no 'Den' pattern_code
   #codes[1] = 'Den'
   codes[codeidx['Den']] = 'Den'
   datalines = [] # so next logic doesn't override
  elif k1 in {
    'ciklikzAmi':'kliS',  # 
    'ciklitsAmi':'klid',  # 
    'jijarizAmi':'jF',  # 
    'jugupizAmi':'gup',  # 
    'didarizAmi':'df',  # des
    'dIdAMsAmi':'dAn',  # des
    'piparcizAmi':'pfc',  # des
    'vivitse':'vid',  # Desiderative
    }:
   codes[codeidx['Des']] = 'Des'
   datalines = [] # so next logic doesn't override
  elif k1 in {
    'kAsyAmi':'kE',  # Future

    }:
   codes[codeidx['F']] = 'F'
   datalines = [] # so next logic doesn't override
  lex = False
  for iline,line in enumerate(datalines):
   if iline != 0:
    break
   # exclude lex pattern
   if lexflag(line):
    break
   for ipattern,pattern in enumerate(patterns):
    if re.search(pattern,line):
     codes[ipattern] = pattern_codes[ipattern]
     #if L=='143': 
     # m = re.search(pattern,line)
     # print(k1,L,codes[ipattern],m.group(0))
     break  # get all patterns # only get first pattern
  #if k1 == 'bapsAmi':print('k1=',k1,'codes=',codes,codes_used,code)
  codes_used = [c for c in codes if c != None]
  if len(codes_used) != 0:
   code = ''.join(codes_used)
  if (code != None) and lex:
   print('exclude lex',code,entry.metaline)
   code=None
  if code != None:
    entry.markcode = code
    #entry.markline = line
    #entry.marklinenum=entry.linenum1 + (iline+1)
    #break # for iline,line
 for x in exclusions:
  if not exclusions[x]:
   print('Unused exclusion:',x)

def write_verbs(fileout,entries):
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   if code not in coded:
    coded[code] = 0
   coded[code] = coded[code] + 1
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   k2a = re.sub(r'^([a-zA-Z]+)(.*)$',r'\1',k2)
   if k2a != k2:
    print('simplifying k2 from "%s" to "%s"'%(k2,k2a))
    k2=k2a
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, code=%s' %(n,L,k1,k2,code))
   for out in outarr:
    f.write(out+'\n')
 code_keys = sorted(coded.keys())
 for code in code_keys:
  print('%04d %s' %(coded[code],code))
 print('%04d' %n,"verbs written to",fileout)

def init_exclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

def init_inclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # bur_verb_exclude.txt
 filein2 = sys.argv[3] # bur_verb_include.txt
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 exclusions = init_exclusions(filein1)
 inclusions = init_inclusions(filein2)
 mark_entries_verb(entries,exclusions,inclusions)
 write_verbs(fileout,entries)
