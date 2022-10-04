#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MAKEFILE="${SCRIPT_DIR}/../Makefile"

if [[ "$1" == "test-modules" || "$1" == "test-rest-modules" || "$1" == "test-runnable-docker-modules" ]]; then
    TEST_TYPE=$1
else
    echo "ERROR: Must supply at least one of the following:" >&2
    echo "'test-modules', 'test-rest-modules', 'test-runnable-docker-modules' !" >&2
    echo "Be sure that the server has been started for 'test-rest-modules' (http://127.0.0.1:5000)!" >&2
    exit 1
fi

TEST_TMP=`mktemp -d /tmp/test_temp.XXXXX`
mkdir -p ${TEST_TMP}

for output_file in ${SCRIPT_DIR}/test_output/*; do
    output_file=`basename $output_file`
    act_modules1=${output_file##*.}
    act_modules2=${act_modules1//_/,}
    input_file=${output_file/.$act_modules1/}

    echo
    echo "Testing make --no-print-directory -f ${MAKEFILE} ${TEST_TYPE} RAWINPUT=${SCRIPT_DIR}/test_input/$input_file \
        MODULES=${act_modules2} > ${TEST_TMP}/$output_file 2> ${TEST_TMP}/log.$TEST_TYPE.$output_file" >&2

    time make --no-print-directory -f ${MAKEFILE} ${TEST_TYPE} RAWINPUT=${SCRIPT_DIR}/test_input/$input_file \
        MODULES=${act_modules2} > ${TEST_TMP}/$output_file 2> ${TEST_TMP}/log.$TEST_TYPE.$output_file

    if [[ "$?" == "0" && -z "$(diff ${TEST_TMP}/$output_file ${SCRIPT_DIR}/test_output/$output_file)" ]]; then
        echo "Test succeeded! :)" >&2
    else
        echo ">>> Test failed! :( <<<" >&2
        exit 1
    fi
done
