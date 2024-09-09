% T. Atkins, 2024
% Calculate the force components (normal and tangential) for a SINGLE joint (i.e. two phalanges)

function [F_T1, F_T2, F_N1, F_N2] = geometry(finger, joint)
    if ~isstruct(finger)
        error("Input 'finger' must be a struct.")
    end

    if ~ismember(joint, [1,2,3])
        error("Input 'joint' must be 1, 2 or 3.")
    end

    %% Step 0: Setup variables
    x = finger.nxt(joint);
    y = finger.len(joint)-finger.nxt(joint+1);

    h = finger.hgt;

    theta = finger.theta(joint);

    F = finger.force(joint);

    %% Step 1
    k = sqrt(x^2 + y^2 - 2 * x * y * cos(pi - theta));

    %% Step 2
    p = y * sin(theta);

    %% Step 3
    epsilon = asin(p / k);

    %% Step 4
    gamma = pi - epsilon;

    %% Step 5
    r = h * cos(theta);
    e = p - r;

    %% Step 6: Quadrilateral calculation --> pin spacing (d)
    % Calculate pin 1 (proximal) Cartesian coordinates
    p1_angle = pi / 2 - epsilon;
    p1_x = k + h * cos(p1_angle);
    p1_y = h * sin(p1_angle);

    % Calculate pin 2 (distal) Cartesian coordinates
    p2_angle = pi / 2 - gamma;
    p2_x = -h * cos(p2_angle);
    p2_y = h * sin(p2_angle);

    % Compute d (Euclidean distance)
    d = sqrt((p2_x-p1_x)^2 + (p2_y-p1_y)^2);

    %% Step 7
    lambda = asin((e + h) / d);

    %% Step 8
    alpha = theta - lambda;

    %% Step 9: Distal forces (2)
    beta = (pi / 2) - alpha;
    F_T2 = F * sin(beta);
    F_N2 = F * cos(beta);

    %% Step 10: Proximal forces (1)
    sigma = (pi / 2) - lambda;
    F_T1 = F * sin(sigma);
    F_N1 = F * cos(sigma);

end