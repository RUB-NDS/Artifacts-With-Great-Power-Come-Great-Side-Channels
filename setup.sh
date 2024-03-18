#!/bin/bash
echo "Starting docker build for artifacts"
cd tools/
echo "[1/9] - Building analyzer image for ground truth evaluation"
docker build -t timing-analyzer-artificial -f dockerfile-analyzer-artificial .
echo "[2/9] - Building analyzer image for real-world evaluation"
docker build -t timing-analyzer-real -f dockerfile-analyzer-real .
echo "[3/9] - Building report tool image for analyzed measurements"
docker build -t timing-reporter -f dockerfile-reporter .
echo "[4/9] - Building TLS-Docker-Timer image to reproduce measurements"
cd ../measuring/
docker build -t tls-docker-timer .

if ! docker image inspect timing-analyzer-artificial > /dev/null 2>&1; then
    echo "Error: timing-analyzer-artificial image is missing"
    exit 1
fi

if ! docker image inspect timing-analyzer-real  > /dev/null 2>&1; then
    echo "Error: timing-analyzer-real image is missing"
    exit 1
fi

if ! docker image inspect timing-reporter > /dev/null 2>&1; then
    echo "Error: timing-reporter image is missing"
    exit 1
fi

if ! docker image inspect tls-docker-timer > /dev/null 2>&1; then
    echo "Error: tls-docker-timer image is missing"
    exit 1
fi
cd ../datasets/
echo "[5/9] Downloading data sets"
./download.sh

echo "[6/9] - Unzipping analysis results"
unzip -q -n e_analysis_results.zip 
echo "[7/9] -  Unzipping measurements of artificial same-xy side channel (15k samplesize) for type-1 error analysis"
unzip -q -j -n a_measurements_ground_truth.zip 'measurements_ground_truth/table3_type_1_error_analysis/measurements-15k-same-xy/*'  -d measurements-15k-same-xy
echo "[8/9] -  Unzipping measurements of MatrixSSL (Bleichenbacher attack) from qualitative analysis"
unzip -q -j -n d_measurements_qualitative.zip 'measurements_qualitative/MATRIXSSL-4.6.0/Bleichenbacher/*' -d MatrixSSL-4.6.0-Bleichenbacher 

# run the TLS-Docker-Time container once to build the default image (NSS v 3.87)
echo "[9/9] -  Preparing TLS-Docker-Timer container"
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/output tls-docker-timer -l nss -v 3.87 -n 1 -i 1 -subtask Bleichenbacher
grep "Subtask Bleichenbacher completed 5 measurements" timing-evaluator.log > /dev/null 2>&1;
if [ $? -ne 1 ]; then
    sleep 1
    rm -f timing-evaluator.log
    echo "Preparation finished."
else
    echo "Preparation of TLS-Docker-Timer container failed."
    exit 1
fi
