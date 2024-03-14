#!/bin/ash

if [ $# -eq 0 ]; then
    # no args provided - use defaults
    IMAGE_NAME="nss"
    IMAGE_TAG="3.87"
    CLI_FLAGS="-i 100000 -n 100000 -l $IMAGE_NAME -v $IMAGE_TAG -proxy -subtask bleichenbacher"
else
    # parse from args
    while getopts ":l:v:" opt; do
    case ${opt} in
        l)
        IMAGE_NAME="$OPTARG"
        ;;
        v)
        IMAGE_TAG="$OPTARG"
        ;;
        :)
        echo "Option -$OPTARG requires an argument" >&2
        exit 1
        ;;
    esac
    done
    CLI_FLAGS="$@"
fi
VOLUME_NAME="cert-data"


# Check if the TLS-Docker-Library cert volume exists otherwise, call setup.sh
if docker volume inspect "$VOLUME_NAME" &> /dev/null; then
    echo "[+] Found TLS-Docker-Library certificate volume."
else
    echo "[-] TLS-Docker-Library certificate volume is missing. Will attempt to prepare docker library."
    cd /TLS-Docker-Library/
    sh setup.sh | sed 's/^/[TLS-Docker-Library Setup]: /'
    if docker volume inspect "$VOLUME_NAME" &> /dev/null; then
        echo "[+] Successfully prepared TLS-Docker-Library"
    else
        echo "[-] Failed to prepare TLS-Docker-Library."
        exit 1
    fi
fi

# Check if the image exists otherwise, build it
if docker inspect "$IMAGE_NAME-server:$IMAGE_TAG" &> /dev/null; then
    echo "[+] Found docker image for '$IMAGE_NAME-server:$IMAGE_TAG'."
else
    cd /TLS-Docker-Library/
    echo "[-] Docker image '$IMAGE_NAME-server:$IMAGE_TAG' does not exist. Will attempt to build it using TLS-Docker-Library."
    if [ -f "certs/out/ca.pem" ]; then
        echo "[+] TLS-Docker-Library is ready to build"
    else
        echo "[-] Preparing TLS-Docker-Library again"
        sh setup.sh | sed 's/^/[TLS-Docker-Library Setup]: /'
        if [ ! -f "certs/out/ca.pem" ]; then
            echo "[-] Failed to prepare TLS-Docker-Library"
            exit 1
        fi
        echo "[+] Successfully prepared TLS-Docker-Library"
    fi
    
    python3 -u images/build-everything.py -l $IMAGE_NAME -v $IMAGE_TAG | sed 's/^/[TLS-Docker-Library Image Build]: /'

    if docker inspect "$IMAGE_NAME-server:$IMAGE_TAG" &> /dev/null; then
        # Client implementation is not required
        docker image rm $IMAGE_NAME-client:$IMAGE_TAG &> /dev/null
    else
        echo "[-] Failed to build '$IMAGE_NAME:$IMAGE_TAG' using TLS-Docker-Library"
        exit 1
    fi
fi

cd /entrypoint/

# Overwrite certificates that are relevant for the evaluation
docker run -v cert-data:/data --name cert-data-helper-container busybox true &> /dev/null
docker cp evalCerts/_data/. cert-data-helper-container:/data &> /dev/null
if [ $? -eq 0 ]; then
    echo "[+] Replaced certificates in docker volume"
else
    echo "[-] Failed to replace certificates in docker volume"
    exit 1
fi
docker rm cert-data-helper-container &> /dev/null
echo "Starting Timing-Proxy in background."
./loopProxy.sh > /dev/null 2>&1 &
echo "Starting TLS-Docker-Timer."
cd /output
java -jar /TLS-Docker-Timer/apps/TLS-Docker-Timer.jar $CLI_FLAGS