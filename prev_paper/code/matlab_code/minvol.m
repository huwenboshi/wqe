function [c, E] = minvol(pa)
    dim = size(pa, 1);
    num_pa = size(pa, 2);
    
    pah = zeros(dim+1, num_pa);
    pah(1,:) = ones(1,num_pa);
    pah(2:end,:) = pa;
    
    E_hat = [];
    cvx_begin sdp
        variable E_hat(dim+1,dim+1)
        variable T(dim, dim)
        
        minimize trace(T)
        subject to
            for i = 1:num_pa
                pah(:,i)'*E_hat*pah(:,i) <= 1
            end
            E_hat == semidefinite(dim+1)
            [E_hat(2:end, 2:end) eye(dim, dim);
             eye(dim, dim) T] == semidefinite(2*dim)
    cvx_end
    
    F = E_hat(2:end,2:end);
    v = E_hat(2:end, 1);
    s = E_hat(1, 1);
    c = -F\v;
    E = F ./ (1-(s-c'*F*c));
end