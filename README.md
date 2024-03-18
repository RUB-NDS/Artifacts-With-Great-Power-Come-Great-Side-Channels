# Artifact: With Great Power Come Great Side Channels: <br> Statistical Timing Side-Channel Analyses with Bounded Type-1 Errors

Artifact for the USENIX Security '24 publication. The full paper can be found [here](https://www.usenix.org/conference/usenixsecurity24/presentation/dunsche). The datasets collected for our study can be found [here](https://zenodo.org/records/10817685) (DOI 10.5281/zenodo.10817684)

## Scope
This repository contains Dockerfiles and shell scripts that aim to support the user in confirming the results of our study. For this purpose, the shell scripts show how to run the statistical tools considered in our study and how to collect own measurements.

## Structure:
The main directory contains the *setup.sh* script intended to prepare the environment for the experiments described in the artifact appendix of our paper (see below).

Other directories:
- **additional_figures**: Contains figures of our quantitative analysis of TLS libraries besides OpenSSL
- **datasets**: Contains a shell script to download our datasets from Zenodo
- **experiments**: Contains shell scripts that reproduce specific results of our study. The scripts are designed to allow the user to reproduce additional results with few adaptions.
- **measuring**: Contains a Dockerfile that can be used to collect measurements for TLS libraries based on our measuring tool ([TLS-Docker-Timer](https://github.com/tls-attacker/TLS-Docker-Library)) and the [TLS-Docker-Library](https://github.com/tls-attacker/TLS-Docker-Timer).
- **tools**: Contains Dockerfiles that allow the user to run previous open-source tools for statistical analyses of timing measurements as well as our new tool R-Time-Leak-Finder (RTLF)


## Running The Experiments

### Requirements
Running the experiments requires *git* and *Docker* and a minimum of around 55GB of disk storage. Since part of the software used for experiment 3 relies on assembly instructions, ARM CPUs (e.g Apple Silicon) may not be able to run all experiments. Experiment 3 also requires the user to pass the host docker socket to a docker container as our TLS-Docker-Timer tool running in the container manages docker containers for the tested TLS libraries (see [here](https://github.com/tls-attacker/TLS-Docker-Timer/blob/master/README.md) for details).

### Setup
To prepare the environment for the experiments, run the *setup.sh* script. This will perform the following steps:
1. Build the docker image for the analysis of our ground truth measurements (timing-analyzer-artificial)
2. Build the docker image for the analysis of our real-world measurements of TLS libraries (timing-analyzer-real)
3. Build the docker image for collecting and printing the analysis results (timing-reporter)
4. Build the docker image for collecting timing measurements of TLS libraries (tls-docker-timer)
5. Download our datasets (~40GB) from Zenodo
6. Unzip dataset for experiment 1a and 2a
7. Unzip dataset for experiment 1b
8. Unzip dataset for experiment 2b
9. Prepare the environment for experiment 3 using the tls-docker-timer docker image created before

The last step should start the measuring tool, prepare the TLS-Docker-Library, build an example image (NSS 3.87), and collect five timing measurements to confirm that everything works correctly. Note that the preparation of the TLS-Docker-Library and the NSS image build process will add a new docker volume (*cert-data*) and multiple (small) docker images (*alpine-build*, *debian-build*, and *nss-server*) to your docker host instance.


### Experiments

Our experiments 1b, 2b, and 3 require computational effort, as they involve the analysis and collection of timing measurements. To run all three experiments beforehand, use ```./experiments/run_lengthy_experiments.sh```. This is script is expected to take around nine hours. When later going over the individual experiments, the computational steps will be skipped.

For details on the experiments, please see the artifact appendix and the readme file [here](https://github.com/RUB-NDS/Artifacts-With-Great-Power-Come-Great-Side-Channels/tree/main/experiments).