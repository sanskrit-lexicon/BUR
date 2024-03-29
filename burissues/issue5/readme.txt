work on issue5 for BUR dictionary.  
objective: install corrections from odile.
03-27-2024
 Ref: https://github.com/sanskrit-lexicon/BUR/issues/5"

# directory of this file
cd /c/xampp/htdocs/sanskrit-lexicon/bur/burissues/issue5

# temp_bur_0.txt
cp /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt temp_bur_0.txt
# temp_bur_1.txt  a second copy 
cp temp_bur_0.txt temp_bur_1.txt

The corrections suggested by Odile also will require changes to csl-pywork
repository, namely file
csl-pywork/v02/distinctfiles/bur/pywork/burab/burab_input.txt

 
# *************************************************************************
# Make corrections to temp_bur_1.txt
# *************************************************************************
This is the main task.
-------------------------------
part. abbreviation
Odile:
It is about "part."‌.
As an abbreviation, it abbreviates "particule";
but this appears only twice in the dictionary (at "u" and "cit");
whereas the word "part" appears at the end of several sentences (14).
And there, it is underlined et refers to "particule"; [Jim Eng. particle]
this reference being wrong,  [Jim : Here 'part.' stands for 'participe' ]
it would be good to just take
this reference "part." out and write in whole the word "particule"
at the two above mentioned occurrences (under "u" and "cit") .

Jim:
 Use the 'local abbreviation' technique for the two instances at 'u' and 'cit'
 changes to bur.txt
