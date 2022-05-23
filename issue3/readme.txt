Miscellaneous corrections.

temp_bur_0.txt   latest from csl-orig:
cp /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt temp_bur_0.txt

Andhrabharati's correction suggestion file.
abdata.txt == BUR.corrections.txt copied from link at
https://github.com/sanskrit-lexicon/csl-devanagari/issues/37#issuecomment-1030889680

temp_bur_1.txt  manual corrections

python prep1.py temp_bur_0.txt change_1.txt
python updateByLine.py temp_bur_0.txt change_1.txt temp_bur_1.txt

94 changes áº¡, áº  to <ab>a2.</ab> or <ab>A2.</ab>
1  A'ler -> Aller (k1 = stfkz)
22 (s) -> s:   Some of these are odd, and would be visarga e.g. duskham
1  8c -> 8e  (8th)


Add 'A2.' to burab_input.txt in csl-pywork.

python prep2.py temp_bur_1.txt prep2.txt
21 instances of regex= [0-9]o
309 instances of regex= [0-9]e
21 instances of regex= 1re
30 instances of regex= 1er
2 instances of regex= 2d
128 instances of regex= ae
9 instances of regex= AE


==============================================================

install into csl-orig and check validity
cp temp_bur_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur   
 # ok  commited changes to csl-orig. 05-10-2022.

