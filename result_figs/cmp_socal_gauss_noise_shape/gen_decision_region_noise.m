addpath('../../genotype_caller_matlab/');

data = dlmread('SNP_A-1721275int.txt');
train_data = dlmread('SNP_A-1721275_train.txt');

outlier = [14 9 1];
train_data = [train_data; outlier];

% find the ellipsoids
c1 = 1;
c2 = 10000;
c3 = 100;
c4 = 2;

train_aa_idx = train_data(:,3)==1;
num_aa = sum(train_aa_idx);
train_aa_data = train_data(train_aa_idx,1:2);

train_ab_idx = train_data(:,3)==2;
num_ab = sum(train_ab_idx);
train_ab_data = train_data(train_ab_idx,1:2);

train_bb_idx = train_data(:,3)==3;
num_bb = sum(train_bb_idx);
train_bb_data = train_data(train_bb_idx,1:2);

train_nonaa_data = [train_ab_data;train_bb_data];
[c_aa, E_aa, rho_aa] = robsep(train_aa_data',train_nonaa_data',...
    c1,c2,c3);
E_aa = E_aa/((1+rho_aa)/c4);

train_nonab_data = [train_aa_data;train_bb_data];
[c_ab, E_ab, rho_ab] = robsep(train_ab_data',train_nonab_data',c1,c2,c3);
E_ab = E_ab/((1+rho_ab)/c4);

train_nonbb_data = [train_aa_data;train_ab_data];
[c_bb, E_bb, rho_bb] = robsep(train_bb_data',train_nonbb_data',c1,c2,c3);
E_bb = E_bb/((1+rho_bb)/c4);

% create a new figure
figure;

% plot all data point
plot(data(:,1),data(:,2),'b.');
hold on;

% plot training data
plot(train_data(:,1),train_data(:,2),'r.');
hold on;

% plot the ellipsoids
ellipse_plot(E_aa, c_aa);
ellipse_plot(E_ab, c_ab);
ellipse_plot(E_bb, c_bb);
hold on;

% plot the outlier
plot(outlier(:,1), outlier(:,2),'d','color',[0 0.5 0],...
    'MarkerFaceColor',[0 0.5 0],'MarkerSize',7.5);

% add label
xlabel('log(allele A intensity)');
ylabel('log(allele B intensity)');
xlim([10 15]);
ylim([8.5 15])
axis equal;
title('SNP\_A-1721275');

%-------------------------------------------------------------------------

% find the gaussian parameters
[m_aa, v_aa, m_ab, v_ab, m_bb, v_bb] = gauss_est(train_aa_data, ...
    train_ab_data, train_bb_data);

% start a new figure
figure;

% plot the data
% plot all data point
plot(data(:,1),data(:,2),'b.');
hold on;

% plot training data
plot(train_data(:,1),train_data(:,2),'r.');
hold on;

% plot the gaussian
elpt = ellipsedata(v_aa, m_aa, 100, [3,5,7]);
plot(elpt(:,1:2:end),elpt(:,2:2:end),'k', m_aa(1), m_aa(2), 'ko',...
    'MarkerFaceColor',[1 1 1]);
hold on;

elpt = ellipsedata(v_ab, m_ab, 100, [3,5,7]);
plot(elpt(:,1:2:end),elpt(:,2:2:end),'k', m_ab(1), m_ab(2), 'ko',...
    'MarkerFaceColor',[1 1 1]);
hold on;

elpt = ellipsedata(v_bb, m_bb, 100, [3,5,7]);
plot(elpt(:,1:2:end),elpt(:,2:2:end),'k', m_bb(1), m_bb(2), 'ko',...
    'MarkerFaceColor',[1 1 1]);
hold on;

% plot the outlier
plot(outlier(:,1), outlier(:,2),'d','color',[0 0.5 0],...
    'MarkerFaceColor',[0 0.5 0],'MarkerSize',7.5);

% add label
xlabel('log(allele A intensity)');
ylabel('log(allele B intensity)');
xlim([10 15]);
ylim([8.5 15])
axis equal;
title('SNP\_A-1721275');
