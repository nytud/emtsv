
INPUT=test_input/input.test
TAGINPUT=test_input/emTag.test
DEPINPUT=test_input/emDep.test

all: usage

usage:
	@echo
	@echo "You can..."
	@echo " make install :)"
	@echo " make test-morph"
	@echo " make test-tag"
	@echo " make test-dep"
	@echo " make test-morph-tag"
	@echo " make test-morph-tag-chunk"
	@echo

install:
	@git clone --recurse-submodules https://github.com/dlazesz/emTSV

# testing emMorph only
test-morph:
	@( echo "string" ; cat $(INPUT) | ./trivToken.sh ) | python3 ./emMorphREST.py --pipe

# testing emTag only
test-tag:
	@cat $(TAGINPUT) | python3 ./emTagREST.py --pipe

#	testing emDep only
test-dep:
	@cat $(DEPINPUT) | python3 ./emDepREST.py --pipe

# testing emMorph + emTag
test-morph-tag:
	@( echo "string" ; cat $(INPUT) | ./trivToken.sh ) | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe

# testing emMorph + emTag + emChunk
test-morph-tag-chunk:
	@( echo "string" ; cat $(INPUT) | ./trivToken.sh ) | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe | python3 ./emChunkREST.py --pipe

