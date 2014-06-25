data_train = dlmread('selected_reg_maf/SNP_A-1713561_train.txt');
data_valid = dlmread('selected_reg_maf/SNP_A-1713561_validate.txt');
data_full = [data_train; data_valid];
figure;
plot(data_full(:,1),data_full(:,2),'b.');

data_train = dlmread('selected_low_maf/SNP_A-1643082_train.txt');
data_valid = dlmread('selected_low_maf/SNP_A-1643082_validate.txt');
data_full = [data_train; data_valid];
figure;
plot(data_full(:,1),data_full(:,2),'b.');