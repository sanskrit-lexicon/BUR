Insertion of Greek text into bur.txt

temp_bur_0.txt   latest from csl-orig:
cp /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt temp_bur_0.txt

Andhrabharati's text
abdata.txt == Bur.greek.string.lines.csl-org.filled.txt
downloaded from link at
https://github.com/sanskrit-lexicon/csl-devanagari/issues/37#issuecomment-1030888655

editing of abdata.txt:
1. Add missing <L> numbers before several <P> elements.
2. supply greek δάϰυω <L>8539 <L>8539<pc>315,1<k1>daMS

python prep1.py temp_bur_0.txt abdata.txt change_1.txt

135480 lines read from temp_bur_0.txt
19775 entries found
618 records from abdata.txt
618 Change records generated
0 Change problems

python updateByLine.py temp_bur_0.txt change_1.txt temp_bur_1.txt

==============================================================

install into csl-orig and check validity
cp temp_bur_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur   
 # ok  READY TO UPLOAD.  CHANGE display of greek in BUR and BOP.

==============================================================
==============================================================
==============================================================
