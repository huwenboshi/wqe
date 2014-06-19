msdata = dlmread('maxsep_maf_result.txt');
mvdata = dlmread('minvol_maf_result.txt');
rbdata = dlmread('robsep_maf_result.txt');

msavg = zeros(50,1);
mvavg = zeros(50,1);
mscnt = zeros(50,1);
mvcnt = zeros(50,1);
rbavg = zeros(50,1);
rbcnt = zeros(50,1);
freq = linspace(0,0.5,50);

nms = size(msdata,1);
for i=1:nms
    idx = floor(msdata(i,1)*100);
    if(idx == 0)
        idx = idx + 1;
    end
    mscnt(idx) = mscnt(idx) + 1;
    msavg(idx) = msavg(idx)+msdata(i,2);
end
msavg = msavg./mscnt;

nmv = size(mvdata,1);
for i=1:nmv
    idx = ceil(msdata(i,1)*100);
    if(idx == 0)
        idx = idx + 1;
    end
    mvcnt(idx) = mvcnt(idx) + 1;
    mvavg(idx) = mvavg(idx)+mvdata(i,2);
end
mvavg = mvavg./mvcnt;

nrb = size(rbdata,1);
for i=1:nrb
    idx = ceil(rbdata(i,1)*100);
    if(idx == 0)
        idx = idx + 1;
    end
    rbcnt(idx) = rbcnt(idx) + 1;
    rbavg(idx) = rbavg(idx)+rbdata(i,2);
end
rbavg = rbavg./rbcnt;

figure;

plot(freq,msavg,'r-'); 
hold on;
plot(freq,mvavg,'b-')
hold on;
plot(freq,rbavg,'k-')
hold on;
legend ('MAXSEP','MINVOL','COMB','location', 'east');
hold on;

plot(freq,msavg,'r*')
hold on;
plot(freq,mvavg,'b*')
hold on;
plot(freq,rbavg,'k*')
hold on;
xlabel('minor allele frequency', 'fontsize', 15)
ylabel('accuracy', 'fontsize', 15)
