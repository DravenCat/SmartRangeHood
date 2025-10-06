#include "RangeCalibration.h"

// Function to calculate speed of sound based on T/RH/P
float RangeCalibration::calculateSpeedOfSound(float temperature, float humidity, float pressure) {
    // Calculate speed of sound in mm/s
    // Base formula: v = 331.3 + 0.606 * T (where T is in Celsius)
    // This gives speed in m/s, so we multiply by 1000 to get mm/s

    float speedOfSound = (331.3 + 0.606 * temperature) * 1000; // mm/s

    // Optional: Add humidity correction (small effect)
    // speedOfSound += (0.0124 * humidity);

    // Optional: Add pressure correction (very small effect for typical variations)
    // speedOfSound *= (pressure / 101.325); // Normalize to standard pressure

    return speedOfSound;
}

// Function to convert raw ultrasonic reading to compensated distance
float RangeCalibration::compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure) {
    // Convert the raw distance back to time of flight
    float timeOfFlight_ns = (rawDistance * 2.0) / 343500.0 * 1e9; // Convert to nanoseconds

    // Calculate actual speed of sound
    float actualSpeed = calculateSpeedOfSound(temperature, humidity, pressure);

    // Calculate compensated distance using actual speed of sound
    float compensatedDistance = (timeOfFlight_ns * 1e-9) * actualSpeed / 2.0;

    return compensatedDistance;
}
