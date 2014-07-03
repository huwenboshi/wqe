tbl = dlmread('cr_vs_ac.txt');
tbl(:,2) = tbl(:,2)*100;
plot(tbl(:,1),tbl(:,2),'b.-');
ylim([98.8 100]);
xlabel('call rate (%)');
ylabel('concordance rate (%)');
set(gca, 'xdir','reverse');

