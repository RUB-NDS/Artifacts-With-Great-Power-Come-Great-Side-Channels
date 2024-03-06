args <- commandArgs(trailingOnly = TRUE)
inputFile <-args[1]

load(inputFile, loaded <- new.env())
if(max(loaded[["output"]][[1]]) > 0) {
	quit(status = 11)
} else {
	quit(status = 10)
}
