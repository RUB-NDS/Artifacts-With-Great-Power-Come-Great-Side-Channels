## Experiments
This directory contains shell scripts that run the experiments also described in our artifact appendix. These experiments do not cover our entire evaluation but are meant as illustrative examples which can easily be adapted to confirm additional results. All experiments expect that the environment was prepared using the *setup.sh* script from the main directory. In particular, the experiments require that all docker images have been built and the required datasets have been extracted. The shell scripts of experiment 1b, 2b, and 3 have been designed to be easily adaptable to reproduce additional results of our study.

### Experiment 1a (E1a)
This experiment collects our analysis results of the different statistical tools, including RTLF. Specifically, we chose the results of Table 2 and Table 3 from our paper. While Table 2 shows the results for known artificial side channels, Table 3 shows the result of our type-1 error analysis, where tools incorrectly identified a timing leak. To run the experiment use ```sh experiments/experiment1a.sh```

**Execution and Results:** The script will run a docker container that collects and prints the analysis results. The results show how often which test correctly identified a timing leak and how often it incorrectly reported a timing leak. The script will first print the results of Table 2, i.e the true-positive rate or *statistical power*. After pressing enter, the tool will present the false-positive rate or *type-1 error rate* of the tools (Table 3 in our paper). The results indicate that both *Mona* and the *t-test* show a high false positive rate for small sample sizes. *dudect*, on the other hand, shows a very low type-1 error rate but also fails to achieve high statistical power, especially for small samplesizes.

The complete expected output is
```
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-30k-shift-1% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 77.4%          | 99.8%    | 74.4%  | 56.2%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 22.6%          | 0.2%     | 25.6%  | 43.8%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-30k-same-mean (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 0.0%           | 0.0%     | 0.0%   | 31.1%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 100.0%         | 100.0%   | 100.0% | 68.9%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-500k-tail (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 0.0%           | 1.7%     | 5.0%   | 44.1%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 100.0%         | 98.3%    | 95.0%  | 55.9%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-500k-same-mean (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 0.0%           | 0.0%     | 0.0%   | 16.6%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 100.0%         | 100.0%   | 100.0% | 83.4%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-500k-shift-5% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 0.0%           | 0.0%     | 0.0%   | 0.9%     |
+----------+----------------+----------+--------+----------+
| Diff:    | 100.0%         | 100.0%   | 100.0% | 99.1%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-30k-tail (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 40.9%          | 100.0%   | 31.7%  | 59.1%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 59.1%          | 0.0%     | 68.3%  | 40.9%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-30k-shift-0.9% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 77.9%          | 100.0%   | 76.4%  | 48.2%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 22.1%          | 0.0%     | 23.6%  | 51.8%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-500k-shift-1% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 2.5%           | 49.1%    | 66.7%  | 68.4%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 97.5%          | 50.9%    | 33.3%  | 31.6%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-500k-shift-0.9% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 6.5%           | 78.8%    | 88.0%  | 54.7%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 93.5%          | 21.2%    | 12.0%  | 45.3%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table2_power_analysis/measurements-30k-shift-5% (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 0.0%           | 1.2%     | 0.0%   | 85.8%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 100.0%         | 98.8%    | 100.0% | 14.2%    |
+----------+----------------+----------+--------+----------+

Completed reporting.
Press enter to print second batch of results (type-1 error analysis)

Selected directory : /analysis_results/ground_truth_eval/table3_type_1_error_analysis/
Selected suffix    : (all)
Selected options   : -n

/analysis_results/ground_truth_eval/table3_type_1_error_analysis/measurements-20k-same-xy (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 90.6%          | 100.0%   | 76.0%  | 69.2%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 9.4%           | 0.0%     | 24.0%  | 30.8%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table3_type_1_error_analysis/measurements-30k-same-xy (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 94.1%          | 100.0%   | 92.5%  | 69.4%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 5.9%           | 0.0%     | 7.5%   | 30.6%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table3_type_1_error_analysis/measurements-25k-same-xy (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 92.4%          | 100.0%   | 87.3%  | 69.4%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 7.6%           | 0.0%     | 12.7%  | 30.6%    |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table3_type_1_error_analysis/measurements-500k-same-xy (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 97.3%          | 100.0%   | 100.0% | 91.2%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 2.7%           | 0.0%     | 0.0%   | 8.8%     |
+----------+----------------+----------+--------+----------+
/analysis_results/ground_truth_eval/table3_type_1_error_analysis/measurements-15k-same-xy (1000 datasets)
+----------+----------------+----------+--------+----------+
|          | rtlf-alpha-9   | dudect   | mona   | t-test   |
+==========+================+==========+========+==========+
| No Diff: | 90.8%          | 100.0%   | 59.2%  | 72.4%    |
+----------+----------------+----------+--------+----------+
| Diff:    | 9.2%           | 0.0%     | 40.8%  | 27.6%    |
+----------+----------------+----------+--------+----------+

```