==============================================================
change_1a:  (s) -> ḥ
Andhrabharati points out there is a typographical distinction
between a 'broken-s' (visarga) and a normal s in Burnouf
(Ref: https://github.com/sanskrit-lexicon/BUR/issues/3#issuecomment-1122711774)
I presume that all the '(s) -> s' changes of change_1 need to
be corrected.
That's what change_1a does.
python prep1a.py temp_bur_1.txt change_1a.txt
==============================================================
python updateByLine.py temp_bur_1.txt change_1a.txt temp_bur_1a.txt
cp temp_bur_1a.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur   
 # ok  commited changes to csl-orig. 05-10-2022.

cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3
==============================================================
temp_bur_2.txt  manual changes to temp_bur_1a.txt
Corrections (s to visarga)
Based on temp_bur.AB.ver.-v3.txt, downloaded from link at
https://github.com/sanskrit-lexicon/BUR/issues/3#issuecomment-1123358584


python diff_to_changes.py temp_bur.AB.ver.-v2.txt temp_bur.AB.ver.-v3.txt temp_change_bur.AB_2_3.txt
55 changes written to temp_change_bur.AB_2_3.txt

temp_bur_2.txt starts out with
  52 matches in 50 lines for "ḥ" in buffer: temp_bur_2.txt
temp_bur.AB.ver.-v3.txt has
  112 matches in 97 lines for "ḥ" in buffer: temp_bur.AB.ver.-v3.txt

So expect about 60 changes to temp_bur_2.txt in about 50 lines.

python diff_to_changes.py temp_bur_1a.txt temp_bur_2.txt change_2.txt
 59 changes

python diff_to_changes.py temp_bur.AB.ver.-v3.txt temp_bur.AB.ver.-v3_edit.txt change_bur.Ab.ver.-v3.txt
4 changes written to change_bur.Ab.ver.-v3.txt

==============================================================
==============================================================

install into csl-orig and check validity
cp temp_bur_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur
# push csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig/v02
# update cologne server
 # ok  commited changes to csl-orig. 05-10-2022.
# return home
cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3
================================================
push this issue3 repository
cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3
================================================
corrections based on abdata.txt and odile.txt input
# make all the changes.
Some of the 'æ' changes will be manually revised
python prep3.py temp_bur_2.txt change_3.txt
 21 changes of section type 1
282 changes of section type 2
 21 changes of section type 3
 30 changes of section type 4
  2 changes of section type 5
  0 changes of section type 6
137 changes of section type 7
479 changes written to change_3.txt
python updateByLine.py temp_bur_2.txt change_3.txt temp_bur_3.txt
=================================================================
temp_bur_4.txt manual adjustments, from Odile and Andhrabarati (duska)
All ae changed except for
-'kaer' (under cāru);
-'Naerrita' under brahma;   CHANGED per text 
-'Gaerî' under 'vṛṣākapi' which is a misprint (of the book) for 'Gaorî' (which i suggest to replace here by 'Gaorî (gaurī)' (as in French 'au' is equivalent to 'o', and it is not at all a diphtongue, that is why the author did use 'ao' for 'au' in the dict. )    PRINT CHANGE
- zaez (under śaśa) (non latine word)
Second list, DO NOT CHANGE:
-the ae of ajwaen, 'aeva' (not latine)
under 9 eva (aeva)
Third list, DO NOT CHANGE:
- 3 dipsāmi (lae), 'lae' which is a misprint for 'le' and should be corrected; 
 - 4 dhava (dae), 'dae' which is a non latine word
Under triṃśat note the misprint 'nymphaea blance' for 'nymphaea blanc'.

And these two changes from AB: dusk -> duḥkh
Trouver, rencontrer, {%sukhaṃ duskaṃ vā%} le plaisir ou la douleur;
{%smariṣyati kaucalyāṃ suduskitām%} il ne se souviendra pas que

----------------------------
python diff_to_changes.py temp_bur_3.txt temp_bur_4.txt change_4.txt
10 changes written to change_4.txt

=================================================================
install into csl-orig and check validity
cp temp_bur_4.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur
# push csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig/v02
# update cologne server
 # ok  commited changes to csl-orig. 05-10-2022.
# return home
cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3

=================================================================
temp_bur_5.txt  additional ab markup
Sources:
 temp_bur.AB.ver.-v3_edit.txt
 odile1.txt

Compare abbreviation frequency counts in bur.txt and AB.ver.v3
v3_edit1: modify v3_edit for digentry to work. 
python prep5.py temp_bur_4.txt temp_bur.AB.ver.-v3_edit1.txt prep5_bur4.txt
135480 lines read from temp_bur_4.txt
19775 entries found
89372 lines read from temp_bur.AB.ver.-v3_edit1.txt
19775 entries found
# abbrev codes = 155, Total abbrevs = 62843
# abbrev codes = 294, Total abbrevs = 65425
298 keys
298 abbreviations written to prep5_bur4.txt
64 abbreviations occur same number of times
234 abbreviations occur different number of times


=================================================================
cp temp_bur_4.txt temp_bur_5.txt
Make changes  in temp_bur_5, one abbreviation at a time
edit2 version. Some additions indicuated in [[x]]
python prep5a.py '1p.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt
python prep5a.py '2p.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt
python prep5a.py '3p.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt
python prep5a.py 'a.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt
python prep5a.py 'a1.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt
python prep5a.py 'A2.' temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt unused.txt



python prep5.py temp_bur_5.txt temp_bur.AB.ver.-v3_edit2.txt prep5_bur5.txt

===========================================================================
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/bur/pywork/burab/burab_input.txt temp_burab_input_0.txt
vêdiq. védique

from odile:
gramm.  grammairiens

tg. terme grammatical
gram. grammaire
L=13918 gr. in raktikA  -> <ab n="gramme(s)">gr.</ab>  (unit of mass)
L=11058, 13221, 13320  <ab n="gramme(s)">gram.</ab> 

(1/8) -> 1/8  (similarly remove parens for 8 other fractions)
==============================================================

install into csl-orig and check validity
cp temp_bur_5.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur   
 # ok  commited changes to csl-orig. 05-10-2022.
cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3
==============================================================
python diff_to_changes.py temp_bur_4.txt temp_bur_5.txt change_5.txt
2777 changes written to change_5.txt

python diff_to_changes.py temp_bur.AB.ver.-v3_edit1.txt temp_bur.AB.ver.-v3_edit2.txt change_v3_edit1_edit2.txt
100 changes written to change_v3_edit1_edit2.txt
 Note especially the [[]]  (23 cases).  These had missing text. There
 may be other similar cases, not yet detected.
==============================================================
install to csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/
Then install to cologne server.

cd /c/xampp/htdocs/sanskrit-lexicon/bur/issue3

==============================================================
push this BUR repository
==============================================================
prepare for tooltips.
python prep_burab.py temp_burab_input_0.txt prep5_bur5.txt prep_burab.txt
 
output is a form similar to burab_input, with adaptations for
filling in the unknown tooltips.

temp_bur_6.txt some adjustments
<ab>vêdiq.</ab> -> <ab>védiq.</ab>
python prep_burab.py temp_burab_input_0.txt prep5_bur5.txt prep_burab.txt

cp temp_burab_input_0.txt temp_burab_input_1.txt

temp_burab_input_1.txt
 The following removed from temp_burab_input_1
A2 <id>A2</id> <disp>aoriste 2nd</disp> NOTE: All are now 'A2.' (with period)
c.-à-d. <id>c.-à-d.</id> <disp>c’est-à-dire</disp> NOTE: All are now 'c-à-d.'
cond. <id>cond.</id> <disp>conditionnel</disp>
gal. <id>gal.</id> <disp>gaëlique</disp>
m. à m. <id>m. à m.</id> <disp>mot à mot</disp> NOTE: All are now 'm à m.'
 
neg. <id>neg.</id> <disp>negatif</disp>: NOTE: Now  <id>nég.</id> <disp>négatif</disp>
pron. <id>pron.</id> <disp>pronom</disp>
ppt. <id>ppt.</id> <disp>proprement</disp>
s-ent. <id>s-ent.</id> <disp>sous-entendu</disp>
subj. <id>subj.</id> <disp>subjonctif</disp>
-----------------------------------
UNRESOLVED: Ep.and 'Ép.' 
Ép. <id>Ép.</id> <disp>épithète</disp>
  Ép. does not currently appear in bur.txt
Add 'Ep. <id>Ep.</id> <disp></disp>' to burab.
  There are 16 'Ep.' (no accent).  Should these be 'Ép.'?


python prep5.py temp_bur_6.txt temp_bur.AB.ver.-v3_edit3.txt prep5_bur6.txt

with preliminary changes, rerun
python prep_burab.py temp_burab_input_1.txt prep5_bur6.txt prep_burab.txt
check1 warning: Ép. <id>Ép.</id> <disp>épithète</disp>
check1 identifies 1 problems

python prep_burab_examples.py prep_burab.txt temp_bur_6.txt prep_burab_examples.txt
