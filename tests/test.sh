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
    if [[ "$?" == "0" && -z "$DIFF" ]]; then
        echo "Test succeeded! :)"
    else
        echo ">>> Test failed! :( <<<"
        exit 1
    fi
}

TEST_TMP=`mktemp -d /tmp/test_temp.XXXXX`

declare -A TEST_CONF
TEST_CONF['input.test.tok-morph']=''
TEST_CONF['input.test.tok-morph-pos']='(~30sec)'
TEST_CONF['halandzsa.test.tok-morph-pos']='testing guesser (~30sec)'
TEST_CONF['input.test.tok-morph-pos-conv_morph-dep']='(~1min)'
TEST_CONF['input.test.tok-morph-pos-conv_morph-dep-chunk-ner']='(~1min)'
TEST_CONF['input.test.tok-spell-morph-pos-conv_morph-dep-chunk-ner-cons-bert_ner-bert_basenp-bert_np']='(~1min)'
TEST_CONF['emDep.test.dep']='(~1min)'
TEST_CONF['emTag.test.pos']='(~1min)'
TEST_CONF['kutya.test.tok-morph-pos-conv_morph-dep']='(~1min)'
TEST_CONF['puzser.test.tok-morph-pos-conv_morph-dep']='(~1min)'
TEST_CONF['alaptorveny_full.txt.tok-morph-pos-conv_morph-dep']='(~1min)'

for output_file in "${!TEST_CONF[@]}"; do
    echo
    act_modules1=${output_file##*.}
    act_modules2=${act_modules1//-/,}
    act_modules3=${act_modules2//_/-}
    input_file=${output_file/.$act_modules1/}
    run_test $TEST_TYPE $act_modules3 \
      ${SCRIPT_DIR}/test_input/$input_file \
      ${TEST_TMP}/$output_file \
      ${SCRIPT_DIR}/test_output/$output_file \
      ${TEST_TMP}/log.$TEST_TYPE.$output_file \
      ${TEST_CONF[$output_file]}
done
