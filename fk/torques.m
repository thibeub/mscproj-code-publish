% T. Atkins, 2024
function [tau1, tau2, tau3] = torques(finger)
    temp = finger.len;
    NUM_JOINTS = length(temp(temp ~= 0));

    h = finger.hgt;
    nxt = finger.nxt; % x4
    len = finger.len; % x3
    F_T = finger.F_T;
    F_N = finger.F_N;

    tau1 = h*(F_T(1, 2) - F_T(2, 1)) - (len(1) - nxt(2)) * (F_N(1, 2) - F_N(2, 1));
    if NUM_JOINTS == 3
        tau2 = h*(F_T(2, 2) - F_T(3, 1)) - (len(2) - nxt(3)) * (F_N(2, 2) - F_N(3, 1));
        tau3 = h* F_T(3, 2) - (len(3) - nxt(4)) * F_N(3, 2);
    else % thumb
        tau2 = h*F_T(2, 2) - (len(2) - nxt(3)) * F_N(2, 2);
        tau3 = 0;
    end
    % disp(tau1)
    % disp(tau2)
    % disp(tau3)
end