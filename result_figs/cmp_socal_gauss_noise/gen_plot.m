data = dlmread('result.txt');
data = data(3:end,:);

vars = data(:,1);
socal = data(:,2);
gauss = data(:,3);

h1 = plot(vars,socal,'-b.',vars,gauss,'-rd','MarkerFaceColor',[1 0 0 ]);
legend('SoCal', 'RLMM');
xlim([1 10]);
ylim([88 98.5]);
xlabel('variance of simulated outlier');
ylabel('concordance rate (%)');

