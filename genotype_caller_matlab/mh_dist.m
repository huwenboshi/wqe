function dist = mh_dist(m, v, x)
%ELLIPSE_DIST Summary of this function goes here
%   Detailed explanation goes here
    dist = sqrt((x-m)'*v*(x-m));
end

