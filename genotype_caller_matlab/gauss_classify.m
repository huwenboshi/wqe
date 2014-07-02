function class = gauss_classify(m_aa, v_aa, m_ab, v_ab, m_bb, v_bb, x)
%CLASSIFY Summary of this function goes here
%   Detailed explanation goes here
    daa = mh_dist(m_aa, v_aa, x);
    dab = mh_dist(m_ab, v_ab, x);
    dbb = mh_dist(m_bb, v_bb, x);
    [val,class] = min([daa;dab;dbb]);
end

