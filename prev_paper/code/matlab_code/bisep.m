function [c1, E1, c2, E2] = bisep(pa, pb)
    dim = size(pa, 1);
    num_pa = size(pa, 2);
    num_pb = size(pb, 2);
    
    pah = zeros(dim+1, num_pa);
    pah(1,:) = ones(1,num_pa);
    pah(2:end,:) = pa;
    
    pbh = zeros(dim+1, num_pb);
    pbh(1,:) = ones(1, num_pb);
    pbh(2:end,:) = pb;
    
    E1_hat = [];
    E2_hat = [];
    cvx_begin sdp
        variable E1_hat(dim+1,dim+1)
        variable E2_hat(dim+1,dim+1)
        variable rho1(1)
        variable rho2(1)
        variable rho3(1)
        variable rho4(1)
        
        minimize abs(rho1)-1+abs(rho2)-1+rho3+rho4
        subject to
            for i = 1:num_pa
                pah(:,i)'*E1_hat*pah(:,i) <= rho1
                pah(:,i)'*E2_hat*pah(:,i) >= rho2
            end
            for i = 1:num_pb
                pbh(:,i)'*E2_hat*pbh(:,i) <= rho3
                pbh(:,i)'*E1_hat*pbh(:,i) >= rho4
            end
            E1_hat == semidefinite(dim+1)
            E2_hat == semidefinite(dim+1)
    cvx_end
    
    F1 = E1_hat(2:end,2:end);
    v1 = E1_hat(2:end, 1);
    s1 = E1_hat(1, 1);
    c1 = -F1\v1;
    E1 = F1 ./ (1-(s1-c1'*F1*c1));
    
    F2 = E2_hat(2:end,2:end);
    v2 = E2_hat(2:end, 1);
    s2 = E2_hat(1, 1);
    c2 = -F2\v2;
    E2 = F2 ./ (1-(s2-c2'*F2*c2));
end