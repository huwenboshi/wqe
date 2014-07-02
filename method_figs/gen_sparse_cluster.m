data = dlmread('SNP_A-1700211int.txt');
train_data = dlmread('SNP_A-1700211_train.txt');

c4 = 2;

c_aa = [13.0401406105; 11.5331200557];
E_aa = [15.366502377   -4.23183586038;
        -4.23183586038 13.2701697182];
rho_aa = 27.7563720409;
E_aa = E_aa/((1+rho_aa)/c4);

c_ab = [12.4082950631; 12.7980255933];
E_ab = [60.2079043501 -29.0312344412; 
        -29.0312344412 45.0473027062];
rho_ab = 93.9979148433;
E_ab = E_ab/((1+rho_ab)/c4);

c_bb = [11.0247936707; 13.0898109804];
E_bb = [59.8413298228 -29.1244860329;
       -29.1244860329 45.4138772336];
rho_bb = 93.9979148433;
E_bb = E_bb/((1+rho_bb)/c4);


figure;

% plot all data point
plot(data(:,1),data(:,2),'b.');
hold on;

% plot aa training data
plot(train_data(:,1),train_data(:,2),'r.');
hold on;

% plot aa ellipsoid
ellipse_plot(E_aa, c_aa);
hold on;
ellipse_plot(E_ab, c_ab);
hold on;
ellipse_plot(E_bb, c_bb);

xlabel('log(allele A intensity)');
ylabel('log(allele B intensity)');