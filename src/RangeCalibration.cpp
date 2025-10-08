#include "RangeCalibration.h"

#define USE_DISTANCE_MODEL true
// #define USE_MODEL_1 1


// Function to calculate speed of sound based on T/RH/P
float RangeCalibration::calculateSpeedOfSound(float temperature, float humidity, float pressure) {
    // Calculate speed of sound in mm/s
    // Base formula: v = 331.3 + 0.606 * T (where T is in Celsius)
    // This gives speed in m/s, so we multiply by 1000 to get mm/s

    // float speedOfSound = (speed_of_sound_default + 0.606 * temperature) * 1000; // mm/s

    float speedOfSound = speed_of_sound_default;
    speedOfSound += (a_t * (temperature - temperature_default));
    speedOfSound += (a_rh * (humidity - humidity_default));
    speedOfSound += (a_p * (pressure - pressure_default));
    speedOfSound *= 1000;

    return speedOfSound;  // return mm/s
}

// Function to convert raw ultrasonic reading to compensated distance
float RangeCalibration::compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure) {
    // Convert the raw distance back to time of flight
    float timeOfFlight_ns = (rawDistance * 2.0) / 343500.0 * 1e9; // Convert to nanoseconds
    float delta_t = temperature - temperature_default;
    float delta_rh = humidity - humidity_default;
    float delta_p = pressure - pressure_default;

    // Calculate actual speed of sound
    float actualSpeed = calculateSpeedOfSound(temperature, humidity, pressure);

    // Calculate compensated distance using actual speed of sound
    float compensatedDistance = 0;
    if (!USE_DISTANCE_MODEL) {
        compensatedDistance = (timeOfFlight_ns * 1e-9) * actualSpeed / 2.0;
    }
    if (USE_DISTANCE_MODEL) {
        compensatedDistance = a_0 + a_1 * timeOfFlight_ns;
        compensatedDistance += b_0 * delta_t * timeOfFlight_ns;
        compensatedDistance += b_1 * delta_rh * timeOfFlight_ns / 100;
        compensatedDistance += b_2 * delta_p * timeOfFlight_ns;
        compensatedDistance += b_3 * delta_t;
    }

    return compensatedDistance; // return mm
}
