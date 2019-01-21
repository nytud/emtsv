
# raw text input
RAWINPUT=test_input/input.test
#RAWINPUT=test_input/puzser.test
#
# some larger raw testfiles available on juniper...
#RAWINPUT=/store/projects/e-magyar/test_input/hundredthousandwords.txt

# input crafted directly for emTag
#TAGINPUT=test_input/emTag.test

# input crafted directly for emDep
#DEPINPUT=test_input/emDep.test

# ----------

all: usage

# always update according to targets below :)
usage:
	@echo
	@echo "You can..."
	@echo " make test-tok-morph"
	@echo " make test-tok-morph-tag"
	@echo " make test-tok-morph-tag-single"
#	@echo " make test-tok-morph-tag-chunk"
#	@echo " make test-tok-morph-tag-chunk-single"
#	@echo " make test-tok-morph-tag-deptool"
#	@echo " make test-tok-morph-tag-deptool-single"
#	@echo " make test-tag"
#	@echo " make test-dep"
	@echo

# ----------

# testing emMorph only
test-tok-morph:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok \
     | python3 ./emtsv.py morph

# testing emMorph + emTag
test-tok-morph-tag:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok \
     | python3 ./emtsv.py morph \
     | python3 ./emtsv.py pos

# testing emMorph + emTag
# single python interpreter (single threaded)
test-tok-morph-tag-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos

# testing emMorph + emTag + em_morph2UD + emDepUD
# single python interpreter (single threaded)
test-tok-dep-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos,conv-morph,dep

# testing emMorph + emTag + em_morph2UD + emDepUD + emCons
# single python interpreter (single threaded)
test-tok-cons-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos,conv-morph,dep,cons

# ----------

# testing emMorph + emTag + emChunk -- ezt majd!
#test-tok-morph-tag-chunk:
#	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
#     | ./trivSentSplit.sh \
#     | python3 ./emtsv.py morph \
#     | python3 ./emtsv.py pos \
#     | python3 ./emtsv.py chunk

# testing emMorph + emTag + emChunk single pyhton interpreter (single threaded) -- ezt majd!
#test-tok-morph-tag-chunk-single:
#	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
#     | ./trivSentSplit.sh \
#     | python3 ./emtsv.py morph,pos,chunk

# XXX ugyanez kell deptool-ra majd
# XXX ugyanez kell emdep-re majd
# XXX ugyanez kell emcons-ra majd
# XXX ... meg a teljes eszközláncra! :)

# ----------

# testing emTag only -- ezt majd!
#test-tag:
#	@cat $(TAGINPUT) \
#    | python3 ./emtsv.py pos

#	testing emDep only -- ezt majd!
#test-dep:
#	@cat $(DEPINPUT) \
#    | python3 ./emtsv.py dep

