data = dlmread('SNP_A-1721275int.txt');
train_data = dlmread('SNP_A-1721275_train.txt');

c4 = 2;

c_aa = [13.0854384578; 11.7470601948];
E_aa = [32.3104794093 -19.9674186637;
        -19.9674186637 23.9591749814];
rho_aa = 66.0892137393;
E_aa = E_aa/((1+rho_aa)/c4);

c_ab = [12.4688805744; 13.0527713064];
E_ab = [32.8935946836 -16.7439154593;
        -16.7439154593 28.6796413384];
rho_ab = 46.9841189466;
E_ab = E_ab/((1+rho_ab)/c4);

c_bb = [11.4027965222; 13.6677924444];
E_bb = [20.0749398169 -13.143836991;
        -13.143836991 44.7413914249];
rho_bb = 44.1049172054;
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