cd ../cvx
cvx_setup
cd ../main

wfid = fopen('result_maxsep_time.txt','w');
fid = fopen('/home/huwenbo/wqe_subset/snps.txt');

% parameters
c1 = 1;
c2 = 10;
c3 = 100;
c4 = 32;

tic;

dir = '/home/huwenbo/wqe_subset/';
tline = fgetl(fid);
while ischar(tline)
    train_file = sprintf('%s%s%s',dir,tline,'_train.txt');
    valid_file = sprintf('%s%s%s',dir,tline,'_validate.txt');
    
    % read in training data
    train_data = dlmread(train_file);

    % plot train data
    train_aa_idx = train_data(:,3)==1;
    train_aa_data = train_data(train_aa_idx,1:2);

    train_ab_idx = train_data(:,3)==2;
    train_ab_data = train_data(train_ab_idx,1:2);

    train_bb_idx = train_data(:,3)==3;
    train_bb_data = train_data(train_bb_idx,1:2);

    % learn decision region for aa
    tic;
    train_nonaa_data = [train_ab_data;train_bb_data];
    [c_aa, E_aa, rho_aa] = maxsep(train_aa_data',train_nonaa_data');
    E_aa = E_aa/((1+rho_aa)/c4);

    % learn decision region for ab
    train_nonab_data = [train_aa_data;train_bb_data];
    [c_ab, E_ab, rho_ab] = maxsep(train_ab_data',train_nonab_data');
    E_ab = E_ab/((1+rho_ab)/c4);

    % learn decision region for bb
    train_nonbb_data = [train_aa_data;train_ab_data];
    [c_bb, E_bb, rho_bb] = maxsep(train_bb_data',train_nonbb_data');
    E_bb = E_bb/((1+rho_bb)/c4);
    tt = toc;

    % read in validation data
    valid_data=dlmread(valid_file);

    % plot validation data
    tic;
    valid_aa_idx = valid_data(:,3)==1;
    valid_aa_data = valid_data(valid_aa_idx,1:2);

    valid_ab_idx = valid_data(:,3)==2;
    valid_ab_data = valid_data(valid_ab_idx,1:2);

    valid_bb_idx = valid_data(:,3)==3;
    valid_bb_data = valid_data(valid_bb_idx,1:2);
    tv = toc;

    % compute accuracy
    num_total_test = sum(valid_aa_idx)+sum(valid_ab_idx)+...
        sum(valid_bb_idx);
    num_correct = 0;
    for i=1:size(valid_data,1)
        pt = valid_data(i,1:2)';
        class = classify(E_aa, c_aa, E_ab, c_ab, E_bb, c_bb, pt);
        if(class == valid_data(i,3))
            num_correct = num_correct + 1;
        end
    end

    % print accuracy
    accuracy = num_correct/num_total_test;
    fprintf(wfid, '%s %f %f %f\n', tline, accuracy, tt, tv);
    
    tline = fgetl(fid);
end

fclose(fid);
fclose(wfid);

toc;
