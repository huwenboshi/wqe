% run robsep on snp one at a time

% parameters
c1 = 1;
c2 = 10000;
c3 = 100;
c4 = 2;

train_file = '/home/huwenbo/Dropbox/Spring14/wqe/jun28_problem_snps/SNP_A-1518245_data.txt';

% read in training data
train_data = dlmread(train_file);

train_data(85,1:2) = train_data(85,1:2)+[-0.5 0.5];

plot(train_data(85,1),train_data(85,2),'ro');
hold on;

train_data(85,3) = 1;

% plot train data
train_aa_idx = train_data(:,3)==1;
num_aa = sum(train_aa_idx);
train_aa_data = train_data(train_aa_idx,1:2);
plot(train_aa_data(:,1),train_aa_data(:,2),'r*');
hold on;

train_ab_idx = train_data(:,3)==2;
num_ab = sum(train_ab_idx);
train_ab_data = train_data(train_ab_idx,1:2);
plot(train_ab_data(:,1),train_ab_data(:,2),'g*');
hold on;

train_bb_idx = train_data(:,3)==3;
num_bb = sum(train_bb_idx);
train_bb_data = train_data(train_bb_idx,1:2);
plot(train_bb_data(:,1),train_bb_data(:,2),'b*');
hold on;

% learn decision region for aa
train_nonaa_data = [train_ab_data;train_bb_data];
[c_aa, E_aa, rho_aa] = robsep(train_aa_data',train_nonaa_data',...
    c1,c2,c3);
E_aa = E_aa/((1+rho_aa)/c4);
%E_aa = E_aa/(num_aa/(num_aa+num_ab+num_bb));
ellipse_plot(E_aa, c_aa);
hold on;

% learn decision region for ab
train_nonab_data = [train_aa_data;train_bb_data];
[c_ab, E_ab, rho_ab] = robsep(train_ab_data',train_nonab_data',c1,c2,c3);
E_ab = E_ab/((1+rho_ab)/c4);
%E_ab = E_ab/(num_ab/(num_aa+num_ab+num_bb));
ellipse_plot(E_ab, c_ab);

% learn decision region for bb
train_nonbb_data = [train_aa_data;train_ab_data];
[c_bb, E_bb, rho_bb] = robsep(train_bb_data',train_nonbb_data',c1,c2,c3);
E_bb = E_bb/((1+rho_bb)/c4);
%E_bb = E_bb/(num_bb/(num_aa+num_ab+num_bb));

% compute accuracy
num_total_test = sum(train_aa_idx)+sum(train_ab_idx)+sum(train_bb_idx);
num_correct = 0;
for i=1:size(train_data,1)
    pt = train_data(i,1:2)';
    class = classify(E_aa, c_aa, E_ab, c_ab, E_bb, c_bb, pt);
    if(class == train_data(i,3))
        num_correct = num_correct + 1;
    end
end

% print accuracy
accuracy = num_correct/num_total_test;
fprintf('accuracy: %f\n', accuracy);