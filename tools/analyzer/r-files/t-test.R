library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
inputFile <- args[1]
alpha <- as.double(args[2])
q <- read.csv(file = inputFile)

q <- q %>% mutate(V1 = recode(V1, "BASELINE" = "1")) %>% mutate(V1 = recode(V1, "MODIFIED" = "2"))
x <- (q %>% select(V1,V2) %>% filter(V1=="1"))$V2
y <- (q %>% select(V1,V2) %>% filter(V1=="2"))$V2

if(t.test(as.numeric(x),as.numeric(y))$p.value>alpha){
  quit(status = 10)
}else{
  quit(status = 11)
}