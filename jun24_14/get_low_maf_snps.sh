awk '{if(($2>=0.99 || $2 <= 0.01) && $2 != 1) print $1}' ../jun21_14/trainpct_90_ellipsoids.txt > low_maf_snps.txt
