#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

test_one() {
  # make target for testing (test-...)
  TARGET=$1
  # input file for testing
  INPUT=$2
  # output file during testing
  OUTPUT=$3
  # gold output for diff
  GOLD=$4
  # message
  MESSAGE=$5

  echo "Testing '${TARGET}' on '${INPUT} should yield ${OUTPUT}' ${MESSAGE}"
  mkdir -p `dirname ${OUTPUT}`
  time make -f ${SCRIPT_DIR}/../Makefile RAWINPUT=${INPUT} test-${TARGET} > ${OUTPUT}
  if diff ${GOLD} ${OUTPUT}; then
    echo "Test succeeded! :)"
  else
    echo ">>> Test failed! :( <<<"
    exit 1
  fi
}

TEST_TMP=`mktemp -d /tmp/test_temp.XXXXX`

echo

test_one tok-morph \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph \
  ${SCRIPT_DIR}/test_output/out.input.tok-morph \
  ""

# ----- tok-morph-tag

echo

test_one tok-morph-tag \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph-tag \
  ${SCRIPT_DIR}/test_output/out.input.tok-morph-tag \
  "(~30sec)"

echo

test_one tok-morph-tag-single \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph-tag-single \
  ${SCRIPT_DIR}/test_output/out.input.tok-morph-tag-single \
  "(~30sec)"

echo

test_one tok-morph-tag-single \
  ${SCRIPT_DIR}/test_input/halandzsa.test \
  ${TEST_TMP}/out.halandzsa.tok-morph-tag \
  ${SCRIPT_DIR}/test_output/out.halandzsa.tok-morph-tag \
  "testing guesser (~30sec)"

echo

# testing on a large file
if [ "$HOSTNAME" = juniper ]; then
test_one tok-morph-tag \
  /store/projects/e-magyar/test_input/hundredthousandwords.txt \
  ${TEST_TMP}/out.100.tok-morph-tag \
  /store/projects/e-magyar/test_output/out.100.tok-morph-tag \
  "testing with a 100.000 word file (~3min)"
fi

# ----- tok-dep

echo

test_one tok-dep-single \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.tok-dep \
  ${SCRIPT_DIR}/test_output/out.input.tok-dep \
  "(~1min)"

# ----- all (without cons)

echo

test_one all-single \
  ${SCRIPT_DIR}/test_input/input.test \
  ${TEST_TMP}/out.input.all \
  ${SCRIPT_DIR}/test_output/out.input.all \
  "(~1min)"

echo

# testing on a large file
if [ "$HOSTNAME" = juniper ]; then
test_one all-single \
  /store/projects/e-magyar/test_input/hundredthousandwords.txt \
  ${TEST_TMP}/out.100.all \
  /store/projects/e-magyar/test_output/out.100.all \
  "testing with a 100.000 word file (~15min)"
fi
