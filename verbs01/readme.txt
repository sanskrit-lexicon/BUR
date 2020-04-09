
Analysis of bur verbs
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/bur/.

The shell script redo.sh reruns several python programs, from mwverb.py to verb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* bur_verb_filter.
bur has prefixed verbs as separate entries (like MW, in contrast to pwg, etc.).

python bur_verb_filter.py ../bur.txt bur_verb_exclude.txt bur_verb_include.txt bur_verb_filter.txt

bur_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  (74 cases)
bur_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns. (18 cases)


Patterns for roots:  
These patterns are mostly used to derive root codes, but there are 
many exceptions that are coded by various 'ad-hoc' lists within the
bur_verb_filter.py program.
 R   =  u'^{#[*]',   Un-prefixed roots.  Also, in metaline, '<k2>*'
 Des = u'¦.*<ab>dés.</ab>'   Desiderative
 Aug = u'¦.*<ab>aug.</ab>'   Intensive
 C   = u'¦.*<ab>c.</ab>'     Causal
 F   = u'¦.*<ab>f2[.]</ab>'  2nd future
 D = u'Ami#}¦' or u'omi#}' or u'e#}¦' or u'mi#}¦'
           1st singular forms.  The 'D' abbreviation means 'Derived',
           a catchall category.


Counts of total patterns:
0403 Aug
0451 C
2208 D
0423 Des
0057 F
2273 R

Total 5815 entries identified as verbs.

Format of file bur_verb_filter.txt by ecample:
;; Case 0001: L=4, k1=ak, k2=*ak, code=R
;; Case 0007: L=143, k1=aNgayAmi, k2=aNgayAmi, code=D
;; Case 0026: L=278, k1=atikupyAmi, k2=atikupyAmi, code=D


* bur_verb_filter_map
python bur_verb_filter_map.py slp1 bur_verb_filter.txt mwverbs1.txt ../bur.txt conjdata/extract2.txt bur_verb_filter_map.txt 

python bur_verb_filter_map.py deva bur_verb_filter.txt mwverbs1.txt ../bur.txt conjdata/extract2.txt bur_verb_filter_map_deva.txt 


Correspondences between bur verb spellings and
 - bur verb spellings
 - mw verb spellings

Uses some empirically derived rules, and some empirically derived mappings.
The conjdata/extract2.txt file contains previously computed 1st person
conjugated forms;  it was also used where possible to determine the root
corresponding to Burnouf entries. For example,
ativft ativarte P ati+vft    indicates that the 1st singular present
of prefixed verb ativft is ativarte, and that the parsed form is ati+vft.
This was used to derive the line of bur_verb_filter_map.txt :
;; Case 0038: L=314, k1=ativarte, k2=ativarte, code=D, mw=ativft,preverb,ati+vft

However, for various reasons, many (perhaps 1/3) of the
inflected form entries of BUR could not be mapped by this technique. 
To handle such cases, various lists of mappings were hard-coded into
bur_verb_filter_map.py.  

For example, the BUR headword 'BrAmayAmi' is not
found among the conjugated forms of conjdata/extract2.txt. But consultation
of MW for root 'Bram' shows 'BrAmayati' as a Causal form, which implies
'BrAmayAmi' as 1st singular present of Causal of root 'Bram'. This 
association appears in the 'map2mw_special_R' dictionary of the
bur_verb_filter_map.py, and leads to the line of bur_verb_filter_map.txt :
;; Case 3555: L=12876, k1=BrAmayAmi, k2=BrAmayAmi, code=R, mw=Bram,verb

There are 145 cases where the mapping from BRU entries to MWverbs
is known to be questionable; these are identified by a '?' as the first
character of the 'mw' field. For example:
;; Case 0215: L=1061, k1=aBigopayAmi, k2=aBigopayAmi, code=D, mw=?aBigup,preverb,aBi+gup

Here, as with 'BrAmayAmi', we can confirm from MW entry for 'gup'
that 'gopayAmi' is causal form of 'gup'; clearly then the prefixed verb would
be 'aBigup'.  However, MW does not have an entry for this particular 
prefixed verb (MW has upagup, nigup, nirgup, parigup, pragup, and vigup,
 but not aBigup).  So, another hard-coded mapping 'bur_preverb_parses' in 
the bur_verb_filter_map.py program provides the parsing 'aBigup':'aBi+gup'.
The question mark in 'mw=?aBigup,preverb,aBi+gup' then indicates that
that aBigup is not found in mw.



* bur_preverb1.txt and bur_preverb1_deva.txt
python preverb1.py slp1  bur_verb_filter_map.txt bur_preverb1.txt
python preverb1.py deva  bur_verb_filter_map.txt bur_preverb1_deva.txt

One prints Sanskrit text in SLP1, and the other prints Sanskrit text in
Devanagari.

The bur_preverb1 report is a reorganization of bur_verb_filter_map.
It groups the various entries related to a given MW verb entry.
For example, for the verb 'Bram':

; Verb 1017: Bram (1 uninflected, 4 inflected, 3 prefix entries)
  L=12860 k1=Bram       code=*R  mw=Bram,verb
  L=12416 k1=baBrAmi    code=R   mw=Bram,verb
  L=12423 k1=bamBramye  code=Aug mw=Bram,verb
  L=12535 k1=biBramizAmi code=Des mw=Bram,verb
  L=12876 k1=BrAmayAmi  code=R   mw=Bram,verb
  L=3002  k1=udBramAmi  code=D   mw=udBram,preverb,ud+Bram
  L=10652 k1=pariBramAmi code=D   mw=pariBram,preverb,pari+Bram
  L=15614 k1=viBramAmi  code=D   mw=viBram,preverb,vi+Bram

First appears the entry in Burnouf for the bare root 'Bram', as
indicated by the '*' (code=*r); this is the '1 uninflected' entry.
Next appear 4 entries whose headword is believed to be an inflected
form of the non-prefixed verb:
 baBrAmi, bamBramye, biBramizAmi, BrAmayAmi.
Finally appear 3 entries believed to be prefixed verb forms based on 'Bram':
udBramaAmi, pariBramAmi, viBramAmi.

