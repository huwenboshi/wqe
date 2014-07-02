function [maa, vaa, mab, vab, mbb, vbb] = gauss_est(paa, pab, pbb)
    maa = mean(paa);
    maa = maa';
    vaa = cov(paa);
    
    mab = mean(pab);
    mab = mab';
    vab = cov(pab);
    
    mbb = mean(pbb);
    mbb = mbb';
    vbb = cov(pbb);
end