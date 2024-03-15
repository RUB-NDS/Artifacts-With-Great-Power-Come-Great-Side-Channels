
#!/bin/bash
TARGET_DIRECTORY="measurements-15k-same-xy"
THREADS=8
DIRECTORY=$(pwd)

echo "Analyzing $TARGET_DIRECTORY with dudect"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-artificial /$TARGET_DIRECTORY/ 2 $THREADS
echo "Analyzing $TARGET_DIRECTORY with mona"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-artificial /$TARGET_DIRECTORY/ 3 $THREADS
echo "Analyzing $TARGET_DIRECTORY with t-test"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY--rm timing-analyzer-artificial /$TARGET_DIRECTORY 4 $THREADS
echo "Analyzing $TARGET_DIRECTORY with rtlf"
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-analyzer-artificial /$TARGET_DIRECTORY/ 1c $THREADS

# print results
docker run -v $DIRECTORY/datasets/$TARGET_DIRECTORY:/$TARGET_DIRECTORY --rm timing-reporter /$TARGET_DIRECTORY/ all -n