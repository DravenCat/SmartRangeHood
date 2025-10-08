#ifndef RSCALIBRATION_RANGECALIBRATION_H
#define RSCALIBRATION_RANGECALIBRATION_H


class RangeCalibration {

    public:
    float calculateSpeedOfSound(float temperature, float humidity, float pressure);
    float compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure);

    private:
    const float speed_of_sound_default = 343.5;  // m/s
    const float temperature_default = 20.0;  // C
    const float humidity_default = 0.0;  // %
    const float pressure_default = 100;   // kPa

    // Model 1
    const float a_t = 1.779762;  // m/s/°C
    const float a_rh = -20.035801; // m/s
    const float a_p = 0.0; // m/s/kPa

    // Model 3
    const float a_0 = -77.576344;  // mm
    const float a_1 = 0.000266;  // mm/ns
    const float b_0 = -0.000003;  // mm/(ns·°C)
    const float b_1 = -0.000136;  // mm/ns
    const float b_2 = 0.0;  // mm/(ns·kPa)
    const float b_3 = 6.535015;  // mm/°C

};


#endif //RSCALIBRATION_RANGECALIBRATION_H