echo "extract2_preverb"
python extract2_preverb.py normprev-conj-spcl.txt extract2_preverb.txt
echo "extract1s_verb"
python extract1s_verb.py normroot-conj-spcl.txt extract1s_verb.txt
echo "conjugate_mwverb.txt"
python conjugate_mwverb.py ../mwverbs1.txt extract1s_verb.txt extract2_preverb.txt conjugate_mwverb.txt

echo "extract2.txt"
cat extract2_preverb.txt extract1s_verb.txt conjugate_mwverb.txt > extract2.txt