--- u
OLD: {#u#}¦ {%u,%} <ab>part.</ab> enclitique
NEW: {#u#}¦ {%u,%} <ab n="particule">part.</ab> enclitique 
--- cit
OLD: {#cit#}¦ {%cit,%} <ab>part.</ab> enclitique
NEW: {#cit#}¦ {%cit,%} <ab n="particule">part.</ab> enclitique

What do the other instances of '<ab>part.</ab>' refer to?
According to Windows 11 copilot:
question: is 'part' a french word?
answer: Yes.  some English meanings: section, portion, share

burab_input.txt :
Remove the tooltip for 'part.'
part.	<id>part.</id> <disp>particule</disp>


Odile:
Note that there is one occurrence, under verb "kr", which is "Part."
 in bold character, and which refers in fact to "participe";
 if you can, as it is bold (and in capital), you could make the reference for it.

One instance of <ab>Part.</ab> under 'kf' Here it means 'participe' (participle)
OLD:
<ab>Part.</ab>
NEW:
<ab n="Participe">Part.</ab>

=================================================================
odile:
I also noticed that the abbreviation "qq." is referring to "quelques"
whereas it should refer to "quelque(s)".
Jim:
I think 'quelque' is singular and 'quelques' is plural.
<ab>qq.</ab> occurs 29 times.
Change burab_input.txt:
OLD:
qq.	<id>qq.</id> <disp>quelques</disp>
NEW:
qq.	<id>qq.</id> <disp>quelque(s)</disp>

=================================================================
odile:
At the same verb "kR", there is also a "P." in bold character underlined
 but not referenced;
 it is here for "parfait" (perfect) (like the other abbreviations for "p." with small p which are properly referenced. But the occurences with capital P aren't referenced and should be referenced (and there are a good number).

Jim: I find 6 instances of '<ab>P.</ab>', and 1110 instances of <ab>p.</ab>
burab_input.txt
p.	<id>p.</id> <disp>parfait</disp>   NO CHANGE
New line:
P.	<id>P.</id> <disp>Parfait</disp>

=================================================================
odile:
Also non referenced "aor." refers to "aoriste" (I see 4 occurrences)

Jim:
<ab>aor.</ab> 2 instances
<ab>Aor.</ab> 2 instances
Additions to burab_input.txt:
aor.	<id>aor.</id> <disp>aoriste</disp>
Aor.	<id>Aor.</id> <disp>aoriste</disp>

=================================================================
odile: there is also ...
---
the reference "1p.",
 proper reference is "1re personne", not "1er personne"
   (1er is used when the substantive is masculine,
    here "personne" is feminine))
Jim:
<ab>1p.</ab> 50 instances
change burab_input.txt
OLD:
1p.	<id>1p.</id> <disp>1er personne</disp>
NEW:
1p.	<id>1p.</id> <disp>1re personne</disp>

=================================================================
odile:
"2p.", proper reference is "2e personne", that is, the etc. and the comma should be taken out; same for the "3p." the proper reference is "3e personne" (that ", etc." was there when there was only one reference for the 3 cases, so now, one doesn't need it anymore).

Jim:
change burab_input.txt:
OLD:
2p.	<id>2p.</id> <disp>2e personne, etc</disp>
3p.	<id>3p.</id> <disp>3e personne, etc</disp>
NEW:
2p.	<id>2p.</id> <disp>2e personne</disp>
3p.	<id>3p.</id> <disp>3e personne</disp>

=================================================================
odile:
Also "Imp." with capital letter is not referenced and should be "impératif".
Same for "Ind." (indicatif)

Jim:
<ab>Imp.</ab> 6 instances
<ab>Ind.</ab> 1 instance

Add two new lines to burab_input.txt
=================================================================
odile:
the reference for "pr." is "Présent", it should be "présent".
  For "Pr." it can still be "présent" (or "Présent").
Jim:
Change burab_input.txt
OLD:
pr.	<id>pr.</id> <disp>Présent</disp>
NEW:
pr.	<id>pr.</id> <disp>présent</disp>


=================================================================
odile:
Still under kR:
Aor. conj. sg. 3p. karat, karati ou karate; pl. 1p. karāma;
  du. 2p. karatam et kṛthas, 3ᵉ p. karatām.

here "3ᵉ p." should be written "3p."; 

Jim:
The print has '3ᵉ p.'
There are 4 instances of '3ᵉ <ab>p.</ab>' in bur.txt.
In these, <ab>p.</ab> refers to 'personne', not 'parfait' !
Solution:
 Change '<ab>p.</ab>' to '<ab n="personne">p.</ab>'  in these 4 cases

=================================================================
odile:
Still under kR:
and "conj." "conjf."

<ab>conj.</ab> 12 times
<ab>conjf.</ab> 1 times
conj.	<id>conj.</id> <disp>conjonction</disp>
conjf.	<id>conjf.</id> <disp>conjonctif</disp>

Jim:
under kR,  Print has 'conj.' (under 'Aor. conj.')
This should be 'conjonctif'
Solution:
change temp_bur_1.txt
OLD:
<ab>Aor.</ab> <ab>conj.</ab>
NEW:
<ab>Aor.</ab> <ab>conjf.</ab>
<L>4984<pc>179,1<k1>kf<k2>*kf
DONE csl-corrections notes print change 

# *************************************************************************
  Additional work for consistency between <ab> markup of bur.txt and
  tooltips in burab_input
# *************************************************************************
--------------------------------------------------

burab_input.txt missed tooltips for Ind. and Imp. (Capital letter I)
Get temporary version of burab_input.txt
cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/bur/pywork/burab/burab_input.txt burab_input_0.txt

At this point, we 'freeze' temp_buf_1.txt and generate a change file

python diff_to_changes_dict.py temp_bur_0.txt temp_bur_1.txt change_bur_0_1.txt
22 changes written to change_bur_0_1.txt


Generate more information about discrepancies between
<ab>X</ab> instances in bur.txt and tooltips in burab_input.txt

python cap_ab.py temp_bur_1.txt burab_input_0.txt cap_ab.txt

135479 from temp_bur_1.txt
172 from burab_input_0.txt
123 abbrevs without tooltip
25 abbrevs with ADDED lower-case version
98 abbrevs tooltips TODO
295 lines written to cap_ab.txt

--------------------------------------------------
burab_input_1.txt
For the 25 cases (see the 'ADDED' lines of cap_ab.txt),
generate tooltips: e.g. tooltip for 'Adv.' is 'adverbe', which we
have as the tooltip for 'adv.'.

python make_burab_1.py cap_ab.txt burab_input_1.txt

--------------------------------------------------
burab_input_2.txt
 See if abbreviations of stc (Stchoupak dictionary) help.

cp /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/stc/pywork/stcab/stcab_input.txt stcab_input_0.txt

python make_burab_2.py cap_ab.txt stcab_input_0.txt burab_input_2.txt 
295 from cap_ab.txt
103 from stcab_input_0.txt
11 abbreviations found in Stchoupak
87 remaining Burnouf abbreviations without tooltip
295 lines written to burab_input_2.txt

We still need tooltips for those 87;
These 87 are the ' TODO ' lines of burab_input_2.txt

We need a display to provide context.
python display_todo.py temp_bur_1.txt burab_input_2.txt display_todo_1.txt
135479 lines read from temp_bur_1.txt
19775 entries found
295 from burab_input_2.txt
87 records written to display_todo_1.txt

--------------------------------------------------
# For further work, we use bur_2
cp temp_bur_1.txt temp_bur_2.txt
cp burab_input_2.txt burab_input_3.txt
#
changes:
--- den
temp_bur_2.txt
OLD:
<ab>den.</ab>
NEW:
<ab>dén.</ab>

25 instances

There is already a tooltip for '
burab_input_3.txt
OLD:
den.	<id>den.</id> <disp>NEW</disp> TODO <count>25</count>
  Old line deleted
NEW: revise
dén.	<id>dén.</id> <disp>dénominatif</disp> TODO DONE <count>101</count>

python display_todo.py temp_bur_2.txt burab_input_3.txt display_todo_2.org

many additional changes made to burab_input_3.txt
After these, all the 294 abbreviations have a tooltip.

**************************************
installation steps
**************************************
----------
burab_input_4.txt  version to install, contains counts.
python display_final.py temp_bur_2.txt burab_input_3.txt burab_input_4.txt
135479 lines read from temp_bur_2.txt
19775 entries found
294 from burab_input_3.txt
9 unused tips removed
A2      <id>A2</id> <disp>aoriste 2nd</disp>
c.-à-d. <id>c.-à-d.</id> <disp>c’est-à-dire</disp>
cond.   <id>cond.</id> <disp>conditionnel</disp>
gal.    <id>gal.</id> <disp>gaëlique</disp>
m. à m. <id>m. à m.</id> <disp>mot à mot</disp>
ppt.    <id>ppt.</id> <disp>proprement</disp>
pron.   <id>pron.</id> <disp>pronom</disp>
s-ent.  <id>s-ent.</id> <disp>sous-entendu</disp>
subj.   <id>subj.</id> <disp>subjonctif</disp>
285 lines written to burab_input_4.txt
----------
change_1_2.txt

python diff_to_changes_dict.py temp_bur_1.txt temp_bur_2.txt change_bur_0_2.txt
25 changes written to change_bur_0_2.txt
----------

cp temp_bur_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt 

cp  burab_input_4.txt /c/xampp/htdocs/cologne/csl-pywork/v02/distinctfiles/bur/pywork/burab/burab_input.txt

-----------------
# check local installation of displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur
# ok

-----------------
# sync csl-pywork to Github

cd /c/xampp/htdocs/cologne/csl-pywork
git add .
git commit -m "Revise burab_input.txt.
Ref: https://github.com/sanskrit-lexicon/BUR/issues/5"

git commit -m "Revise burab_input.txt.
Ref: https://github.com/sanskrit-lexicon/BUR/issues/5"

git push
-----------------
# sync csl-orig to Github

cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "bur update related to <ab> markup;
Ref: https://github.com/sanskrit-lexicon/BUR/issues/5"

git push

-----------------
# update cologne server
pull csl-pywork and csl-orig
make bur displays in csl-pywork/v02
====================================================================
THE END
