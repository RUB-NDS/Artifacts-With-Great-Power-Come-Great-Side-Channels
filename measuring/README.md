# Collecting Measurements of TLS Libraries
We provide a Dockerfile that can be used to reproduce the measurements of our quantitative and qualitative analysis based on our measurement tool (TLS-Docker-Timer). Note that timing measurements vastly depend on the system they are run on so results may vary to some degree.

## Setup
Running the *setup.sh* file of the main directory will also cover the build of this TLS-Docker-Timer image.
The Dockerfile uses Alpine Linux as the baseimage. All dependencies are available as public GitHub repositories, so building this docker image specifically only requires
```
docker build -t tls-docker-timer .
```

## Collecting Measurements
Our tool uses docker images from the TLS-Docker-Library to collect measurements. To do so, the docker container running the tool needs access to a local docker daemon. While the TLS-Docker-Library is included as part of the build process of the TLS-Docker-Timer image, no images of TLS libraries will be built. To facilitate the build and measurement process, the container will build the required docker image at runtime. Note that the created image will be added to you local image storage, so running the container at a later point will not require you to re-build the image.

To use the default setup of our artifact appendix, you can run the TLS-Docker-Timer container using:
```
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/output tls-docker-timer
```

- `-v /var/run/docker.sock:/var/run/docker.sock` will pass your local docker socket to the docker container
- `-v $(pwd):/output` will mount your current working directory as the output directory of the measurement tool

Upon executing this command, the docker container will do the following:
- Prepare the TLS-Docker-Library and its certificate docker volume if it is not available yet (~4 minutes)
- Build the docker image of the TLS library (~3 - 7 minutes)
- Replace certificates in the docker volume to match those of our evaluation
- Start a proxy process used to collect measurements
- Start the TLS-Docker-Timer jar that sends the attack vectors and manages the target's docker container

By default, the docker container will test NSS version 3.87 for a Bleichenbacher timing leak with 100,000 measurements for each of the five attack vectors. Specifically, the following flags will be used for TLS-Docker-Timer.jar:
```
-l nss -v 3.87 -i 100000 -n 100000 -subtask bleichenbacher
```

By adding CLI flags to the docker run command, you can change the tested TLS library and version as well as the attack and the number of measurements. The entrypoint script of the docker container will attempt to parse the library its version from the command string to build the TLS image if it is not available yet. Using the flags from above as the CLI flags would result in the same behavior, as using no flags. As another example, you can test OpenSSL version 1.1.1i for all three attack types (Bleichenbacher, Padding Oracle, and Lucky13) with 500000 measurements per attack vector using:
```
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/output tls-docker-timer -l openssl -v 1.1.1i -i 500000 -n 500000 
```
Note that the docker image will always attempt to collect measurements using a proxy application written in C++. If the proxy does not work on you system (e.g due to virtual CPUs), timing measurements will be collected by the TLS-Docker-Timer Java application itself, which is not recommended as it is more prone to noise and bias.

For further documentation on the CLI flags of the TLS-Docker-Timer, see [here](https://github.com/tls-attacker/TLS-Docker-Timer).

## Certificate Volume
The TLS-Docker-Library usually creates its own docker volume (*cert-data*) containing freshly generated X.509 certificates. We overwrite these certificates to enforce RSA certificates for all server instances (especially for NSS' keystore). Additionally, we add policy files for the Botan TLS library that enables cipher suites with RSA key exchange. This step is performed automatically upon starting the docker container.