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
