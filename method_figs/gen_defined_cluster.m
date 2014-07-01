data = dlmread('SNP_A-1721275int.txt');
train_data = dlmread('SNP_A-1721275_train.txt');

figure;

% plot all data point
plot(data(:,1),data(:,2),'b.');
hold on;

% plot aa training data
plot(train_data(:,1),train_data(:,2),'r.');
hold on;

xlabel('log(allele A intensity)', 'FontSize', 20);
ylabel('log(allele B intensity)', 'FontSize', 20);