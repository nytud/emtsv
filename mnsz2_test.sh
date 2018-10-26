#!/bin/bash

date

# a trivToken.sh a "január 16-án" formájú tokenek miatt kell
# -> ti. NEM lehet szóköz tokenben! XXX :)

# --- asszem, most már ez is jó! XXX :)
#( echo "string" ; cat test_input/mnsz2_radio_100e.tok.test ) | ./trivToken.sh | ./trivSentSplit.sh | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe > out
# -> 18sec
(( echo "string" ; cat test_input/mnsz2_radio_1mio.tok.test ) | ./trivToken.sh | ./trivSentSplit.sh | cat -s; echo) | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe | python3 ./depToolREST.py --pipe > out
# -> 35sec után elhal... (!) XXX XXX XXX ld.: [./err.1mio] XXX XXX XXX

# --- az alábbi tutira jó... ~ 'make test-morph-tag'
#( echo "string" ; cat test_input/puzser.test | ./trivToken.sh ) | ./trivToken.sh | ./trivSentSplit.sh | python3 ./emMorphREST.py --pipe | python3 ./emTagREST.py --pipe

date

