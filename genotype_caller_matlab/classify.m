function class = classify(E_aa, c_aa, E_ab, c_ab, E_bb, c_bb, x)
%CLASSIFY Summary of this function goes here
%   Detailed explanation goes here
    daa = ellipse_dist(E_aa, c_aa, x);
    dab = ellipse_dist(E_ab, c_ab, x);
    dbb = ellipse_dist(E_bb, c_bb, x);
    [val,class] = min([daa;dab;dbb]);
end

