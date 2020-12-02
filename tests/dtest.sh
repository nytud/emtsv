#! /bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TESTDIR=$(mktemp -d /tmp/dtestXXXXXX)
GOLDDIR="${SCRIPT_DIR}/test_output"
# MODFULL='tok,spell,morph,pos,conv-morph,dep,chunk,ner,cons,bert-ner,bert-basenp,bert-np'
MODALL='tok,morph,pos,conv-morph,dep,chunk,ner'

echo "Temporary files are stored in $TESTDIR"
date >$TESTDIR/log
cat ${SCRIPT_DIR}/test_input/input.test | \
docker run -i --rm mtaril/emtsv:test $MODALL >$TESTDIR/all.tsv 2>>$TESTDIR/log

DIFF=$(git diff --no-index --color-words $GOLDDIR/all.tsv $TESTDIR/all.tsv)

if [ -z "$DIFF" ] ; then
    echo 'Docker test passed.' ;
else
    echo -e "$DIFF"
    echo "Docker test failed, see the $TESTDIR/ directory."
    exit 1
fi
