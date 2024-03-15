#!/bin/bash
TARGET_DIRECTORY="MatrixSSL-4.6.0-Bleichenbacher"
THREADS=8
DIRECTORY=$(pwd)

echo "Analyzing $TARGET_DIRECTORY measurements with dudect"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-real /$TARGET_DIRECTORY/ 2 $THREADS
echo "Analyzing $TARGET_DIRECTORY measurements with mona"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-real /$TARGET_DIRECTORY/ 3 $THREADS
echo "Analyzing $TARGET_DIRECTORY measurements with t-test"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-real /$TARGET_DIRECTORY/ 4 $THREADS
echo "Analyzing $TARGET_DIRECTORY measurements with tlsfuzzer"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-real /$TARGET_DIRECTORY/ 5a $THREADS
echo "Analyzing $TARGET_DIRECTORY measurements with rtlf"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-real /$TARGET_DIRECTORY/ 1b $THREADS

# print results
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-reporter /$TARGET_DIRECTORY/ all -n