#!/bin/bash

date

# --- ez miért nem jó? :)
( echo "string" ; cat test_input/mnsz2_radio_100e.tok.test ) | ./trivSentSplit.sh | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe > out

# --- hiszen az alábbi jó... ~ 'make test-morph-tag'
#( echo "string" ; cat test_input/puzser.test | ./trivToken.sh ) | ./trivSentSplit.sh | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe

date

