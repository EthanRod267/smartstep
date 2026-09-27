"""
analysis.py

Turns raw sensor readings (pressure, gyro, frequency) into the metrics
the dashboard actually displays: form_rating, speed, and suggestions.

This is intentionally kept separate from app.py so the analysis logic
can be developed/tested/replaced independently of the Flask routes.

Everything in this file is PLACEHOLDER logic based on reasonable-sounding
math, not a validated biomechanics model. Replace the calculations inside
each function with whatever your team's actual analysis calls for.
"""


def compute_form_rating(pressure, gyro):
    """
    Returns a 0-100 score representing 'form quality'.

    Placeholder idea: penalize large gyro instability (jerky motion)
    and pressure far from a 'neutral' midpoint.
    Replace with your team's real scoring model.
    """
    if pressure is None or gyro is None:
        return None

    gyro_magnitude = (gyro.get("x", 0) ** 2 + gyro.get("y", 0) ** 2 + gyro.get("z", 0) ** 2) ** 0.5

    # Placeholder: assume "ideal" pressure is around 40 (kPa, arbitrary),
    # and gyro magnitude of 0 is perfectly stable.
    pressure_penalty = abs(pressure - 40) * 0.5
    stability_penalty = gyro_magnitude * 20

    score = 100 - pressure_penalty - stability_penalty
    return round(max(0, min(100, score)), 1)


def compute_speed(frequency):
    """
    Returns an estimated speed value derived from step/oscillation frequency.

    Placeholder idea: treat 'frequency' (Hz) as steps per second and
    convert to a rough speed estimate using an assumed average stride length.
    Replace with a real stride-length model or actual GPS/IMU integration.
    """
    if frequency is None:
        return None

    assumed_stride_length_m = 0.75  # placeholder average stride length
    speed_m_per_s = frequency * assumed_stride_length_m
    return round(speed_m_per_s, 2)


def generate_suggestions(form_rating, speed):
    """
    Returns a list of short human-readable coaching suggestions based on
    the computed metrics. Replace these thresholds/messages with whatever
    guidance your team actually wants to surface.
    """
    suggestions = []

    if form_rating is not None:
        if form_rating < 50:
            suggestions.append("High instability detected — check for excessive lateral motion.")
        elif form_rating < 75:
            suggestions.append("Form is decent but inconsistent — focus on steadier footstrike.")
        else:
            suggestions.append("Form looks solid — maintain current stride pattern.")

    if speed is not None:
        if speed < 1.5:
            suggestions.append("Pace is slow — consider increasing stride frequency.")
        elif speed > 4.5:
            suggestions.append("Pace is very fast — watch for form breakdown at this speed.")

    if not suggestions:
        suggestions.append("Not enough data yet to generate suggestions.")

    return suggestions


def analyze(reading):
    """
    Main entry point called from app.py.

    `reading` is the raw dict coming from the frontend:
        { "device_id": ..., "pressure": ..., "gyro": {...}, "frequency": ... }

    Returns a dict with the three computed metrics:
        { "form_rating": ..., "speed": ..., "suggestions": [...] }
    """
    pressure = reading.get("pressure")
    gyro = reading.get("gyro") or {}
    frequency = reading.get("frequency")

    form_rating = compute_form_rating(pressure, gyro)
    speed = compute_speed(frequency)
    suggestions = generate_suggestions(form_rating, speed)

    return {
        "form_rating": form_rating,
        "speed": speed,
        "suggestions": suggestions
    }
