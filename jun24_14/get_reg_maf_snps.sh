awk '{if($2<=0.7 && $2 >= 0.3) print $1}' ../jun21_14/trainpct_90_ellipsoids.txt > reg_maf_snps.txt
