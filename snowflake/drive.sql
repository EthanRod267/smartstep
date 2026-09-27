SELECT
    driver_id,
    shoe_id,
    movement_time,
    gas_pedal_pressure,
    foot_angle_y AS side_to_side_tilt,

    -- 1. Create a "Danger Flag" column using a CASE rule
    CASE
        WHEN gas_pedal_pressure >= 90.0 THEN '🔴 SLAMMED BRAKES'
        WHEN gas_pedal_pressure > 70.0 AND (foot_angle_y > 10.0 OR foot_angle_y < -10.0) THEN '⚠️ AGGRESSIVE SWERVE'
        ELSE '🟢 SAFE DRIVING'
    END AS driving_behavior

FROM (
    -- This part runs our previous query to flatten the messy MongoDB box first
    SELECT
        raw_sensor_data:sensor_id::STRING AS shoe_id,
        raw_sensor_data:driver_id::STRING AS driver_id,
        raw_sensor_data:timestamp::TIMESTAMP AS movement_time,
        raw_sensor_data:metrics.pedal_pressure_percentage::FLOAT AS gas_pedal_pressure,
        raw_sensor_data:metrics.foot_angle.roll_y::FLOAT AS foot_angle_y
    FROM my_sensor_database.public.foot_movements_table
)
-- 2. Sort it so the most dangerous events show up at the very top
ORDER BY driving_behavior DESC, movement_time DESC;

