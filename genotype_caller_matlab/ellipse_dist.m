function dist = ellipse_dist(E, c, x)
%ELLIPSE_DIST Summary of this function goes here
%   Detailed explanation goes here
    dist = sqrt((x-c)'*E*(x-c));
end

