% T. Atkins
function J = jacobian(finger)
    % temp = finger.len;
    % NUM_JOINTS = length(temp(temp ~= 0));
    
    [L1, L2, L3] = struct("tmp", num2cell(finger.len)).tmp;
    [t1, t2, t3] = struct("tmp", num2cell(finger.theta)).tmp;

    J = [[-L1*sin(t1)-L2*sin(t1+t2)-L3*sin(t1+t2+t3),-L2*sin(t1+t2)-L3*sin(t1+t2+t3),-L3*sin(t1+t2+t3 ...
        )];[L1*cos(t1)+L2*cos(t1+t2)+L3*cos(t1+t2+t3),L2*cos(t1+t2)+L3*cos(t1+t2+t3),L3*cos(t1+t2+t3)];[1,1,1]];
end