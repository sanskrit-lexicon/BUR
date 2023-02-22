work on issue4 for BUR dictionary.  
objective: Proofread Greek text.

# *************************************************************************
# startup instructions (for Anna)
# *************************************************************************
# 1. local copy of BUR repository
# If necessary, make a 'sanskrit-lexicon' directory (such as in ~/Documents/)
# mkdir ~/Documents/sanskrit-lexicon
cd ~/Documents/sanskrit-lexicon
# clone the BUR directory from Github.
git clone https://github.com/sanskrit-lexicon/BUR.git
# this will create 'BUR' folder: ~/Documents/sanskrit-lexicon/BUR
---------
# 2. sync local copy of csl-orig repository
cd ~/Documents/cologne/csl-orig
git pull
--------
# 3. temp_bur_0.txt
cd ~/Documents/sanskrit-lexicon/bur/burissues/issue4
cp ~/Documents/cologne/csl-orig/v02/BUR/bur.txt temp_bur_0.txt
# 4. temp_bur_1.txt
# make a second copy in issue4
cp temp_bur_0.txt temp_bur_1.txt

# *************************************************************** **********
# Make corrections to temp_bur_1.txt
# *************************************************************************
This is the main task.
edit temp_bur_1.txt.
Greek text is identified by '<lang n="greek">X</lang>'.
There are 669 instances in 665 lines of temp_bur_1.txt.

For each such instance:
 a. compare temp_bur_1.txt to the scanned image of Burnouf dictionary.
 b. If necessary, make change to temp_bur_1.txt
    NOTE: Do not introduce new (extra) lines in temp_bur_1.txt,
          as this will cause problems in next step

# *************************************************************************
# make change_1.txt
# *************************************************************************
# The program diff_to_changes_dict.py compares each line of
# temp_bur_0.txt to the corresponding line of temp_bur_1.txt.
# If these lines are different (i.e., a change was made in temp_bur_1.txt),
# then the program writes a change transaction.
python diff_to_changes_dict.py temp_bur_0.txt temp_bur_1.txt change_1.txt

Notes:
1. You can remake change_1.txt at any time.
1a. diff_to_changes_dict.py assumes temp_bur_0.txt and temp_bur_1.txt
   have the same number of lines. That's why the 'no extra lines'
   comment above is important.
2. You can push this BUR repository at any temp
3. Jim will use own copy of temp_bur_0.txt and your pushed
   change_1.txt to recreate his copy of your temp_bur_1.txt.
   [See *install instructions* below for details.
4. The BUR/.gitignore file has 'temp*' line, which means
   git will not track files whose names start with 'temp'.
   Thus Anna's local temp_bur_1.txt is not directly available to Jim.
   But Jim can recreate a copy of Anna's temp_bur_1.txt from change_1.txt.


# *************************************************************************
# Installation (Jim)
# *************************************************************************
# Jim makes a local copy temp_bur_0.txt just as Anna did.
# Use updateByLine.py program to create temp_bur_1.txt
python updateByLine.py temp_bur_0.txt change_1.txt temp_bur_1.txt

# install into csl-orig
# a. copy to csl-orig
cp temp_bur_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt

# b. Recreate local displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'bur ' redo_xampp_all.sh
sh generate_dict.sh bur  ../../bur

# c. check xml validity of bur.xml
sh xmlchk_xampp.sh bur
# ok.  [If there are errors, they must be corrected]

## d. update csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .  # v02/bur/bur.txt
git commit -m "bur. Misc corrections.
 Ref: https://github.com/sanskrit-lexicon/BUR/issues/4"
git push
----------------------------------------------------
update at Cologne
cd ... csl-orig
git pull
cd ../csl-pywork/v02
grep 'bur ' redo_cologne_all.sh
sh generate_dict.sh bur  ../../BURScan/2020/
cd /c/xampp/htdocs/sanskrit-lexicon/BUR/burissues/issue4
----------------------------------------------------
