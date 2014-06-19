function [c, E, rho] = maxsep(pa, pb)
    dim = size(pa, 1);
    num_pa = size(pa, 2);
    num_pb = size(pb, 2);
    
    pah = zeros(dim+1, num_pa);
    pah(1,:) = ones(1,num_pa);
    pah(2:end,:) = pa;
    
    pbh = zeros(dim+1, num_pb);
    pbh(1,:) = ones(1, num_pb);
    pbh(2:end,:) = pb;
    
    E_hat = [];
    cvx_begin sdp
        variable E_hat(dim+1,dim+1)
        variable k(1)
        
        minimize -k
        subject to
            for i = 1:num_pa
                pah(:,i)'*E_hat*pah(:,i) <= 1
            end
            for i = 1:num_pb
                pbh(:,i)'*E_hat*pbh(:,i) >= k
            end
            E_hat == semidefinite(dim+1)
    cvx_end
    
    F = E_hat(2:end,2:end);
    v = E_hat(2:end, 1);
    s = E_hat(1, 1);
    c = -F\v;
    E = F ./ (1-(s-c'*F*c));
    rho = k;
end