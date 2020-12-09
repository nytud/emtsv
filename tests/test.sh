#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ "$1" == "test-modules" || "$1" == "test-rest-modules" || "$1" == "test-runnable-docker-modules" ]]; then
    TEST_TYPE=$1
else
    echo "ERROR: Must supply at least one of the following:" >&2
    echo "'test-modules', 'test-rest-modules', 'test-runnable-docker-modules'" >&2
    echo "Be sure that the server has been started (http://127.0.0.1:5000)!" >&2
    exit 1
fi

function run_test() {
    # test-modules or test-rest-modules
    TEST_TARGET=$1
    # modules for testing
    MODULES=$2
    # input file for testing
    INPUT=$3
    # output file during testing
    OUTPUT=$4
    # gold output for diff
    GOLD=$5
    # Log
    LOG=$6
    # message
    MESSAGE=$7

    MAKEFILE="${SCRIPT_DIR}/../Makefile"
    echo "Testing make -f ${MAKEFILE} ${TEST_TARGET} RAWINPUT=${INPUT} MODULES=${MODULES} > ${OUTPUT} 2> ${LOG}"
    echo "${MESSAGE}"

    mkdir -p `dirname ${OUTPUT}`
    time make -f ${MAKEFILE} ${TEST_TARGET} RAWINPUT=${INPUT} MODULES=${MODULES} > ${OUTPUT} 2> ${LOG}
    DIFF=$(diff ${GOLD} ${OUTPUT})
    if [ -z "$DIFF" ] ; then
        echo "Test succeeded! :)"
    else
        echo ">>> Test failed! :( <<<"
        exit 1
    fi
}

TEST_TMP=`mktemp -d /tmp/test_temp.XXXXX`

echo

run_test $TEST_TYPE tok,morph \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph \
  ${SCRIPT_DIR}/test_output/out.input.tok-morph \
  ${TEST_TMP}/log.input.tok-morph \
  ''

# ----- tok-morph-log

echo

run_test $TEST_TYPE tok,morph,pos \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph-pos \
  ${SCRIPT_DIR}/test_output/out.input.tok-morph-pos \
  ${TEST_TMP}/log.input.tok-morph-pos \
  '(~30sec)'

echo

run_test $TEST_TYPE tok,morph,pos \
  ${SCRIPT_DIR}/test_input/halandzsa.test \
  ${TEST_TMP}/out.halandzsa.tok-morph-pos \
  ${SCRIPT_DIR}/test_output/out.halandzsa.tok-morph-pos \
  ${TEST_TMP}/log.halandzsa.tok-morph-pos \
  'testing guesser (~30sec)'

echo

# ----- tok-dep

echo

run_test $TEST_TYPE tok,morph,pos,conv-morph,dep \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-dep \
  ${SCRIPT_DIR}/test_output/out.input.tok-dep \
  ${TEST_TMP}/log.input.tok-dep \
  '(~1min)'

# ----- all (without cons)

echo

run_test $TEST_TYPE tok,morph,pos,conv-morph,dep,chunk,ner \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.all \
  ${SCRIPT_DIR}/test_output/out.input.all \
  ${TEST_TMP}/log.input.all \
  '(~1min)'

echo

# Mod full tok,spell,morph,pos,conv-morph,dep,chunk,ner,cons,bert-ner,bert-basenp,bert-np
run_test $TEST_TYPE tok,morph,pos,conv-morph,dep,chunk,ner \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.all.tsv \
  ${SCRIPT_DIR}/test_output/all.tsv \
  ${TEST_TMP}/log.all.tsv \
  '(~1min)'

echo
