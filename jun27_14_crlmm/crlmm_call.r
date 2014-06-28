library("oligo")
library("hapmap100khind")
pathCelFiles = "/u/home/s/shihuwen/disk/wqe/affy100k_data/affy100k_genotype_cel/HIND"
fullFilenames <- list.celfiles(path = pathCelFiles,full.names = TRUE)
outputDir <- file.path(getwd(), "crlmmTest")
crlmm(fullFilenames, outputDir, verbose = FALSE)
