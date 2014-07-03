data = dlmread('result.txt');

vars = data(:,1);
socal = data(:,2);
gauss = data(:,3);

h1 = plot(vars, socal, '-b.', vars, gauss, '-r.');
legend('SoCal', 'simRLMM');
xlabel('noise variance');
ylabel('concordance rate (%)');

