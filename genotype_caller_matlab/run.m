wfid = fopen('result.txt','w');
fid = fopen('snps.txt');

% parameters
c1 = 1;
c2 = 10;
c3 = 100;
c4 = 32;

dir = './';
tline = fgetl(fid);
while ischar(tline)
    train_file = sprintf('%s%s%s',dir,tline,'_train.txt');
    valid_file = sprintf('%s%s%s',dir,tline,'_validate.txt');
    
    % read in training data
    train_data = dlmread(train_file);

    % plot train data
    train_aa_idx = train_data(:,3)==1;
    train_aa_data = train_data(train_aa_idx,1:2);
    h1 = plot(train_aa_data(:,1),train_aa_data(:,2),'r*');
    hold on;
    
    train_ab_idx = train_data(:,3)==2;
    train_ab_data = train_data(train_ab_idx,1:2);
    plot(train_ab_data(:,1),train_ab_data(:,2),'r*')
    hold on;
    
    train_bb_idx = train_data(:,3)==3;
    train_bb_data = train_data(train_bb_idx,1:2);
    plot(train_bb_data(:,1),train_bb_data(:,2),'r*');
    hold on;
    
    % learn decision region for aa
    train_nonaa_data = [train_ab_data;train_bb_data];
    [c_aa, E_aa, rho_aa] = maxsep(train_aa_data',train_nonaa_data');
    E_aa = E_aa/((1+rho_aa)/c4);
    ellipse_plot(E_aa, c_aa);
    break;
end

fclose(fid);
fclose(wfid);
