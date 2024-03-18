## Analyzer and Reporter
In this directory, we provide Dockerfiles to easily run RTLF and the other considered statistical tools and tests on our measurements.

### Building
We recommend building all docker images through the *setup.sh* file in the main directory of the repository. To build these isolated docker images, run the following commands:
```
docker build -t timing-analyzer-artificial -f dockerfile-analyzer-artificial .
docker build -t timing-analyzer-real -f dockerfile-analyzer-real .
docker build -t timing-reporter -f dockerfile-reporter .
```

### Running
To run the analyzer, use the following command:
```
docker run -v <source>:<target> --rm -timing-analyzer-artificial <directory_path> <tool_index> <num_threads>
docker run -v <source>:<target> --rm timing-analyzer-real <directory_path> <tool_index> <num_threads>
```

To run the reporter, use the following command:
```
docker run -v <source>:<target> --rm -it  timing-reporter <directory_path> <suffix_index> <options>
```
Note that the *directory_path* must be a directory in the docker mountpoint (*\<target>*).

The available tools to use as *suffix_index* are:
- 1a - RTLF with a the lowest type-1 error achievable based on our bootstrap
- 1b - RTLF with a type-1 error threshold of 0.9% (used for the real-world study)
- 1c - RTLF with a type-1 error threshold of 9% (used for the ground truth)
- 1d - RTLF with a type-1 error threshold of 18%
- 2 - dudect
- 3 - mona (mona-timing-report)
- 4 - t-test
- 5a - tlsfuzzer
- 5b - tlsfuzzer with Bonferroni correction

The *timing-reporter* container further accepts *all* as the *suffix_index* to collect all present results and print them as a table.
Options for the *timing-reporter* container are ```-n```, for short output, or ```-d```, for detailed output.

### Open-Source Tools
The *analyzer* docker images include the following tools which get cloned during the build process from their respective GitHub repositories:
- [dudect](https://github.com/oreparaz/dudect)
- [mona-timing-report](https://github.com/seecurity/mona-timing-report)
- [tlsfuzzer](https://github.com/tlsfuzzer/tlsfuzzer)

### Adaptions
To facilitate the automated comparison of the different tools, we implemented exit codes that depict the result of the analysis (timing leak / no leak). We further adapted *dudect* to operate on pre-collected measurements as it usually collects the measurements itself. For transparency, we provide these changes as git patchfiles in the [analyzer/patches](https://github.com/RUB-NDS/Artifacts-With-Great-Power-Come-Great-Side-Channels/tree/main/tools/analyzer/patches) subdirectory. Note that tlsfuzzer's analysis script already uses exit codes 1 and 0 as its resultcodes so we did not modify it further. 


### Analysis Results
To compare analysis results at a later point, we store them with distinct file extensions of the shape [analyzed csv file].result-[tool]. Each file contains the exit code that expresses if a timing difference was found by the tool (11) or not (10) (or 1 and 0 in the case of tlsfuzzer). The output of RTLF stored as RDATA further contains details about the bootstrap results of the individual deciles. The RDATA can be inspected using R.