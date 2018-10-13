
all: usage

usage:
	@echo
	@echo "You can..."
	@echo " make install :)"
	@echo " make test-chunk-chain"
	@echo " make test-tag-only"
	@echo " make test-dep-only"
	@echo

install:
	git clone --recurse-submodules https://github.com/dlazesz/emTSV

# testing emMorph + emTag + emChunk
test-chunk-chain:
	cat test_input/input.test | sed "s/\([.,;:?!]\)/ \1/" | tr ' ' '\n' | python3 ./emMorphREST.py --pipe
#	cat test_input/emTag.test | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe | python3 ./emChunkREST.py --pipe

# testing emTag only
test-tag-only:
	cat test_input/emTag.test | python3 ./emTagREST.py --pipe

#	testing emDep only
test-dep-only:
	cat test_input/emDep.test | python3 ./emDepREST.py --pipe

