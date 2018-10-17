#!/bin/bash

date

( echo "string" ; cat test_input/mnsz2_radio_100e.tok.test ) | ./trivSentSplit.sh | python3 ./emMorphREST.py | python3 ./emTagREST.py > out

date

