% T. Atkins
function Ftip = tip_force(finger)
    rho = sum(finger.theta);
    mu = -pi/2 + rho;
    xi = pi - rho;

    Fx = finger.F_ee(1);
    Fy = finger.F_ee(2);

    % x component
    Ftip_x = Fx / cos(mu);

    % y component
    Ftip_y = Fy * cos(xi);

    % Total
    Ftip = sqrt(Ftip_x^2 + Ftip_y^2);
end