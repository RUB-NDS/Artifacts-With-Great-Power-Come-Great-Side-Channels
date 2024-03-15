#!/bin/bash

# Download our data sets from Zenodo (https://zenodo.org/records/10817685)
wget -nc https://zenodo.org/records/10817685/files/a_measurements_ground_truth.zip
wget -nc https://zenodo.org/records/10817685/files/b_measurements_quantitative_openssl.zip
wget -nc https://zenodo.org/records/10817685/files/c_measurements_quantitative_other_libraries.zip
wget -nc https://zenodo.org/records/10817685/files/d_measurements_qualitative.zip
wget -nc https://zenodo.org/records/10817685/files/e_analysis_results.zip
wget -nc https://zenodo.org/records/10817685/files/f_source_files_artificial_side_channels.zip