### Experiment 1b (E1b)
This experiment reproduces the analysis we performed to obtain the results shown in E1a. As extensive compuatational effort is required to analyze all of our measurements with all tools, this experiment is limited to the artificial *same-xy* side channel with *15k* samplesize of our type-1 error analysis. We chose this dataset, as it is the smallest and thus requires the least computational effort. As the name of the "side channel" implies, both distributions are designed to be identical, i.e there is no timing difference. The tools are hence expected to report that there is no timing leak. To run the experiment, use 

```sh experiments/experiment1b.sh```. 

For the t-test and RTLF, this analysis uses a type-1 error threshold of 9%.

**Execution and Results:**  The script will run a docker container for each statistical tool to analyze the 1,000 given sets of measurements. Subsequently, the script will again print the analysis results to console. The results are expected to match those from E1a for the *measurements-same-xy-15k* directory. Only RTLF should show minor deviations as its bootstrap is not deterministic.


### Experiment 2a (E2a)
This experiment collects our analysis results for the real-world example of MatrixSSL. As discussed in our paper, MatrixSSL has a *Bleichenbacher* timing leak as the PKCS parsing code returns early if malformed padding is detected. To run the experiment, use 

```sh experiments/experiment2a.sh```

**Execution and Results:** As shown by the output, only RTLF indicates a timing leak for specific Bleichenbacher measurement pairs of MatrixSSL. Specifically, the output is expected to be:
```
+----------+-------------------------------+----------+--------+----------+------------------------+
|          | rtlf-alpha-0-9                | dudect   | mona   | t-test   | tlsfuzzer-bonferroni   |
+==========+===============================+==========+========+==========+========================+
| No Diff: | B1B2,B3B4,B1B5,B2B5           | (all)    | (all)  | (all)    | (all)                  |
+----------+-------------------------------+----------+--------+----------+------------------------+
| Diff:    | B1B4,B1B3,B2B4,B3B5,B2B3,B4B5 |          |        |          |                        |
+----------+-------------------------------+----------+--------+----------+------------------------+
```


### Experiment 2b (E2b)
This experiment reproduces the analysis results shown in E2a. For this purpose, the script will again run each analysis tool on each of the real-world measurements. For the t-test, tlsfuzzer, and RTLF, this analysis uses a type-1 error threshold of 0.9%. To run the experiment, use 

```sh experiments/experiment2b.sh```

**Execution and Results:** The individual docker containers will first produce the analysis results of the different tools before the results are printed to console. Note that while the number of measurements sets is significantly lower here compared to *E1b*, the datasets are much more extensive (500,000 measurements for each attack vector as opposed to 15,000 used for *same-xy-15k*). The outputs should match those from *E2a*. Due to RTLF's non-deterministic bootstrap, slight deviations are possible.


### Experiment 3 (E3)
Experiment 3 illustrates how to collect timing measurements for a TLS library based on docker containers. For this purpose, the experiment uses the TLS-Docker-Timer, which we developed and used for our study. To run the experiment, use 

```sh experiments/experiment3.sh```.

**Execution and Results:** By default, the script will collect measurements for NSS v3.87, specifically for the *Bleichenbacher* attack. To reduce the computational effort, the script is limited to 100,000 measurements for each vector of the attack. Once the measurements have been obtained, each tool from *E2b* is again used to analyze the measurements. Finally, the script prints the results to console. The results are expected to align with those of Figure 4, 6, and
7 from our paper. Specifically, the tools should indicate timing differences for all vector pairs except B1B3, B2B4, B2B5, and B4B5. However, as the number of measurements is reduced and timing measurements highly depend on the system they are collected on, there may be deviations. This could be both false positives as well as false negatives. The expected output is:
```
+----------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------+
|          | rtlf-alpha-0-9                | dudect                        | mona                          | t-test                        | tlsfuzzer   |
+==========+===============================+===============================+===============================+===============================+=============+
| No Diff: | B4B5,B1B3,B2B4,B2B5           | B2B4,B4B5,B2B5,B1B3           | B1B3,B2B5,B4B5,B2B4           | B4B5,B2B5,B2B4,B1B3           |             |
+----------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------+
| Diff:    | B1B5,B1B4,B2B3,B1B2,B3B5,B3B4 | B1B4,B3B5,B1B2,B2B3,B3B4,B1B5 | B3B4,B1B2,B2B3,B3B5,B1B4,B1B5 | B1B2,B1B5,B2B3,B3B5,B3B4,B1B4 | (all)       |
+----------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------+
```
Note that tlsfuzzer employs a test that is not based on pairwise comparison (Friedman test) and does not indicate which vectors specifically exhibit timing variations. Therefore, we print all vectors categorized as either with or without differences to represent the boolean analysis results.