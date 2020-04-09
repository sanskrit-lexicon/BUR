
extract information for prefixed verbs from old conjugation tables.

normprev-conj-spcl.txt comes from data.zip in
 /c/ejf/pdfs/TM2013/0research/ejfcologne/vlgtab1/data
similarly for normroot-conj-spcl.txt

#python extract1s_preverb.py normprev-conj-spcl.txt extract1s_preverb.txt
python extract2_preverb.py normprev-conj-spcl.txt extract2_preverb.txt

#extraction for non-prefixed verbs
python extract1s_verb.py normroot-conj-spcl.txt extract1s_verb.txt

#cat extract1s_preverb.txt extract1s_verb.txt > extract1s.txt
#cat extract2_preverb.txt extract1s_verb.txt > extract2.txt


python conjugate_mwverb.py ../mwverbs1.txt extract1s_verb.txt extract2_preverb.txt conjugate_mwverb.txt


cat extract2_preverb.txt extract1s_verb.txt conjugate_mwverb.txt > extract2.txt
