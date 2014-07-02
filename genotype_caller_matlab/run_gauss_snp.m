% run robsep on snp one at a time

% parameters
c1 = 1;
c2 = 10000;
c3 = 100;
c4 = 2;

train_file = '/home/huwenbo/Dropbox/Spring14/wqe/jun28_problem_snps/SNP_A-1518245_data.txt';

% read in training data
train_data = dlmread(train_file);
ndata = size(train_data,1);

% plot train data
train_aa_idx = train_data(:,3)==1;
num_aa = sum(train_aa_idx);

% generate noise
train_aa_data_label = train_data(train_aa_idx,:);
noise_center = train_aa_data_label(randi(num_aa),1:2);
noise_draw = mean(train_aa_data_label(:,1:2))+mvnrnd([0 0], eye(2)*4);
train_data = [train_data; noise_draw 1];
plot(noise_center(1),noise_center(2),'bo', 'MarkerSize', 10);
hold on;
plot(noise_draw(1),noise_draw(2),'ko');
hold on;

train_aa_idx = train_data(:,3)==1;
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
ellipse_plot(E_aa, c_aa);
hold on;

% learn decision region for ab
train_nonab_data = [train_aa_data;train_bb_data];
[c_ab, E_ab, rho_ab] = robsep(train_ab_data',train_nonab_data',c1,c2,c3);
E_ab = E_ab/((1+rho_ab)/c4);
ellipse_plot(E_ab, c_ab);

% learn decision region for bb
train_nonbb_data = [train_aa_data;train_ab_data];
[c_bb, E_bb, rho_bb] = robsep(train_bb_data',train_nonbb_data',c1,c2,c3);
E_bb = E_bb/((1+rho_bb)/c4);
%ellipse_plot(E_bb, c_bb);

% gauss stuff
[m_aa, v_aa, m_ab, v_ab, m_bb, v_bb] = gauss_est(train_aa_data, ...
    train_ab_data, train_bb_data);

% compute accuracy
num_total_test = sum(train_aa_idx)+sum(train_ab_idx)+sum(train_bb_idx);
num_correct = 0;
num_correct_g = 0;
for i=1:ndata
    pt = train_data(i,1:2)';
    class = classify(E_aa, c_aa, E_ab, c_ab, E_bb, c_bb, pt);
    class_g = gauss_classify(m_aa,v_aa,m_ab,v_ab,m_bb,v_bb,pt);
    if(class == train_data(i,3) && i <= ndata)
        num_correct = num_correct + 1;
    else
        disp(train_data(i,:));
    end
    if(class_g == train_data(i,3) && i <= ndata)
        num_correct_g = num_correct_g+1;
    end
end

% print accuracy
accuracy = num_correct/num_total_test;
accuracy_g = num_correct_g/num_total_test;

fprintf('ellipse accuracy: %f\n', accuracy);
fprintf('gauss accuracy: %f\n', accuracy_g);