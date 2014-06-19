#!/bin/bash

../scripts/combine_ref_and_int.py \
    -r ../reference_call_hapmart/refcall_hapmart_reformated_allele_fixed.txt \
    -i ../affy100k_intensity/affy100k_xba_combined_intensity.txt \
    -m ../array_annotation/affy100k_annot.combined.csv.map > ../affy100k_training_data_full/affy100_xba_training_full.txt
