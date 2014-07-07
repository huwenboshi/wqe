data = dlmread('result.txt');

vars = data(:,1);
socal = data(:,2);
gauss = data(:,3);

h1 = plot(vars,socal,'-b.',vars,gauss,'-rd','MarkerFaceColor',[1 0 0 ]);
legend('SoCal', 'RLMM');
xlabel('noise variance');
ylabel('concordance rate (%)');

