#!/bin/bash
MEASUREMENTS_PER_VECTOR=100000
LIBRARY="nss" # wolfssl/openssl/libressl/gnutls/...
LIBRARY_OUT="NSS"
LIBRARY_VERSION="3.87"
SUBTASK="Bleichenbacher" # Bleichenbacher/PaddingOracle/Lucky13
DIRECTORY=$(pwd)

if [ ! -d "./own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION" ]; then
    docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $DIRECTORY:/output tls-docker-timer -l $LIBRARY -v $LIBRARY_VERSION -i $MEASUREMENTS_PER_VECTOR -n $MEASUREMENTS_PER_VECTOR -subtask $SUBTASK
else
    echo "Measurements directory already exists - skipping measuring with TLS-Docker-Timer container"
fi

echo "Analyzing own $LIBRARY_OUT $LIBRARY_VERSION measurements with dudect"
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-analyzer-real /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK 2 8
echo "Analyzing own $LIBRARY_OUT $LIBRARY_VERSION measurements with mona"
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-analyzer-real /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK/ 3 8
echo "Analyzing own $LIBRARY_OUT $LIBRARY_VERSION measurements with t-test"
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-analyzer-real /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK/ 4 8
echo "Analyzing own $LIBRARY_OUT $LIBRARY_VERSION measurements with tlsfuzzer"
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-analyzer-real /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK/ 5a 8
echo "Analyzing own $LIBRARY_OUT $LIBRARY_VERSION measurements with rtlf"
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-analyzer-real /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK/ 1b 8

# print results
docker run -v $DIRECTORY/own_measurements/$LIBRARY_OUT-$LIBRARY_VERSION/$SUBTASK:/$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK --rm timing-reporter /$LIBRARY_OUT-$LIBRARY_VERSION-$SUBTASK/ all -d
