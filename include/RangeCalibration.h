#ifndef RSCALIBRATION_RANGECALIBRATION_H
#define RSCALIBRATION_RANGECALIBRATION_H

// #define USE_MODEL_4

class RangeCalibration {

    public:
    float calculateSpeedOfSound(float temperature, float humidity, float pressure);
    float compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure);

    private:
    const float speed_of_sound_default = 343.5;  // m/s
    const float temperature_default = 20.0;  // C
    const float humidity_default = 0.0;  // %
#ifndef USE_MODEL_4
    const float pressure_default = 100;   // kPa
#endif

#ifdef USE_MODEL_4
    const float pressure_default = 101;   // kPa
#endif


    // Model 1
    const float a_t = 1.779762;  // m/s/°C
    const float a_rh = -20.035801; // m/s
    const float a_p = 0.0; // m/s/kPa

#ifndef USE_MODEL_4
    // Model 3
    const float a_0 = -22.998877;  // mm
    const float a_1 = 0.000181;  // mm/ns
    const float b_0 = 0.000002;  // mm/(ns·°C)
    const float b_1 = -0.000048;  // mm/ns
    const float b_2 = 0.0;  // mm/(ns·kPa)

#endif

#ifdef USE_MODEL_4
    // Model 4
    const float a_0 = -78.312327;  // mm
    const float a_1 = 0.000130;  // mm/ns
    const float b_0 = -0.000001;  // mm/(ns·°C)
    const float b_1 = 0.000150;  // mm/ns
    const float b_2 = 0.000006;  // mm/(ns·kPa)
    const float b_3 = 6.480966;  // mm/°C
#endif

};


#endif //RSCALIBRATION_RANGECALIBRATION_H