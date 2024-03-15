docker run -v $(pwd)/datasets/analysis_results:/analysis_results --rm timing-reporter /analysis_results/ground_truth_eval/table2_power_analysis/ all -n
echo 'Press enter to print second batch of results (type-1 error analysis)'
read 
docker run -v $(pwd)/datasets/analysis_results:/analysis_results --rm timing-reporter /analysis_results/ground_truth_eval/table3_type_1_error_analysis/ all -n