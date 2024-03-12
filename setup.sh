#!/bin/bash
echo "Starting docker build for artifacts"
cd tools/
echo "[1/4] - Building analyzer image for ground truth evaluation"
docker build -t timing-analyzer-artificial -f dockerfile-analyzer-artificial .
echo "[2/4] - Building analyzer image for real-world evaluation"
docker build -t timing-analyzer-real -f dockerfile-analyzer-real .
echo "[3/4] - Building report tool image for analyzed measurements"
docker build -t timing-reporter -f dockerfile-reporter .
echo "[4/4] - Building TLS-Docker-Timer image to reproduce measurements"
cd ../measuring/
docker build -t tls-docker-timer .

if ! docker image inspect timing-analyzer-artificial > /dev/null 2>&1; then
    echo "Error: timing-analyzer-artificial image is missing"
    return 1
fi

if ! docker image inspect timing-analyzer-real  > /dev/null 2>&1; then
    echo "Error: timing-analyzer-real image is missing"
    return 1
fi

if ! docker image inspect timing-reporter > /dev/null 2>&1; then
    echo "Error: timing-reporter image is missing"
    return 1
fi

if ! docker image inspect tls-docker-timer > /dev/null 2>&1; then
    echo "Error: tls-docker-timer image is missing"
    return 1
fi

echo "Successfully built artifact images"