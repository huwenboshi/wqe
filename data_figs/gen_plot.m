data = dlmread('allele_freq.txt');
data(data > 0.5) = 1-data(data > 0.5);
hist(data);
xlabel('minor allele frequency (MAF)');
ylabel('count');

num_nonmorph = sum(data == 0 || data == 1);