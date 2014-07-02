data = dlmread('SNP_A-1721275int.txt');
train_data = dlmread('SNP_A-1721275_train.txt');

train_aa_idx = train_data(:,3)==1;
train_aa_data = train_data(train_aa_idx,1:2);

train_ab_idx = train_data(:,3)==2;
train_ab_data = train_data(train_ab_idx,1:2);

train_bb_idx = train_data(:,3)==3;
train_bb_data = train_data(train_bb_idx,1:2);