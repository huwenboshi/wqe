source("http://bioconductor.org/biocLite.R")
biocLite("oligo")
biocLite("hapmap100kxba")
biocLite("hapmap100khind")
biocLite("pd.mapping50k.xba240")
biocLite("pd.mapping50k.hind240")
library("oligo")

xba_dir = "/u/home/s/shihuwen/project/wqe/affy100k_data/affy100k_genotype_cel/XBA"
xba_files = list.celfiles(path=xba_dir, full.names=TRUE)
raw = read.celfiles(xba_files)
summary = snprma(raw)

sense_a = A(summary, "sense")
colnames(sense_a) = rownames(pData(phenoData(summary)))
out_name = "/u/home/s/shihuwen/project/wqe/affy100k_intensity/affy100k_xba_sense_a_intensity.txt"
write.table(sense_a, out_name, col.names=NA)

sense_b = B(summary, "sense")
colnames(sense_b) = rownames(pData(phenoData(summary)))
out_name = "/u/home/s/shihuwen/project/wqe/affy100k_intensity/affy100k_xba_sense_b_intensity.txt"
write.table(sense_b, out_name, col.names=NA)
