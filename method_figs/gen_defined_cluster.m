data = dlmread('SNP_A-1722680int.txt');
figure;
plot(data(:,1),data(:,2),'b.');
xlabel('log(allele A intensity)');
ylabel('log(allele B intensity)');