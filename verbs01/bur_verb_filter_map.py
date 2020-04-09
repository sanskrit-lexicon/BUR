#-*- coding:utf-8 -*-
"""bur_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs
from bur_verb_filter import init_entries,Entry
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('transcoder')

class Burverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  try:
   m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
   self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  except:
   print('Burverb error: line=',line)
   exit(1)
  self.mw = None
  self.mwrec = None
  
def init_burverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Burverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 # list of keys that can be verb or preverb,
 # AND a code
 ddup = {
  'Ap':'verb','As':'verb','nI':'verb','vyac':'verb',
  'ez':'verb','prez':'preverb','vI':'preverb'
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
 #bur:mw

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

def init_cforms(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Cform(x) for x in f]
 print(len(recs),"conjugated forms read from",filein)
 
 d = {}
 for rec in recs:
  form = rec.form
  if form not in d:
   d[form] = []
  #d[form].append(rec.k1)
  d[form].append(rec)
 # print records with duplicates
 ndup = 0
 for form in d.keys():
  if len(d[form]) > 1:
   ndup = ndup + 1
   dups = d[form] # list of records
   hws = [r.k1 for r in dups]
   hwstr = ','.join(hws)
   #print('init_cform dups: %s -> %s' %(form,hwstr))
 print(ndup,"conjugated forms with multiple headwords")
 return d,recs


map2mw_special_R = {
 #bur:mw
 'garayAmi':'guru',   #10 den. of guru (bur). Not in mw
 'avaryAmi':'avarya',  # 
 'aYC':'aYc',   # Voyez {%āñch.%}
 'aSnItapibatIyAmi':'aSnItapibatIya',  # 
 'aSvAyAmi':'aSvAya',  # 
 'Ard':'ard',  # Ard not mw
 'iC':'iz',     # Cf. iṣ
 'irajyAmi':'irajya',  # 
 'irasyAmi':'irasya',  # 
 'iryAmi':'iry',  # bur den. not mw
 'IryAmi':'Iry',  # bur den. not mw
 'asUy':'asUya',
 'aSvasyAmi':'aSvasya',  # 
 'ij':'yaj',    # Cf, yaj
 'IL':'il',     # Cf. il, iḍ, il
 'ucC':'uC',   # Cf uC
 'uruzyAmi':'uruzya',  # 
 'uS':'vaS',
 'UwAmi':'Uw',  # not mw
 'Un':'Unaya',
 'fkz':'fkz',  # cf. f. Not mw
 'elAyAmi':'elAya',  # den.
 'ez':'ez',  # 
 'kalp':'kxp',
 'kaMS':'kaMs',
 'kuwumb':'kuwumbaya',
 'kfj':'karj',
 'kfb':'karb',  # Cf karb
 'ket':'ketaya',  # Causal of kit
 'krudD':'kruD', # Cf krudh
 'kzid':'kzvid', # Cf kṣvid
 'gacC':'gam',   # Cf gam
 'garD':'gfD',   # Cf gṛdh
 'gozW':'gozWa',
 'guR':'guRaya',
 'gfB':'grah',  # <ab>vd.</ab> de {%gṛh;%}
 'gfmB':'grah',
 'gfh':'grah',  # même racine que grah
 'graB':'grah',
 'Card':'Cfd',
 'jaq':'jal',  # cf jal
 'jug':'juNg',
 'Jarj':'JarJ',
 'tantr':'tantraya',
 'tir':'tiraya',
 'tIr':'tIraya',
 'tutT':'tutTaya',
 'tUr':'tvar',   # cf. tvar
 'Taq':'Tuq',   #  cf sTuq  (mw Tuq = sTuq (cover))
 'TuD':'SuD', # cette rac. paraît être une mauvaise orthog. de {#SuD#}
 'duHK':'duHKa', # could be duHKaya or duKya
 'dUz':'duz',
 'Dinuhi':'Dinv', # 2p. imp. vd. dhinv
 'DyA':'DyE',
 'DrU':'Dru',
 'trA':'trE',
 'picC':'piC',
 'pIv':'pIva',
 'puzp':'puzpya',
 'pUr':'pF',
 'pUrv':'pF',
 'pracC':'praC',
 'baw':'vaw',  #b/v
 'baRw':'vaRw', #b/v
 'ban':'van',
 'buz':'bus',  # or vyuz
 'byuz':'vyuz',
 'Brasj':'Brajj',
 'masj':'majj',
 'mfl':'mfq',
 'yaC':'yam',
 'rarp':'rap',
 'larv':'larb',
 'lasj':'lajj',
 'lUp':'luz',
 'leK':'leKAya',
 'vfc':'vfj',
 'SaMst':'saMst',
 'Sur':'SUr',
 'Sf':'Sru',
 'SvF':'svF',
 'zaYj':'saYj',
 'zaw':'saw',
 'zad':'sad',
 'zan':'san',
 'zah':'sah',
 'zi':'si',
 'zic':'sic',
 'ziD':'siD',
 'zu':'su',
 'zU':'sU',
 'zev':'sev',
 'zwu':'stu',
 'zWA':'sTA',
 'zRA':'snA',
 'zmi':'smi',
 'sId':'sad',
 'sTUla':'sTUl',
 'sbf':'svf',
 'nf':'nF',
 'svakk':'zvakk',  #?
 'lAw':'lAwyAya',
 'zaR':'SaR',   # typo 'saR' -> 'SaR' under hw=zaR ?
 'jurv':'jUrv',
  '':'',
 # missing or alternate nasal
 'ab':'amb',  # bur has both ab and amb, mw only amb
 'aB':'amB',  # bur has both
 'ig':'iNg',
 'iMv':'inv',
 'iv':'inv',  #C. %iṃv   (what is abbreviation 'C.'? print err for 'Cf.' ?)
 'kAc':'kAYc', # Cf %kāñc
 'kudr':'kundr', # Cf kundr
 'kub':'kumb',  # Cf kumb
 'kuB':'kumB',  # Cf kumB 
 'kruT':'krunT', # Cf krunth
 'guW':'guRW',   # Cf guṇṭh
 'caq':'caRq',  # cf. caṇḍ
 'cub':'cumb',
 'jiv':'jinv',
 'jfB':'jfmB',
 'wak':'waNk',
 'qaB':'qamB',
 'tuYj':'tuj',
 'tub':'tumb',
 'tfMh':'tfh',
 'trak':'traNk',
 'trad':'trand',
 'triK':'triNK',
 'dav':'danv',
 'daS':'daMS',
 'Div':'Dinv',
 'pij':'piYj',
 'Bad':'Band',
 'Svid':'Svind',
 'skud':'skund',
 'hiq':'hiRq',
 'nis':'niMs',
 'piv':'pinv',
 'miv':'minv',
 'riv':'riRv',
 'vfYj':'vfj',
 'hiv':'hinv',

 # verbs usu. class 10 or causal
  # roots without prefix. Class 10, or causal
 'aNgayAmi':'aNg', # 10 c
 'kanayAmi':'kanaya',   #10 
 'kandayAmi':'kand',   #10 
 'kavayAmi':'kav',   #10 Huet
 'kumAlayAmi':'kumAlaya',   #10 
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

 '':'',
 # misc _R
 'gopAyAmi':'gopAya',  # 
  'cakAsmi':'cakAs',  # class 2
 'curaRyAmi':'curaRya',  # Den.
 'tapasyAmi':'tapasya',  # 
 'dAmi':'dA',  # vd, or 'do'
 'dAsAyAmi':'dAsAya',  # 
 'daSasyAmi':'daSasya',
 'panasyAmi':'panasya',  # Den
 'bapsAmi':'Bas',  # bur says from 'pzA' (typo for 'psA'?) psA ~ Bas in mw
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
 'qumB':'qap',

 # omi endings
 'juhomi':'hu',   # 
 'minomi':'mi',   # 
 'jage':'gA', # 
 'asrAye':'asrAya', # den
 'AdDve':'As', # 2p. pl. pr. de As. M.
 'AnaNke':'aNk', # pf.  cf mw.  
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
 'jagfBre':'grah',    # vd. 
 'jagfmBAte':'grah', # vd.
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
 'tene':'tan',  # pr. moy.
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
 'veda':'vid', # pf.
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
 #'saYcIvaraye':'saMcIvaraya',  #consider a verb non-prefixed, as bur no cIvaraya
 #'nitoSe':'nituS',   # consider a verb non-prefixed, as bur has no tuS
 #'AprAmi':'AprA',    # consider a verb non-prefixed, as bur has no prA

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
}

# next 3 from hwnorm1/sanhw1/hwnorm1c.py
slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}

def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)

def homorganic_nasal(a):
 return re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)

def map2mw_nasal(k1,d):
 k = homorganic_nasal(k1)
 if k in d:
  return k
 return None

def map_3s(k,d):
 if k.endswith(('yati','yate')):
  k1 = k[0:-2]  # remove final ti, te
  if k1 in d:
   return k1
 return None

def map2mw_R(d,k1):
 """ for bur
 """
 if k1 in map2mw_special_R:
  k =  map2mw_special_R[k1]
  if k not in d:
   #print('map2mw_R Error 1: %s -> %s (not in mw)'%(k1,k))
   return k,False
  else:
   mwrec = d[k]
   if mwrec.cat != 'verb':
    print('map2mw_R Error 2: %s -> %s (a preverb)'%(k1,k))
   else:
    return k,True
 if k1 in d:
  return k1,True
 # omi endings
 omis = [
  ('karomi','kf'),
  ('kfRomi','kF'),
  ('Apnomi','Ap'),
  ('SfRomi','Sru'),
  ('cinomi','ci'),
  ('tanomi','tan'),
  ('vfRomi','vf'),
  ('rADnomi','rAD'),
  ('staBnomi','stamB'),
  ('DUnomi','DU'),
  ('Dunomi','Du'),
  ('dunomi','du'),
  ('zunomi','zu'), # su
  ('zuRomi','zu'), # su
  ('hinomi','hi'),
  ('hiRomi','hi'),
  ('stfRomi','stf'),
  ('yuyomi','yu'),
  ('fDnomi','fD'),
  ('zwaBnomi','zwamB'),
  ('aSnomi','aS'),
  ('zkaBnomi','zkamB'),
 ]
 for (old,new) in omis:
  k = re.sub(old,new,k1)
  if k in d:
   return k,True
 return '?',True

map2mw_special_D = {
 # prefixed verbs
 'ativAhayAmi':'ativah',
 'anupUrayAmi':'anupF', #c. Huet
 'anvASrayAmi':'anvASri',
 'apavarjayAmi':'apavfj', #10
 'aBigopayAmi':'aBigup',  #10 not mw
 'aBicodayAmi':'aBicud', #10
 'aBiDArayAmi':'aBiDf', #10
 'aBinAdayAmi':'aBipracud', #10
 'aBipAlayAmi':'aBipal',  #10, not in mw
 'aBipracodayAmi':'aBipracud', 
 'aBiSabdayAmi':'aBiSabdaya', #10. A Root in MW
 'aByucCrayAmi':'aByucCri', # aBi+ut+Sri. Not in mw
 'avadArayAmi':'avadF', # 10
 'avaDArayAmi':'avaDf', # 10
 'avaDIrayAmi':'avaDI', # 10
 'AnAdayAmi':'Anad', # 10
 'ApUrayAmi':'ApF', #10
 'AyoDayAmi':'AyuD', #10
 'AropayAmi':'Aruh',   #10 causal
 'AloqayAmi':'Aluq',   #10 
 'AvArayAmi':'Avf',   #10 
 'AsAdayAmi':'Asad',   #10 c. Huet
 'AsPowayAmi':'AsPuw',   #10  c. Huet
 'uccawayAmi':'uccaw',   #10 
 'udGAwayAmi':'udGaw',   #10 
 'udGozayAmi':'udGuz',   #10 
 'unmUlayAmi':'unmUla',   #10 
 'upaDArayAmi':'upaDf',   #10 
 'upavIRayAmi':'upavIRaya',   #10 mw vIRaya
 'nimAdayAmi':'nimad',   #10 
 #'nironayAmi':'',   #10 vd. niras + nI  (niras = tiras bur)
 'pariKedayAmi':'pariKid',   #10 c
 'paricodayAmi':'paricud',   #10 c
 'paripAdayAmi':'paripad',   #10 c
 'paripozayAmi':'paripuz',   #10 
 'parimohayAmi':'parimuh',   #10 
 'parivaMSayAmi':'parivaMS',   #10 Cannot find 'vaMS' as verb in mw or bur!
 'parivezayAmi':'pariviz',   #10 
 'pracodayAmi':'pracud',   #10 
 'praRiDayAmi':'praRiDe',   #10 not in mw
 'pratiCAdayAmi':'pratiCad',   #10 not in mw
 'pratiRayAmi':'pratinI',   #10  # pratinI not in mw.  is 'R' error in bur?
 'pratinirjayAmi':'pratinirji',   #10 not mw
 'praDarzayAmi':'praDfz',   #10 c
 'praDArayAmi':'praDf',   #10 
 'prapAlayAmi':'prapal',   #10 not mw
 'procCrayAmi':'procCri',   #10 pra+ud+Sri not mw
 'viDarzayAmi':'viDfz',   #10 c
 'vipayAmi':'vipay',   #10 not in mw
 'viloqayAmi':'viluq',   #10 c
 'vyaMsayAmi':'vyaMs',   #10 
 'saYcodayAmi':'saMcud',   #10 c
 'santarjayAmi':'saMtarj',   #10 c
 'sandAhayAmi':'saMdah',   #10 c
 'sanDArayAmi':'saMDf',   #10 c
 'sannisUdayAmi':'saMnisUd',   #10 not mw.  or saMnizUd
 'sannodayAmi':'saMnud',   #10 
 'samaBinayAmi':'samaBinI',   # not mw
 'samaBipUrayAmi':'samaBipF',   #10 
 'samaBisanDayAmi':'samaBisaMDe',   #10 c not mw
 'samApayAmi':'samAp',   #10 c
 'samArADayAmi':'samArAD',   #10 c
 'samAloqayAmi':'samAluq',   #10 c
 'samAsAdayAmi':'samAsad',   #10 
 'samunmUlayAmi':'samunmUl',   #10 
 'samprakIrtayAmi':'samprakIrt',   #10 c not mw
 'sampracodayAmi':'sampracud',   #10 c
 'samBartsayAmi':'samBarts',   #10 c not mw
 'samBAjayAmi':'samBaj',   #10 c
 'samloqayAmi':'saMluq',   #10 c
 'samvarmayAmi':'saMvarmaya',   # mw verb
 'samvastrayAmi':'saMvastraya', # 
 'saMSvayAmi':'saMSvi',   #10 c not mw

 'atipaTAmi':'atipaT',  # not mw (shld this be 'atipaW'?
 'aDigAyAmi':'aDigE',  # not mw
 'aDyasAmi':'aDyas',  # 
 'anupivAmi':'anupA',  # 
 'anuruDyAmi':'anuruD',  # 
 'anuSAsAmi':'anuSAs',  # 
 'antardaDAmi':'antarADA',  # 
 'apasedAmi':'apasad',  # not mw
 'aBipranamAmi':'aBipraRam',  # note 'n' bur vs. 'R' mw
 'aBimUrCAmi':'aBimUrC',  # not mw
 'aBizajAmi':'aBizaYj',  # 
 'aBizahAmi':'aBizah',  # 
 'aBiziYcAmi':'aBizic',  # 
 'aBizucyAmi':'aBisuc',  # suc not in bur!  also not in mw
 'aByasUyAmi':'aByasUya',  # 
 'aByAsadAmi':'aByAsad',  # 
 #'avaryAmi':'avarya',  # 
 'avaloYcAmi':'avaluYc',  # 
 'avasvapAmi':'avasvap',  # not mw
 'aSnItapibatIyAmi':'aSnItapibatIya',  # 
 'aSvasyAmi':'aSvasya',  # 
 'aSvAyAmi':'aSvAya',  # 
 'AkolAmi':'Akul',  # not mw
 'ApivAmi':'ApA',  # 
 'AvinajAmi':'Avij',  # 
 'ASAsAmi':'ASAs',  # 
 'AsadAmi':'Asad',  # 
 'utmandAmi':'unmad',  # bur 'utm' seems wrong
 'udgFRAmi':'udgF',  # 
 'udvfhAmi':'udvfh',  # 
 'unmaTnAmi':'unmanT',  # 
 'upaDyAmi':'upaDyE',  # 
 'upaScotAmi':'upaScut',  # not mw; mw has upaScyut
 'nimfkzAmi':'nimfkz',  # not mw
 'nirARahyAmi':'nirARah',  # not mw
 'nirunDAmi':'niruD',  # 
 'nirfRAmi':'nirf',  # 
 'nironayAmi':'nironI',  # not mw
 'nirgalAmi':'nirgal',  # not mw
 'nirgopAyAmi':'nirgup',  # 
 'nirRudAmi':'nirRud',  # 
 'nirvarzAmi':'nirvfz',  # not mw
 'niziYcAmi':'nizic',  # 
 'nizIvyAmi':'niziv',  # 
 'nizkUjAmi':'nizkUj',  # not mw
 'nizwakzAmi':'nistakz',  # note 'zw' v. mw 'st'
 'nizwanAmi':'nizwan',  # 
 'nizwapAmi':'nizwap',  # 
 'nizwaMsAmi':'nizwaMs',  # not mw
 'nisfjAmi':'nisfj',  # not mw
 'niskarzAmi':'nizkfz',  # note 'sk' vs. 'zk'
 'niHzeDAmi':'niHziD',  # 
 'niHsPulAmi':'niHsPul',  # not mw
 'nyagBavAmi':'nyagBU',  # not mw
 'nyantardaDAmi':'nyantarDA',  # not mw
 'nyasAmi':'nyas',  # 
 'nyfRAmi':'nyf',  # 
 'parARudAmi':'parARud',  # 
 'parijigAmi':'parigA',  # 
 'pariDvaMsAmi':'pariDvaMs',  # not mw
 'pariziYcAmi':'parizic',  # 
 'parizuvAmi':'parizU',  # 
 'parizkandAmi':'parizkand',  # 
 'parihvarAmi':'parihvf',  # not mw
 'prafRAmi':'prAr',  # pra+f
 'prakuwwAmi':'prakuww',  # not mw
 'prakzveqAmi':'prakzviq',  # not mw
 'prajigAmi':'pragA',  # 
 'praRidAmi':'praRido',  # not mw
 'praRidrAmi':'praRidrE',  # not mw
 'praRimAmi':'praRimA',  # not mw
 'praRiyAmi':'praRiyA',  # not mw
 'pratikarzAmi':'pratikfz',  # not mw
 'pratiyamAmi':'pratiyam',  # 
 'prativiSizRAmi':'prativiSiz',  # not mw
 'prativyUhAmi':'prativyUh',  # 
 'pratizeDAmi':'pratiziD',  # 
 'pratizkirAmi':'pratiskF',  # note 'zk' v. 'sk'
 'pradIvyAmi':'pradiv',  # 
 'pramIRAmi':'pramI',  # 
 'prayucCAmi':'prayuC',  # 
 'pravfhAmi':'pravfh',  # 
 'prasuvAmi':'prasU',  # 
 'prasvanAmi':'prasvan',  # not mw
 'prARakzAmi':'prARakz',  # not mw: pra+A+nakz
 'prez':'prez',  # Not sure why not found
 'prENKAmi':'prENK',  # not mw. pra+iNK 
 'prodlasAmi':'prollas',  # note sandhi diff: dl (bur) -> ll (mw)
 'proDarAmi':'prodDf',  # pra+ud+hf
 'prOKAmi':'prOK',  # not mw. pra + oK
 'vigadAmi':'vigad',  # not mw
 'viciyAmi':'vici',  # 
 'vicftAmi':'vicft',  # 
 'vidAmi':'vidA',  # bur shows from 'do'. MW 'do not separatle from 4 dA
 'vinimIlAmi':'vinimIl',  # not mw 
 'vinizkfntAmi':'vinizkft',  # not mw
 'vinyasAmi':'vinyas',  # 
 'vipraviDyAmi':'vipravyaD',  # not mw
 'virujAmi':'viruj',  # 
 'vilolAmi':'vilul',  # not mw
 'vivocAmi':'vivac',  # vivo.. vd.
 'viSravAmi':'visru',  # bur: cf. visravAmi
 'vizajAmi':'vizaYj',  # 
 'vizIvyAmi':'viziv',  #  bur error? [from] sIv  (rather than siv)
 'vizkandAmi':'vizkand',  # not mw.vi+skand
 'vizPurAmi':'visPur',  # 
 'vizyAmi':'vizo',  # 
 'viskandAmi':'viskand',  #  not mw
 'vI':'vI',  # 
 'vyapaviDyAmi':'vyapavyaD',  # not mw
 'vyamAmi':'vyam',  # not mw
 'vyavadfRAmi':'vyavadf',  # not mw
 'vyavasAmi':'vyavaso',  # 
 'vyAnakzAmi':'vyAnakz',  # no mw
 'vyAnudAmi':'vyAnud',  # no mw
 'vyucCAmi':'vyuz',  # ? 
 'vyfRvAmi':'vyf',  # 
 'saNkuwAmi':'saMkuw',  # not mw
 'saNGozAmi':'saMGuz',  # not mw
 'santfRAmi':'saMtfR',  # not mw
 'sannisfjAmi':'saMnisfj',  # not mw
 'sannyasAmi':'saMnyas',  # 
 'samatigacCAmi':'samatigam',  # not mw
 'samanUttizWAmi':'samanUtTA',  # not mw
 'samavasIdAmi':'samavasad',  # not mw
 'samavAkirAmi':'samavAkf',  # not mw
 'samAkroSAmi':'samAkruS',  # not mw
 'samAgalAmi':'samAgal',  # not mw
 'samutkirAmi':'samutkf',  # not mw
 'samudgranTAmi':'samudgranT',  # 
 'samupAkrAmAmi':'samupAkram',  # not mw
 'sampariBarAmi':'sampariBf',  # not mw
 'sampaSyAmi':'sampaS',  # 
 'sampraRidaDAmi':'sampraRiDA',  # 
 'sampraDyAyAmi':'sampraDyE',  # not mw
 'sampranftyAmi':'sampranft',  # not mw
 'samprasavAmi':'samprasu',  # not mw
 'sammahAmi':'sammah',  # not mw
 'samvfhAmi':'saMvfh',  # not mw
 'samvyavasyAmi':'saMvyavaso',  # not mw
 'saMSiSAmi':'saMSo',  # 
 'saMSlizAmi':'saMSliz',  # 

 # omi
 'vandIkaromi':'vandIkf',   # not mw
 'vikzaRomi':'vikzaR',   # not mw
 'viDunomi':'viDu',   # not mw
 'visinomi':'visi',   # 
 'vistaBnomi':'vizwamB',   # 
 'saYcinomi':'saMci',   # 
 'santanomi':'saMtan',   # 
 'santfpnomi':'saMtfp',   # 
 'sanDUnomi':'saMDU',   # 
 'samADUnomi':'samADU',   # not mw
 'samvfRomi':'saMvf',   # 
 'saMSinomi':'saMSi',   # not mw
 'niSinomi':'niSi',   # 
 'parikzaRomi':'parikzaR',   # not mw
 'pratiskunomi':'pratizku',   # 
 'pravitanomi':'pravitan',   # not mw
 'prASnomi':'prAS',   # 
 'aByujjuhomi':'aByudDu', # not mw.  aBi+ud+hu
 'upasaNkaromi':'upasaMkf',   # not mw

 'aBizunomi':'aBizu',  #
 'aBisaMstaBnomi':'aBisaMstamB',  #
 'avazwaBnomi':'avazwamB',  #
 'ADunomi':'ADu',  #
 'parizuRomi':'parizu',  #
 'parizkaromi':'parizkf',  #
 'pratisaMskaromi':'pratisaMskf',  #
 'prahiRomi':'prahi',  #
 'vizkaBnomi':'vizkamB',  #
 'saMskaromi':'saMskf',  #
 'saMstaBnomi':'saMstamB',  #
 
 # 'e' ending (Atmanepada)
 'aDijage':'aDigA',
 'aDiruhe':'aDiruh',
 'aDivADe':'aDibAD',  # bAD = vAD
 'anumude':'anumud',
 'anuzajje':'anuzajj',
 'anUcye':'anUc',
 'apavADe':'apabAD',
 'aBipariplave':'aBipariplu',
 'aBipede':'aBipad', # perf
 'aBiruhe':'aBiruh',
 'aBivfDe':'aBivfD',
 'aByAse':'aByas',
 'avaSizye':'avaSiz',
 'Aprekze':'Aprekz',  # A+pra+Ikz
 'AvADe':'AbAD', # bAD = vAD
 'ujjihe':'udDA', # ud + hA
 'udvepe':'udvep',
 'upASnave':'upAS',  # upa+aS
 'upAse':'upAs',   # upa + As

 'nidIDye':'nidIDI',  # not mw
 'nirodaDe':'tiroDA',  # niro for tiro
 'nirRIye':'nirRI',  #
 'nirvidye':'nirvid',  #
 'niSIye':'niSad',  # not mw
 'nizaje':'nizaYj',  #
 'nizahe':'nizah',  #
 'nizeve':'nizev',  #
 'nihIye':'nihA',  #
 'parikzIye':'parikzi',  #
 'pariKaRqe':'pariKaRq',  # not mw. MW KaRq not a root
 'paridUye':'paridu',  #
 'pariSIrye':'pariSF',  # ps.
 'parizahe':'parizah',  #
 'parizeve':'parizev',  #
 'parizvaje':'parizvaj',  #
 'parisamApye':'parisamAp',  #
 'parihIye':'parihA',  #
 'palAye':'palAy',  #

 'prakzIye':'prakzi',  #
 'praqIye':'praqI',  # not mw
 'praRimaye':'praRime',  # not mw
 'praRiMse':'praRiMs',  # not mw, pra + niMs
 'pratijare':'pratijF',  # vd.
 'pratidfSye':'pratiduh',  #
 'pratisaYjAye':'pratisaMjYA',  #
 'pratisamucye':'pratisamuc', # not mw
 'pratisamboDe':'pratisaMbuD',  # not mw
 'pratILe':'pratIl',  # not mw
 'pratyanunIye':'pratyanunI',  #
 'pratyupapadye':'pratyupapad',  # not mw
 'pradIdye':'pradIDI',  # not mw
 'pradfSye':'pradfS',  #
 'praparAye':'prapare',  # ? pra + parA + i not mw
 'prasajye':'prasaYj',  #
 'prasiYcye':'prasic',  #

 'preje':'prej',  # not mw  pra_ej
 'preLe':'preL',  # not mw  pra+IL
 'protSale':'protSal',  # not mw pra+ud+Sal
 'vikawWe':'vikatT',  # not mw.  Also, bur has no word kawW 
 'vicikite':'vikit',  # not mw
 'vinizUde':'vinisUd',  # not 'z' vs. 's'
 'vipaRe':'vipaR',  #
 'viByase':'viByas',  # not mw
 'viruDye':'viruD',  #
 'viSIrye':'viSF',  # ps.
 'viSrUye':'viSru',  #
 'vizahe':'vizah',  #
 'vizeve':'vizev',  #
 'vizyande':'vizvaYj',  #
 'vihave':'vihve',  # vd. hU for hve.  hU not marked as MW verb.

 'vyajye':'vyaYj',  #
 'vyatire':'vyatirA',  # ? 
 'vyatilUne':'vyatilU',  #
 'vyatihe':'vyatyas',  # Huet: middle 1s of cl. 2 as is 'he' !
 'vyaSnave':'vyaS',  #
 'vyApriye':'vyApf',  #
 'vyucCidye':'vyucCid',  #

 'saNkIrye':'saMkF',  # 
 'saNkzIye':'saMkzi',  #
 'samakze':'samakz',  # not mw
 'samaSnave':'samaS',  #
 'samAyate':'samAyat',  # not mw
 'samfYje':'samfYj',  # not mw
 'samparidahye':'samparidah',  #
 'sampalAye':'sampalAy',  #
 'samprakASe':'samprakAS',  #
 'sampratyAcakze':'sampratyAcakz',  # not mw
 'sampradfSye':'sampradfS',  #
 'sampravyaTe':'sampravyaT',  # not mw
 'sampriye':'samprI',  #
 'samvide':'saMvid',  #
 'saMsajye':'saMsaYj',  #
 'saMsvaje':'saMsvaYj',  #

 'atiBravImi':'atiBrU',  # not mw
 'anurodmi':'anurud',  # 
 'aBipiparmi':'aBipF',  # 
 'aBirunaDmi':'aBiruD',  # 
 'avaCinadmi':'avacCid',  # 
 'utBinadmi':'udBid',  # note bur 'utB'

 'nirvfRajmi':'nirvfj',  # not mw
 'nizvapimi':'nizvap',  # not mw ni+svap
 'nistOmi':'nizwu',  #   # note 'st' v. 'zw'

 'pariCinadmi':'paricCid',  # 
 'paryudvinajmi':'paryudvij',  # 
 'palyemi':'pare',  # palyemi for paryemi
 'prakzunadmi':'prakzud',  # 
 'prakzOmi':'prakzu',  # not mw
 'praciketmi':'prakit',  # not mw
 'prajakzimi':'prajakz',  # not mw
 'praRidehmi':'praRidih',  # not mw pra+ni+dih
 'prapfnacmi':'prapfc',  # 

 'prodyemi':'prodi',  # 

 'viCinadmi':'vicCid',  # 
 'vinirBanajmi':'BaYj',  # not mw
 'vinizpiRazmi':'vinizpiz',  # 

 'sampfnacmi':'sampfc',  # 
 'samvinajmi':'saMvij',  # 
 'pariveda':'parivid',
 'Agahi':'Agam',  # imp. vd.

 'avaroruDam':'avaruD',  # 
 'upaDAkzizam':'upadah',  # a1
 'upaDAkzizam':'upadah',  # a1
 'upADmAsizam':'upaDmA',  # a1
 'nivadDvam':'nivas',  # 
 'vyaDamam':'viDmA',  # 
 'saYcIvaraye':'saMcIvaraya',  #consider a verb non-prefixed, as bur no cIvaraya
}

def roman_slp1_mw(root0,cat,d):
 # root  in IAST. May have parens, period
 root = re.sub(r'[.,;:]$','',root0)
 root = re.sub(r'[()]','',root)
 root_slp1 = transcoder.transcoder_processString(root,'roman','slp1')
 #if root0 == '(labh)':print('roman_slp1_mw check: %s -> %s ->%s'%(root0,root,root_slp1))
 if root_slp1 not in d:
  return None
 mwrec = d[root_slp1]
 if mwrec.cat != cat:
  print('roman_slp1_mw %s -> %s. Expected %s, but got %s'%(
         root,root_slp1,cat,mwrec.cat))
  return None
 return root_slp1

def map2mw_D_2(d,k1,entry,mwverbs):
 line = entry.datalines[0]
 m = re.search(u'Ami#}¦ {%[^%]*%}[0-9 ,;]+{%\((.*?)\)%}',line)
 if not m:
  return None
 root = m.group(1)  # in IAST
 root_slp1 = roman_slp1_mw(root,'preverb',d)
 return root_slp1

def match_spelling(k1,cformsd):
 if k1 in cformsd:
  return k1
 k1a = homorganic_nasal(k1)
 if k1a in cformsd:
  return k1a
 k1a = re.sub(r'sa[NYR]','saM',k1)
 if k1a in cformsd:
  return k1a
 k1a = re.sub('san([tTdDn])',r'saM\1',k1)
 #if k1 == 'santapAmi':print('spell chk',k1,k1a)
 if k1a in cformsd:
  return k1a
 k1a = re.sub('sam([yrlv])',r'saM\1',k1)
 if k1a in cformsd:
  return k1a
 return None
def map2mw_D_1(d,k10,cformsd):
 k1 = match_spelling(k10,cformsd)
 if k1 != None:
  recs = cformsd[k1]
  #hws = [r.k1 for r in recs]
  # k1 is believed to be present as of one of the headwords in hws list
  for rec in recs:
   mw = rec.k1
   if mw not in d:
    # unexpected
    print('map2mw_D_1 Warning: %s not in mwverbs (for k1=%s)'%(mw,k1))
   else:
    rec.used = True
    return mw

 return None

def map2mw_D(d,k1,entry,mwverbs,cformsd):
 """ for bur. 'entry' is the record in bur.txt 
     structure is from class Entry in bur_verb_filter
     'd' is dictionary into mwverbs1
     k1 should be a 'derived' root, given in first person s
      - a prefixed root
      - a desi
 """
 if k1 in map2mw_special_D:
  return map2mw_special_D[k1]
 ans = map2mw_D_1(d,k1,cformsd)
 if ans:
  return ans
 return '?'
 ans = map2mw_D_2(d,k1,entry,mwverbs)
 if ans:
  return ans
 
 k = re.sub(r'Ami$','',k1) 
 if k in d:
  mwrec = d[k]
  if mwrec.cat == 'preverb':
   return k

 return '?'

map2mw_special_Des = {
 'IzizAmi':'i',
 'ediDize':'eD',
 'ezizizAmi':'iz',
 'ozizizAmi':'uz',
 'cikzaYjize':'kzaj',  # bur shows kzaYj, an alternate of kzaj
 'cukuzizAmi':'kuz',
 'cucyutizAmi':'cyut',
 'jigarizAmi':'gF',
 #'jiGApayizAmi':'hi',
 'jijizizAmi':'jiz',
 'jijYApayizAmi':'jYA',
 'jIpsyAmi':'jYA',
 'juGuzizAmi':'Guz',
 'jujuzize':'juz',
 'tizwigize':'stiG',  # bur has 'stig', but 'stig' not found in bur or mw
 'tistarizAmi':'stf',
 'tutohizAmi':'tuh',
 'didyUtize':'dyut',
 'diDarize':'Df',
 'dipsAmi':'daB', #vd
 'dIpsAmi':'damB', #vd
 'nijiGfkzayizAmi':'nigrah',
 #'pariprepsAmi':'Ap',
 'pipIzAmi':'pA', #vd
 'pratiSuSruzAmi':'pratiSru', #pfx
 'pratIzizAmi':'pratI',  # pfx
 'biBaNkzAmi':'BaYj',  # bur has 'baYj', probably print error
 'buboDizAmi':'buD',
 'rurucize':'ruc',
 'laGayAmi':'laGaya',  #laGaya  Not desiderative ?
 'vijigIzu':'ji',
 'vivIzAmi':'vI',
 'viSiSvAsayizAmi':'viSvas',  # pfx
 'vfzasyAmi':'vfz', #?
 'vyApupUrze':'vyApf', # pfx
 'SISAMsAmi':'SAn',  # bur 'SAna'
 'sisyandize':'syand',
 'jijarizAmi':'jF',  # 
 'jugupizAmi':'gup',  # 
 'didarizAmi':'df',  # des
 'didarizAmi':'df',  # des
 'dIdAMsAmi':'dAn',  # des
 'piparcizAmi':'pfc',  # des
 'ciklikzAmi':'kliS',
 'ciklitsAmi':'klid',
 'vivitse':'vid',  # Desiderative
 'aBilipsAmi':'aBilaB',  
 'utsisAhayizAmi':'utsah',  
 'upaSikzAmi':'upaSak',  
 'pariprepsAmi':'pariprAp',  
 'pariripse':'pariraB',  
 #'pariprepsAmi':'pariprAp',  
 'parIpsAmi':'paryAp',  
 'pradidfkzAmi':'pradfS',  
 'prayuyutse':'prayuD',  
 'pravivikzAmi':'praviS',  
 'prasizAsAmi':'prasan',  
 'vicikitsAmi':'vikit',  
 'vijigIzu':'viji',  
 'vijugupse':'vigup',  
 'viDitse':'viDA',  
 'sammimikzAmi':'sammih',  
 'saMsismaye':'saMsmi',  

}
def map2mw_Des(d,k1,entry):
 """ for bur. 'entry' is the record in bur.txt 
     structure is from class Entry in bur_verb_filter
     'd' is dictionary into mwverbs1
     
 """
 if k1 in map2mw_special_Des:
  return map2mw_special_Des[k1]
 regexes = [
  u'<ab>dés.</ab> de {%(.*?)%}',
  u'<ab>dés.</ab> {%(.*?)%}',
  u'<ab>dés.</ab> du <ab>c.</ab> de {%(.*?)%}',

 ]
 line = entry.datalines[0] # first line of entry in bur.txt
 for regex in regexes:
  m = re.search(regex,line)
  if m:
   root = m.group(1)  # root in 
   root_slp1=roman_slp1_mw(root,'verb',d)
   if root_slp1 != None:
    return root_slp1

 return '?'

map2mw_special_Aug = {
 'arIyarmi':'f',
 'canIskandmi':'skand',
 'carIkarImi':'kf',
 'carIkardmi':'kft',
 'carICardmi':'Cfd',
 'cAkrandmi':'krand',
 'cAkzaYjye':'kzaj',  # bur kzaYj.  
 'cAKAdye':'KAd',
 'cekrIqye':'krIq',
 'ceCedmi':'Cid',
 'cokUjmi':'kUj',
 'jAglAye':'glE',
 'jAharmi':'hary',
 'jAhAmi':'hay',
 'jehigmi':'hikk',
 'johomi':'hu',  # or 'hve'
 #'johomi':'',  # 
 'tAtUrmi':'tvar',  # bur tUr
 'tAstarmi':'stf', # or stF
 'tAstalye':'sTal',  # bur print error? he has no 'stal' entry
 'danIDvaMsmi':'DvaMs',
 'danDranmi':'DraR',  # bur has Dran - but no verb found ?
 'davidyutat':'dyut', # vd.
 'dAdrAmi':'drA',
 'dADarmi':'Df',
 'dADyAmi':'DyE',
 'dedIye':'dI',
 'nenemi':'nI',
 'parijarBurAmi':'parihf', # preverb
 'pApacmi':'pac',
 'banIBraMsmi':'BraMs', # or BraMS
 'bABAmi':'BA',
 'bABrajjmi':'Brajj',
 'beBemi':'BI',
 'boBomi':'BU',
 'yoyojmi':'yuj',
 'yoyomi':'yu',
 'rAraYjmi':'raYj',  # bur has 'ranj', probable print error
 'rAramBImi':'raB',
 'rerIye':'ri',
 'roromi':'ru',
 'vanIvacye':'van',  # ? bur has 'vane', but no such verb. mw also vanIya
 'vevIye':'vI',
 'vevemi':'vI',
 'SeSremi':'Sri',  # or SrI
 'sIzape':'sap',  # vd.
 'cAKyAmi':'KyA',  # 
 'cAcCAmi':'Co',  # 
 'jAjYAmi':'jYA',  # Aug
 'tantasyAmi':'taMs',  # Aug
 'SASrAmi':'SrA',  # Aug
 'boBojmi':'Buj',
 'popomi':'pU',
 'caYcUrye':'car',  # Aug
 'carIkfzye':'kfz', # aug
 'calIkalpye':'kxp', #aug
 'jariharmi':'hf',  # aug.
 'jarIGardmi':'gfD',  # aug.
 'jAgAhmi':'gAh',  #  aug.
 'jeGemi':'hi',  # aug.
 'jejayImi':'ji',  # aug.
 'jejremi':'jri',  # aug
 'jehremi':'hrI',  # aug
 'jogohmi':'guh',  # aug
 'lelehmi':'lih',  # aug.
 'sAsahmi':'sah',  # aug
    'apaSoSucAmi':'apaSuc', # aug
    'ASoSucAmi':'ASuc',
 'parimarmfjye':'parimfj',
 'pravevedmi':'pravid',
 'vicAkASye':'vikAS',
 'vijAye':'viji',
 'vidardarmi':'vidF',
 'vibAbaDye':'vibanD',
 'vimAmfje':'vimfj',
 'saMsanIzyande':'saMsyand',
 
}
def map2mw_Aug(d,k1,entry):
 """ for bur. 'entry' is the record in bur.txt 
     structure is from class Entry in bur_verb_filter
     'd' is dictionary into mwverbs1
     Aug = Intensive
 """
 L = entry.metad['L']
 if L in ['7201','7202']:  # 7203 relates to 'hay'
  return 'hA'
 if k1 in map2mw_special_Aug:
  return map2mw_special_Aug[k1]
 regexes = [
  u'<ab>aug.</ab> de {%(.*?)%}',
  u'<ab>aug.</ab> {%(.*?)%}',
  u'<ab>aug.</ab> du <ab>c.</ab> de {%(.*?)%}',

 ]
 line = entry.datalines[0] # first line of entry in bur.txt
 for regex in regexes:
  m = re.search(regex,line)
  if m:
   root = m.group(1)  # root in 
   root_slp1=roman_slp1_mw(root,'verb',d)
   if root_slp1 != None:
    return root_slp1

 return '?'
map2mw_special_C = {
 'aDyApayAmi':'aDI',
 'aDyAropayAmi':'aDyAruh',
 'anudarSayAmi':'anudfS',
 'anurocayAmi':'anuruc',
 'anuSikzayAmi':'anuSikz',
 'aBidarSayAmi':'aBidfS',
 'aBiprasAdayAmi':'aBiprasad',
 'aBiraYjayAmi':'aBiraYj',
 'aBirADayAmi':'aBirAD',
 'aBirocaye':'aBiruc',
 'aBivAdayAmi':'aBivad',
 'aBiSikzayAmi':'aBiSikz',
 'aByanumodayAmi':'aByanumud',
 'aByavanAmayAmi':'aByavanam',
 'avaDAvayAmi':'avaDU',
 'avasAyAmi':'avaso',
 'AkzArayAmi':'Akzar',

 'AdIpayAmi':'AdIp',  # 
 #'AnayAmi':'',  # 
 'AnartayAmi':'Anft',  # 
 'AnAmayAmi':'Anam',  # 
 'ApyAyAmi':'ApyE',  # 
 'ArADayAmi':'ArAD',  # 
 'Arocaye':'Aruc',  # 
 'AvindayAmi':'Avid',  # 
 'AvedayAmi':'Avid',  # 
 'ASrAvayAmi':'ASru',  # 
 #'AsayAmi':'',  # 
 #'AsayAmi':'',  # 
 'AsecayAmi':'Asic',  # 
 'AhlAdayAmi':'AhlAd',  # 
 'uttArayAmi':'uttF',  # 
 'utpAwayAmi':'utpaw',  # 
 'utpAdayAmi':'utpad',  # 
 'utPAlayAmi':'utPal',  # 
 'utsAdayAmi':'utsad',  # 
 'utsArayAmi':'utsf',  # 
 'uddIpayAmi':'uddIp',  # 
 'udBAvayAmi':'udBU',  # 
 'udBAsayAmi':'udBAs',  # 
 'udvejayAmi':'udvij',  # 
 
 'upadarSayAmi':'upadfS',  # 
 'upadIpayAmi':'upadIp',  # 
 'upavfMhayAmi':'upavfMh',  # 
 'upaveSayAmi':'upaviS',  # 
 'upaSozayAmi':'upaSuz',  # 
 'upaSlezayAmi':'upaSliz',  # 
 'upasTApayAmi':'upasTA',  # 

 'niGAtayAmi':'nihan',  # 
 'nicAyAmi':'nici',  # 
 'nidarSayAmi':'nidfS',  # 

 'niDApayAmi':'niDA',  # 
 'niDArayAmi':'niDf',  # 
 'niranDayAmi':'niraD',  # 
 'nirAmayAmi':'niram',  # 
 'nirvartayAmi':'nivft',  # 
 'nirvApana':'nirvA',  # 
 'nirvApayAmi':'nirvA',  # 
 'nirvAsayAmi':'nirvas',  # 
 'nirvAhayAmi':'nirvah',  # 
 'nivArayAmi':'nivf',  # 
 'nivAsaye':'nivas',  # 
 'nizecayAmi':'nizic',  # 
 'nizkAsayAmi':'nizkas',  # 
 'nizpArayAmi':'nizpF',  # 
 'niHSezayAmi':'niHSiz',  # 
 'niHsrAvayAmi':'niHsru',  # 
 'nyarpayAmi':'nyf',  # 
 'parikalpayAmi':'parikxp',  # 
 'paritarpayAmi':'paritfp',  # 
 'pariDArayAmi':'pariDf',  # 
 'pariprezayAmi':'pariprez',  # 
 'pariBojayAmi':'pariBuj',  # 
 'pariloqayAmi':'pariluq',  # 
 'pariloBayAmi':'pariluB',  # 
 'parivarjayAmi':'parivfj',  # 
 'pariSAmayAmi':'pariSam',  # 
 'pariSezayAmi':'pariSiz',  # 
 'pariSoDayAmi':'pariSuD',  # 
 'parizWApayAmi':'parizWA',  # 
 'parisADayAmi':'parisAD',  # 
 'pariharzAmi':'parihfz',  # 
 #'paryAlocayAmi':'paryA',  # 
 'paryASvasayAmi':'paryASvas',  # 
 'paryAsayAmi':'paryAs',  # 
 'prakzepayAmi':'prakzip',  # 
 'pracAtayAmi':'pracat',  # 
 'pracetayAmi':'pracit',  # 
 'prajAnayAmi':'prajan',  # 
 'prajYApayAmi':'prajYA',  # 
 'pratArayAmi':'pratF',  # 
 'pratikampayAmi':'pratikamp',  # 
 'pratidarSayAmi':'pratidfS',  # 
 'pratidozayAmi':'pratiduz',  # 
 'pratipAdayAmi':'pratipad',  # 
 'pratipAlayAmi':'pratipA',  # 
 'pratirocayAmi':'pratiruc',  # 
 'pratirohayAmi':'pratiruh',  # 
 'prativArayAmi':'prativf',  # 
 'prativAsayAmi':'prativas',  # 
 'pratisTApayAmi':'pratisTA',  # 
 'pratyarpayAmi':'pratyf',  # 
 'pratyavaropayAmi':'pratyavaruh',  # 
 'pratyAyayAmi':'pratI',  # 

 'pradApayAmi':'pradA',  # 
 'pradAmayAmi':'pradam',  # 
 'praDAvayAmi':'praDAv',  # 
 'praDmApayAmi':'praDmA',  # 
 'praDvaMsayAmi':'praDvaMs',  # 
 'pramApayAmi':'pramI',  # 
 'praramayAmi':'praram',  # 
 'pravedayAmi':'pravid',  # 
 'praSamayAmi':'praSam',  # 
 'praSAdayAmi':'praSad',  # 
 #'prasADayAmi':'pra',  # 
 'prastApayAmi':'prastA',  # 
 'prAjana':'prAj',  # pra+aj
 #       'prAyayAmi':'prI',  # verb
 #       'prAvayAmi':'pru',  # 
 'prArTana':'prArt',  # 
 'protsarayAmi':'protsf',  # 
 'protsAdayAmi':'protsad',  # 

 'vikAsayAmi':'vikas',  # 
 'vikzoBayAmi':'vikzuB',  # 
 'vicAlayAmi':'vical',  # 
 'vidarSayAmi':'vidfS',  # 
 'viDArayAmi':'viDf',  # 
 'vinAdayAmi':'vinad',  # 
 'vinAmayAmi':'vinam',  # 
 'vinivedayAmi':'vinivid',  # 
 'viniveSayAmi':'viniviS',  # 
 'vipAwayAmi':'vipaw',  # 
 'vipAtayAmi':'vipat',  # 
 'vipoTayAmi':'vipuT',  # 
 'vipramohayAmi':'vipramuh',  # 
 'vibIBayAmi':'viBI',  # 
 'vimArdayAmi':'vimfd',  # 
 'vimocayAmi':'vimuc',  # 
 'vimohayAmi':'vimuh',  # 
 'viyojayAmi':'viyuj',  # 
 'virAYjayAmi':'viraYj',  # 
 'vilAyayAmi':'vilI',  # 
 'vilAlayAmi':'vilI',  # 
 'vivarjayAmi':'vivfj',  # 
 'viSAdayAmi':'viSad',  # 
 'viSoDayAmi':'viSuD',  # 
 'viSozayAmi':'viSuz',  # 
 'visarjayAmi':'visfj',  # 

 'vyanunAdayAmi':'vyanunad',  # 
 'vyaparopayAmi':'vyaparuh',  # 
 'vyAGArayAmi':'vyAGf',  # 
 #'vyAcayAmi':'',  # 
 'vyApadayAmi':'vyApad',  # 
 'vyApayAmi':'vI',  # vi + i, c.
 'vyAmohayAmi':'vyAmuh',  # 
 'vyAyayAmi':'vI',  # 
 #'vyAyayAmi':'',  # 
 #'vyerayAmi':'',  # 
 'saNkopayAmi':'saMkup',  # 
 'saNgfBayAmi':'saMgrah',  # 
 'saYCAdayAmi':'saMCad',  # 
 'saYjanayAmi':'saMjan',  # 
 'saYjAnayAmi':'saMjan',  # 
 'saYjvAlayAmi':'saMjval',  # 
 'santarpayAmi':'saMtfp',  # 
 'santArayAmi':'saMtF',  # 
 'sandarSayAmi':'saMdfS',  # 

 'samanukalpayAmi':'samanukxp',  # 
 'samardayAmi':'samard',  # 
 'samarpayAmi':'samf',  # 
 'samavaSezye':'samavaSiz',  # 
 'samavaskandayAmi':'samavaskand',  # 
 'samavasTApayAmi':'samavasTA',  # 

 'samAyojayAmi':'samAyuj',  # 
 'samAvedayAmi':'samAvid',  # 

 'samutpAwayAmi':'samutpaw',  # 
 'samutsAdayAmi':'samutsad',  # 
 'samutsAhayAmi':'samutsah',  # 
 'samupavfMhayAmi':'samupavfMh',  # 
 'sampariharzayAmi':'samparihfz',  # 
 'samprakalpita':'samprakxp',  # 
 'sampratiSrAvayAmi':'sampratiSru',  # 
 'sampraDArayAmi':'sampraDf',  # 
 'samprasAraRa':'samprasf',  # 
 'samyAjayAmi':'saMyaj',  # 
 'samlepayAmi':'saMlip',  # 
 'samviBAjayAmi':'saMBaj',  # 
 #'sarjayAmi':'',  # 
 'saMSamayAmi':'saMSam',  # 
 'saMSAtayAmi':'saMSad',  # 
 'saMSoDayAmi':'saMSuD',  # 
 'saMSozayAmi':'saMSuz',  # 
 'saMsADayAmi':'saMsAD',  # 

 'AwayAmi':'aww',
 'AnartayAmi':'Anft',
 'utTApayAmi':'utTA',
 'unnAmayAmi':'unnam',
 'upArADayAmi':'upArAD',
 'ezayAmi':'iz',
 'Ecikzam':'Ikz',
 'EwiWam':'eW',
 'Ezizam':'iz',
 'ozayAmi':'uz',
 'ORiRam':'oR',
 'kzepayAmi':'kzip',
 'cyotayAmi':'cyut',
 'jezayAmi':'jiz',
 'tvezayAmi':'tviz',
 'dApayAmi':'de',  # or dE or do
 'DAvayAmi':'DAv',
 'paryAlocayAmi':'paryAloc',
 'pIpayAmi':'pA',
 'pUraka':'pF',
 'pratyAyayAmi':'pratI',
 'prasADayAmi':'prasAD',
 'BApayAmi':'BA',
 'BArayAmi':'Bf',
 'BIzaye':'BI',
 'rAjayAmi':'rAj',
 'rADayAmi':'rAD',
 'vAyayAmi':'vI',
 'vikAsayAmi':'vikas',
 'vyaYjayAmi':'vyaYj',
 'saNgfBayAmi':'saMgrah',
 'saYjAnayAmi':'saMjan',
 'sAvayAmi':'su',
 'skandayAmi':'skand',
 'hrepayAmi':'hrI',



}

def map2mw_C(d,k1,entry):
 """ for bur. 'entry' is the record in bur.txt 
     structure is from class Entry in bur_verb_filter
     'd' is dictionary into mwverbs1
     C = Causal
 """
 if k1 in map2mw_special_C:
  return map2mw_special_C[k1]
 regexes = [
  u'<ab>c.</ab> de {%(.*?)%}',
  u'<ab>c.</ab> {%(.*?)%}',
  #u'<ab>c.</ab> du <ab>c.</ab> de {%(.*?)%}',

 ]
 line = entry.datalines[0] # first line of entry in bur.txt
 for regex in regexes:
  m = re.search(regex,line)
  if m:
   root = m.group(1)  # root in 
   root_slp1=roman_slp1_mw(root,'verb',d)
   if root_slp1 != None:
    return root_slp1

 return '?'

map2mw_special_F = {
 'aruzyati':'f',
 'elizyAmi':'il',
 'ezizyAmi':'iz',
 #'cakAsmi':'',
 'jahizyAmi':'hA',
 'taruzyAmi':'tF',
 #'pA':'',
 'yAvizye':'yu',
 #'ruc':'',
 'lezye':'lI',
 'kAsyAmi':'kE',  # 
}
def map2mw_F(d,k1,entry):
 """ for bur. 'entry' is the record in bur.txt 
     structure is from class Entry in bur_verb_filter
     'd' is dictionary into mwverbs1
     F = 2nd future
 """
 if k1 in map2mw_special_F:
  return map2mw_special_F[k1]
 regexes = [
  u'<ab>f2.</ab> de {%(.*?)%}',
  u'<ab>f2.</ab> {%(.*?)%}',
  #u'<ab>f2.</ab> du <ab>c.</ab> de {%(.*?)%}',

 ]
 line = entry.datalines[0] # first line of entry in bur.txt
 for regex in regexes:
  m = re.search(regex,line)
  if m:
   root = m.group(1)  # root in 
   root_slp1=roman_slp1_mw(root,'verb',d)
   if root_slp1 != None:
    return root_slp1

 return '?'

def burmap(recs,mwd,entry_Ldict,mwverbs,cformsd):
 
 for rec in recs:
  # try mw spelling directly
  if rec.k1 in['garayAmi']:print('burmap chk:',rec.k1,rec.code)
  if rec.code in ['R']:
   rec.mw,matchflag = map2mw_R(mwd,rec.k1)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
   else:
    #print('burmap anomaly:',rec.k1,rec.mw,rec.mw in mwd)
    pass
  elif rec.code == 'Des':
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_Des(mwd,rec.k1,entry)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
  elif rec.code == 'Aug':
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_Aug(mwd,rec.k1,entry)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
  elif rec.code == 'C':  # causal
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_C(mwd,rec.k1,entry)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
  elif rec.code == 'F':  # 2nd future
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_F(mwd,rec.k1,entry)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
   """
  elif rec.code == 'Den':  # Denominative
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_Den(mwd,rec.k1,entry)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
  """
  elif rec.code == 'D':
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw = map2mw_D(mwd,rec.k1,entry,mwverbs,cformsd)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]

bur_preverb_parses = {
 'atipaT':'ati+paT',  #
 'atiBrU':'ati+BrU',  #
 'aDigE':'aDi+gE',  #
 'anuzajj':'anu+saYj',  #
 'anUc':'anu+vac',  #
 'anvASri':'anu+A+Sri',  #
 'apasad':'apa+sad',  #
 'aBigup':'aBi+gup',  #
 'aBipariplu':'aBi+pari+plu',  #
 'aBipal':'aBi+pal',  #
 'aBimUrC':'aBi+mUrC',  #
 'aBisuc':'aBi+suc',  #
 'aByucCri':'aBi+ud+Sri',  #
 'aByudDu':'aBi+ud+hu',  #
 'avasvap':'ava+svap',  #
 'Akul':'A+kul',  #
 #  'aMh':'aMh',  # pf. of aMh
 'Aprekz':'A+pra+Ikz',  #
 #'iry':'iry',  #
 #'Iry':'Iry',  #
 'upaScut':'upa+Scut',  #
 'upasaMkf':'upa+sam+kf',  #
 #'Uw':'Uw',  #
 #'fkz':'fkz',  #
 #'U':'U',  #
 #'guru':'guru',  #
 #'kliz':'kliz',  #
 #'gfB':'gfB',  #
 #'gfmB':'gfmB',  #
 #'%jri':'%jri',  #
 #'stig':'stig',  #
 #'tfptAya':'tfptAya',  #
 #'tab':'tab',  #
 'nidIDI':'ni+dIDI',  #
 'nimfkz':'ni+mfkz',  #
 'nirARah':'nir+A+nah',  #
 'nironI':'niras+nI',  #
 'nirgal':'nir+gal',  #
 'nirvfz':'nir+vfz',  #
 #'nirvas':'nir+vas',  #
 'nirvfj':'nir+vfj',  #
 'niSad':'ni+Sad',  #
 'nizkUj':'nis+kUj',  #
 'nizwaMs':'nis+taMs',  #
 'nizpF':'nis+pF',  #
 'nizvap':'ni+svap',  #
 'nisfj':'ni+sfj',  #
 'niHsPul':'niH+sPul',  #
 'nyagBU':'nyag+BU',  #
 'nyantarDA':'ni+antar+DA',  #
 'parikzaR':'pari+kzaR',  #
 'pariKaRq':'pari+KaRq',  #
 'pariDvaMs':'pari+DvaMs',  #
 'parivaMS':'pari+vaMS',  #
 'pariSam':'pari+Sam',  #
 'parihvf':'pari+hvf',  #
 'prakuww':'pra+kuww',  #
 'prakzu':'pra+kzu',  #
 'prakzviq':'pra+kzviq',  #
 'prakit':'pra+kit',  #
 'prajakz':'pra+jakz',  #
 'praqI':'pra+qI',  #
 'praRido':'pra+ni+do',  #
 'praRidih':'pra+ni+dih',  #
 'praRidrE':'pra+ni+drE',  #
 'praRiDe':'pra+ni+De',  #
 'praRime':'pra+ni+me',  #
 'praRimA':'pra+ni+mA',  #
 'praRiyA':'pra+ni+yA',  #
 'praRiMs':'pra+niMs',  #
 'pratikfz':'prati+kfz',  #
 'pratiCad':'prati+Cad',  #
 'pratijF':'prati+jF',  #
 'pratiduz':'prati+duz',  #
 'pratinirji':'prati+nir+ji',  #
 'pratipA':'prati+pA',  #
 'prativiSiz':'prati+vi+Siz',  #
 'pratisamuc':'prati+sam+uc',  #
 'pratisaMbuD':'pratisam+buD',  #
 'pratisTA':'prati+sTA',  #
 'pratIL':'prati+IL',  #
 'pratyupapad':'prati+upa+pad',  #
 'pradIDI':'pra+dIDI',  #
 'pradIv':'pra+dIv',  #
 'prapare':'pra+parA+i',  #
 'prapal':'pra+pal',  #
 'pravitan':'pra+vi+tan',  #
 'prastA':'pra+stA',  #
 'prasvan':'pra+svan',  #
 #'prAj':'prAj',  #
 'prARakz':'pra+A+nakz',  #
 'prej':'pra+ej',  #
 'preL':'pra+IL',  #
 'prENK':'pra+iNK',  #
 'procCri':'pra+ut+Sri',  #
 'protSal':'pra+ut+Sal',  #
 'prOK':'pra+uK',  #
 'vandIkf':'vandI+kf',  #
 #'vikawW':'vi+kawW',  #
 'vikzaR':'vi+kzaR',  #
 'vigad':'vi+gad',  #
 'vikit':'vi+kit',  #
 'viDu':'vi+Du',  #
 'vinimIl':'vi+ni+mIl',  #
 'vinizkft':'vi+nis+kft',  #
 'vipay':'vi+pay',  #
 'vipravyaD':'vi+pra+vyaD',  #
 'viByas':'vi+Byas',  #
 'vilul':'vi+lul',  #
 'viSad':'vi+Sad',  #
 'vizkand':'vi+skand',  #
 'visi':'vi+si',  #
 'viskand':'vi+skand',  #
 'vyapavyaD':'vi+apa+vyaD',  #
 'vyam':'vi+am',  #
 'vyavadf':'vi+ava+df',  #
 'vyAnakz':'vi+A+nakz',  #
 'vyAnud':'vi+A+nud',  #
 'saMkuw':'sam+kuw',  #
 'saMGuz':'sam+Guz',  #
 'saMtfR':'sam+tfR',  #
 'saMnisUd':'sam+ni+sUd',  #
 'saMnisfj':'sam+ni+sfj',  #
 'samakz':'sam+akz',  #
 'samatigam':'sam+ati+gam',  #
 'samanUtTA':'sam+anu+sTA',  #
 'samaBinI':'sam+aBi+nI',  #
 'samaBisaMDe':'sam+aBi+sam+De',  #
 'samavaSiz':'sam+ava+Siz',  #
 'samavasad':'sam+ava+sad',  #
 'samavAkf':'sam+ava+A+kf',  #
 'samAkruS':'sam+A+kruS',  #
 'samAgal':'sam+A+gal',  #
 'samADU':'sam+A+DU',  #
 'samAyat':'sam+A+yat',  #
 'samutkf':'sam+ut+kf',  #
 'samupavfMh':'sam+upa+vfMh',  #
 'samupAkram':'sam+upa+A+kram',  #
 'samfYj':'sam+fYj',  #
 'sampariBf':'sam+pari+Bf',  #
 'samprakIrt':'sam+pra+kIrt',  #
 'sampratyAcakz':'sam+prati+A+cakz',  #
 'sampraDyE':'sam+pra+DyE',  #
 'sampranft':'sam+pra+nft',  #
 'sampravyaT':'sam+pra+vyaT',  #
 'samprasu':'sam+pra+su',  #
 'samBarts':'sam+Barts',  #
 'sammah':'sam+mah',  #
 'saMlip':'sam+lip',  #
 'saMBaj':'sam+Baj',  #
 'saMvfh':'sam+vfh',  #
 'saMvyavaso':'sam+vi+ava+so',  #
 'saMSi':'sam+Si',  #
 'saMSvi':'sam+Svi',  #
 #'svarya':'svarya',  #
 # examples where mwverbs1 has multiple choices. We force usage of 
 # the one corresponding to bur.txt
 'aBinayAmi':'aBi+nI',
 'AvayAmi':'A+u',  # questionable 
 'ujjihe':'ud+hA',
 'udDarAmi':'ud+hf',
 'upanayAmi':'upa+nI',
 'upAse':'upa+As',
 'samudDarAmi':'sam+ud+hf',
 'pratIl':'prati+Il', #?
 'vyud':'vi+und',  # mw has both ud/und.  bur only und.
 'pradIvyAmi':'pra+div',  # 
 'prativyUhAmi':'prati+vi+Uh',
 'vizkaBnomi':'vi+skaB',  # mw has both skaB, skamB
}
class Burmap(object):
 def __init__(self,out):
  self.out = out
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',out)
  self.L,self.k1,self.k2,self.code,self.mwfield = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  parts = self.mwfield.split(',')
  self.mwhw = parts[0]
  if len(parts) == 1:
   self.mwcat = 'verb'
  else:
   self.mwcat = parts[1]
  #if self.L in ['1087','2442','2799','2986','3138','3307','17851']:
  #  print('Burmap chk: %s, %s, parts="%s"'%(self.L,self.k1,parts))
  if len(parts) == 3:
   self.mwparse = parts[2]
   #if self.L in ['1087','2442','2799','2986','3138','3307','17851']:
   # print('Burmap chk 2: %s, %s, mwparse="%s"'%(self.L,self.k1,self.mwparse))
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

def init_burmapobj(recs):
 recs1 = []
 for rec in recs:
  line = rec.line
  # add mw 
  mwrec = rec.mwrec
  if mwrec == None:
   extra = rec.mw
   if not rec.mw.startswith('?'):
    # sometimes, rec.mw is a guess, but not a verb in mw.
    # make these cases easy to identify
    if rec.mw in bur_preverb_parses:
     parse = bur_preverb_parses[rec.mw]
     extra = '%s,preverb,%s' %(rec.mw,parse)
    else:
     extra = '%s,verb'%rec.mw
    extra = '?'+extra
   out = '%s, mw=%s'%(line,extra)
  elif mwrec.cat == 'verb':
   out = '%s, mw=%s,%s' %(line,rec.mw,mwrec.cat)
  elif mwrec.cat == 'preverb':
   if rec.k1 in bur_preverb_parses:
    # for some cases where there are multiple parses
    # the bur_preverb_parses value is the one to use.
    # example aBinayAmi => aBinI can be parsed as aBi+nI or aBi+ni+i
    #           but aBi+nI is the one we want.
    parse = bur_preverb_parses[rec.k1]
   else:
    parse = mwrec.parse
   out = '%s, mw=%s,%s,%s' %(line,rec.mw,mwrec.cat,parse)
  else:
   print('init_burmapobj. mwrec=%s',mwrec.line)
   exit(1)
  recs1.append(Burmap(out))
 return recs1

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 nprob = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs1:
   n = n + 1
   outrec = rec.transcode(tranin,tranout)
   out = ';; Case %04d: %s' %(n,outrec)
   f.write(out+'\n')
   continue
   line = rec.line
   # add mw 
   mwrec = rec.mwrec
   if mwrec == None:
    extra = rec.mw
    if not rec.mw.startswith('?'):
     # sometimes, rec.mw is a guess, but not a verb in mw.
     # make these cases easy to identify
     if rec.mw in bur_preverb_parses:
      parse = bur_preverb_parses[rec.mw]
      extra = '%s,preverb,%s' %(rec.mw,parse)
     else:
      extra = '%s,verb'%rec.mw
     extra = '?'+extra
    out = '%s, mw=%s'%(line,extra)
   elif mwrec.cat == 'verb':
    out = '%s, mw=%s,%s' %(line,rec.mw,mwrec.cat)
   elif mwrec.cat == 'preverb':
    out = '%s, mw=%s,%s,%s' %(line,rec.mw,mwrec.cat,mwrec.parse)
   else:
    print('write: Error 1. mwrec=%s',mwrec.line)
    exit(1)
   f.write(out + '\n')
   if rec.mw.startswith('?'):
    nprob = nprob + 1
 print(n,"records written to",fileout)
 print(nprob,"verbs still not mapped to mw")


def unused_write_log(fileout,cforms,mwverbsd):
 with codecs.open(fileout,"w","utf-8") as f:
  n1 = 0
  n2 = 0
  for cform in cforms:
   if cform.cat == 'P': # just prefix
    if cform.used:
     n1 = n1 + 1
     used = 'used'
    else:
     n2 = n2 + 1
     used = 'unused'
    if cform.k1 in mwverbsd:
     mwflag = 'mw=yes'
    else:
     mwflag = 'mw=no'
    out = '%s %s %s %s %s' %(cform.k1,cform.form,cform.parse,used,mwflag)
    f.write(out + '\n')
 print('%s cforms used, %s cforms unused' %(n1,n2))

if __name__=="__main__": 
 tranout = sys.argv[1]
 filein = sys.argv[2] #  bur_verb_filter.txt
 filein2 = sys.argv[3] # mwverbs1
 filein3 = sys.argv[4] # bur.txt
 filein4 = sys.argv[5] # extract1s
 fileout = sys.argv[6]
 #fileout1 = sys.argv[7] # log file
 recs = init_burverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein2)
 entries = init_entries(filein3)
 entry_Ldict = Entry.Ldict
 cformsd,cforms = init_cforms(filein4)
 burmap(recs,mwverbsd,entry_Ldict,mwverbrecs,cformsd)
 recs1 = init_burmapobj(recs)
 write(fileout,recs1,tranout)
 #write_log(fileout1,cforms,mwverbsd)
