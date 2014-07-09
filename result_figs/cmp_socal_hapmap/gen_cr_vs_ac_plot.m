tbl_1_10000_100 = dlmread('cr_vs_ac_1_10000_100.txt');
tbl_1_10000_100(:,2) = tbl_1_10000_100(:,2)*100;
plot(tbl_1_10000_100(:,1),tbl_1_10000_100(:,2),'b.-');
hold on;

tbl_1_1_100 = dlmread('cr_vs_ac_1_1_100.txt');
tbl_1_1_100(:,2) = tbl_1_1_100(:,2)*100;
plot(tbl_1_1_100(:,1),tbl_1_1_100(:,2),'r-d','MarkerFaceColor',[1 0 0]);
hold on;

tbl_1_1000000_100 = dlmread('cr_vs_ac_1_1000000_100.txt');
tbl_1_1000000_100(:,2) = tbl_1_1000000_100(:,2)*100;
plot(tbl_1_1000000_100(:,1),tbl_1_1000000_100(:,2),'g-v',...
    'MarkerFaceColor', [0 1 0]);
hold on;

ylim([96.5 100]);
xlabel('call rate (%)');
ylabel('concordance rate (%)');
%set(gca, 'xdir','reverse');
hl = legend('\beta_1=1, \beta_2=10^4, \beta_3=10^2', ...
            '\beta_1=1, \beta_2=1, \beta_3=10^2', ...
            'Location', 'Best');
set(hl, 'Interpreter', 'tex');