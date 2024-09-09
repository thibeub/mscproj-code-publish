% T. Atkins, 2024

%% Store hand dims (below are incomplete (marked by 'TODO') dummy values - ILLUSTRATIVE ONLY)
real_hand.index.force = 10.*ones(1, 3); % TODO
real_hand.index.hgt = 8; % pin height above phalange [mm] (assumed equal for all fingers)
real_hand.index.nxt = [24.7, 46.25/2, 24.30/2, 23.64/2]; % pin distance (along phalange) to next joint (or finger tip) [mm]
real_hand.index.len = [46.25, 24.30, 25.18]; % phalange length (1st value is dummy) [mm]
real_hand.index.theta = deg2rad([90, 95, 80]);

real_hand.middle.force = 10.*ones(1, 3); % TODO
real_hand.middle.hgt = 8;
real_hand.middle.nxt = [30.50, 48.64/2, 27.74/2, 24.50/2];
real_hand.middle.len = [48.64, 27.74, 26.69];
real_hand.middle.theta = deg2rad([90, 95, 80]);

real_hand.thumb.force = 10.*ones(1, 3); % TODO
real_hand.thumb.hgt = 8;
real_hand.thumb.nxt = [34.37, 32.63/2, 30.74/2, 0];
real_hand.thumb.len = [32.63, 30.74, 0];
real_hand.thumb.theta = deg2rad([80, 90, 0]);

real_hand.ring.force = 10.*ones(1, 3); % TODO
real_hand.ring.hgt = 8;
real_hand.ring.nxt = [26.90, 25.87/2, 26.78/2, 24.50/2];
real_hand.ring.len = [25.87, 26.78, 24.50];
real_hand.ring.theta = deg2rad([90, 95, 80]);

real_hand.little.force = 10.*ones(1,3); % TODO
real_hand.little.hgt = 8;
real_hand.little.nxt = [19.35, 25.87/2, 26.78/2, 24.50/2];
real_hand.little.len = [25.87, 26.78, 24.50];
real_hand.little.theta = deg2rad([90, 95, 80]);

hand_select = real_hand; % real_hand or dummy_hand

%% Compute FK and forces
for finger = ["thumb", "index", "middle", "ring", "little"]
    temp = hand_select.(finger).len;
    NUM_JOINTS = length(temp(temp ~= 0));
    
    % Geometry
    for joint = 1:NUM_JOINTS
        [hand_select.(finger).F_T(joint, 1), hand_select.(finger).F_T(joint, ...
            2), hand_select.(finger).F_N(joint, 1), hand_select.(finger).F_N(joint, 2)] = geometry(hand_select.(finger), joint);
    end

    % Torques
    [hand_select.(finger).torque(1), hand_select.(finger).torque(2 ...
        ), hand_select.(finger).torque(3)] = torques(hand_select.(finger));

    % Jacobian
    hand_select.(finger).jacobian = jacobian(hand_select.(finger));

    % Forces in base frame
    hand_select.(finger).F_ee = linsolve(hand_select.(finger).jacobian.', hand_select.(finger).torque.');
    disp(hand_select.(finger).F_ee(1:2))

    % Compute tip force (i.e. EE force component normal to link 3 / distal phalange)
    hand_select.(finger).Ftip = tip_force(hand_select.(finger));
    disp(hand_select.(finger).Ftip)
    disp("---")
end