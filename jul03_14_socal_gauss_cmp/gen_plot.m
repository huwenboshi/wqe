data = dlmread('result.txt');

vars = data(:,1);
socal = data(:,2);
gauss = data(:,3);

plot(vars, socal, 'b.');
hold on;
plot(vars, socal, 'b-');
hold on;
plot(vars, gauss, 'r.');
hold on;
plot(vars, gauss, 'r-');