
# raw text input
RAWINPUT=test_input/input.test
#RAWINPUT=test_input/puzser.test

# tokenized input (no sentence-split, for emMorph)
TOKENIZEDINPUT=test_input/input.tok.test
#TOKENIZEDINPUT=test_input/puzser.tok.test
#
# some larger pre-tokenized testfiles available on juniper...
#TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_100e.tok.test
#TOKENIZEDINPUT=/store/projects/e-magyar/test_input/mnsz2_radio_1mio.tok.test

# input crafted directly for emTag
TAGINPUT=test_input/emTag.test

# input crafted directly for emDep
DEPINPUT=test_input/emDep.test

# ----------

all: usage

# always update according to targets below :)
usage:
	@echo
	@echo "You can..."
	@echo " make install :)"
	@echo " make test-morph"
	@echo " make test-morph-tag"
	@echo " make test-morph-tag-single"
#	@echo " make test-morph-tag-chunk"
#	@echo " make test-morph-tag-chunk-single"
	@echo " make test-tokenizedinput-morph-tag"
	@echo " make test-tokenizedinput-morph-tag-single"
#	@echo " make test-tokenizedinput-morph-tag-deptool"
#	@echo " make test-tokenizedinput-morph-tag-deptool-single"
#	@echo " make test-tag"
#	@echo " make test-dep"
	@echo

# ----------

install:
	@git clone --recurse-submodules https://github.com/dlazesz/emTSV

# ----------

# testing emMorph only
test-morph:
	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
     | ./trivSentSplit.sh \
     | python3 ./emTSV20.py morph

# testing emMorph + emTag
test-morph-tag:
	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
     | ./trivSentSplit.sh \
     | python3 ./emTSV20.py morph \
     | python3 ./emTSV20.py pos

# testing emMorph + emTag single pyhton interpreter (single threaded)
test-morph-tag-single:
	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
     | ./trivSentSplit.sh \
     | python3 ./emTSV20.py morph,pos

# testing emMorph + emTag + emChunk -- ezt majd!
#test-morph-tag-chunk:
#	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
#     | ./trivSentSplit.sh \
#     | python3 ./emTSV20.py morph \
#     | python3 ./emTSV20.py pos \
#     | python3 ./emTSV20.py chunk

# testing emMorph + emTag + emChunk single pyhton interpreter (single threaded) -- ezt majd!
#test-morph-tag-chunk-single:
#	@( echo "string" ; cat $(RAWINPUT) | ./trivToken.sh ) \
#     | ./trivSentSplit.sh \
#     | python3 ./emTSV20.py morph,pos,chunk

# ----------

# testing emMorph + emTag on pre-tokenized input XXX??? -- még 1x tesztelni a végén az 1mio-ra/100e-re
# there are large MNSZ2 files available for testing locally...
#
#  * header needed = 'echo "string"' the the beginning
#  * empty line at the end needed = 'echo' at the end
#    (It is needed only because it is not guaranteed
#     that the input files always end with a sentence-end-mark
#     which then translated to an empty line by trivSentSplit.sh.
#     If they still do, we will get a WARNING "only one blank line allowed".)
#  * space in token (e.g. "január 16-án") is forbidden = tr ' ' '\n'
#
# XXX TODO tokenizing can be refactored into a separate Makefile target
#          compare: 'test-morph-tag' and 'test-tokenizedinput-morph-tag'
#
test-tokenizedinput-morph-tag:
	@( echo "string" ; cat $(TOKENIZEDINPUT) ; echo ) | tr ' ' '\n' \
     | ./trivSentSplit.sh \
     | python3 ./emTSV20.py morph \
     | python3 ./emTSV20.py pos

test-tokenizedinput-morph-tag-single:
	@( echo "string" ; cat $(TOKENIZEDINPUT) ; echo ) | tr ' ' '\n' \
     | ./trivSentSplit.sh \
     | python3 ./emTSV20.py morph,pos

# testing emMorph + emTag + depTool -- ezt majd!
#test-tokenizedinput-morph-tag-deptool:
#	@( echo "string" ; cat $(TOKENIZEDINPUT) ; echo ) | tr ' ' '\n' \
#     | ./trivSentSplit.sh \
#     | python3 ./emTSV20.py morph \
#     | python3 ./emTSV20.py pos \
#     | python3 ./emTSV20.py deptool

# testing emMorph + emTag + depTool single pyhton interpreter (single threaded) -- ezt majd!
#test-tokenizedinput-morph-tag-deptool-single:
#	@( echo "string" ; cat $(TOKENIZEDINPUT) ; echo ) | tr ' ' '\n' \
#     | ./trivSentSplit.sh \
#     | python3 ./emTSV20.py morph,pos,deptool

# ----------

# testing emTag only -- ezt majd!
#test-tag:
#	@cat $(TAGINPUT) \
#    | python3 ./emTSV20.py pos

#	testing emDep only -- ezt majd!
#test-dep:
#	@cat $(DEPINPUT) \
#    | python3 ./emTSV20.py dep

