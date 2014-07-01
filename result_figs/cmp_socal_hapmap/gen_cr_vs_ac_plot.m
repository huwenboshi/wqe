tbl = dlmread('cr_vs_ac.txt');
data = tbl(:,2);
figure;
bar(data);
ylim([0.985 1.0]);
xlabel('call rate (%)');
ylabel('concordance rate (%)');
set(gca, 'XTickLabel', {'100','95','90','85','80','75','70','65','60',...
                        '55','50'});

%plot(tbl(:,1),tbl(:,2));