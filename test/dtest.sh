#! /bin/bash

echo 'Test "mtaril/emtsv:test" docker image.'

echo 'CLI'

TESTDIR=$(mktemp -d /tmp/dtestXXXXXX)
INPUT='test/input/alaptorveny.txt'
GOLD='test/gold/alaptorveny_dep.tsv'

BASENAME=$(basename $INPUT)
BASENAME="${BASENAME%.*}" # remove extension

OUTPUT=${TESTDIR}/${BASENAME}.tsv

date >$TESTDIR/log

cat ${INPUT} | \
docker run -i --rm mtaril/emtsv:test tok,morph,pos,conv-morph,dep >${OUTPUT} 2>>${TESTDIR}/log

DIFF=$(git diff --no-index --color-words ${GOLD} ${TESTDIR}/${FNAME}.conllup)

if [ -z "$DIFF" ] ; then
    echo 'Docker CLI test passed.' ;
else
    echo -e "$DIFF"
    echo "Docker CLI test failed, see the $TESTDIR/ directory."
    exit 1
fi

echo $TESTDIR
