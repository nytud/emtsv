#!/bin/bash

test_one() {
  # make target for testing (test-...)
  T=$1
  # input file for testing
  I=$2
  # output file during testing
  O=$3
  # gold output for diff
  G=$4
  # message
  M=$5

  echo "Testing '$T' on '$I' $M"
  mkdir -p `dirname $O`
  time make -f ../Makefile RAWINPUT=$I test-$T > $O
  if diff $G $O; then
    echo "Test succeeded! :)"
  else
    echo ">>> Test failed! :( <<<"
  fi
}

TEST_TMP=`mktemp -d test_temp.XXXXX`

echo

test_one tok-morph \
  test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph \
  test_output/out.input.tok-morph \
  ""

# ----- tok-morph-tag

echo

test_one tok-morph-tag \
  test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph-tag \
  test_output/out.input.tok-morph-tag \
  "(~30sec)"

echo

test_one tok-morph-tag-single \
  test_input/input.test \
  ${TEST_TMP}/out.input.tok-morph-tag-single \
  test_output/out.input.tok-morph-tag-single \
  "(~30sec)"

echo

test_one tok-morph-tag-single \
  test_input/halandzsa.test \
  ${TEST_TMP}/out.halandzsa.tok-morph-tag \
  test_output/out.halandzsa.tok-morph-tag \
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
  test_input/input.test \
  ${TEST_TMP}/out.input.tok-dep \
  test_output/out.input.tok-dep \
  "(~1min)"

# ----- all (without cons)

echo

test_one all-single \
  test_input/input.test \
  ${TEST_TMP}/out.input.all \
  test_output/out.input.all \
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
