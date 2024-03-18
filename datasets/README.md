## Datasets
The script *download.sh* collects our datasets from Zenodo. The datasets are provided as zip files and require ~40GB of disk space. Running *setup.sh* from the main directory of the repository will also download the zip files.

### Structure
Downloading the datasets should yield six zip files:
- a_measurements_ground_truth.zip: Contains all of our measurements for the artificial side channels. For each type of artificial side channel and sample size, we collected 1,000 measurement sets.
- b_measurements_quantitative_openssl.zip: Contains all of our measurements for the quantitative analysis of the OpenSSL TLS library. The measurements are split into a small sample size of 30,000 (primarily used for our tool comparison) and the regular sample size of 200,000 (primarily used to study the development of the library).
- c_measurements_quantitative_other_libraries.zip: Contains the measurements of the quantitative analysis of the TLS libraries besides OpenSSL (BearSSL, BoringSSL, Botan, GnuTLS, LibreSSL, MatrixSSL, mbedTLS, NSS, tlslite-ng, and wolfSSL)
- d_measurements_qualitative.zip: Contains the measurements of the qualitative analysis (i.e more extensive datasets of the most recent versions of the 11 considered TLS libraries)
- e_analysis_results.zip: Contains all results obtained using RTLF and the other considered statistical tools and tests for all of the measurements contained in zip files *a_* to *d_*.
- f_source_files_artificial_side_channels.zip: Contains the C code of the artificial side channels used for our ground truth. 