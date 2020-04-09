echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake bur_verb_filter.txt"
python bur_verb_filter.py ../bur.txt bur_verb_exclude.txt bur_verb_include.txt bur_verb_filter.txt
echo "remake bur_verb_filter_map.txt"
python bur_verb_filter_map.py slp1 bur_verb_filter.txt mwverbs1.txt ../bur.txt conjdata/extract2.txt bur_verb_filter_map.txt 
echo "remake bur_verb_filter_map_deva.txt"
python bur_verb_filter_map.py deva bur_verb_filter.txt mwverbs1.txt ../bur.txt conjdata/extract2.txt bur_verb_filter_map_deva.txt 


echo "bur_preverb1.txt"
python preverb1.py slp1  bur_verb_filter_map.txt bur_preverb1.txt
echo "bur_preverb1_deva.txt"
python preverb1.py deva  bur_verb_filter_map.txt bur_preverb1_deva.txt
