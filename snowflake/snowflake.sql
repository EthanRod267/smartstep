SELECT
    -- 1. Grab normal, top-level data
    raw_sensor_data:sensor_id::STRING AS shoe_id,
    raw_sensor_data:driver_id::STRING AS driver_id,
    raw_sensor_data:timestamp::TIMESTAMP AS movement_time,

    -- 2. Reach deeper to grab the pedal pressure
    raw_sensor_data:metrics.pedal_pressure_percentage::FLOAT AS gas_pedal_pressure,

    -- 3. Reach into the nested "foot_angle" branch to pull out X, Y, and Z
    raw_sensor_data:metrics.foot_angle.pitch_x::FLOAT AS foot_angle_x,
    raw_sensor_data:metrics.foot_angle.roll_y::FLOAT AS foot_angle_y,
    raw_sensor_data:metrics.foot_angle.yaw_z::FLOAT AS foot_angle_z

FROM my_sensor_database.public.foot_movements_table;
