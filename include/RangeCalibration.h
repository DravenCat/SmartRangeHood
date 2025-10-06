#ifndef RSCALIBRATION_RANGECALIBRATION_H
#define RSCALIBRATION_RANGECALIBRATION_H


class RangeCalibration {

    public:
    float calculateSpeedOfSound(float temperature, float humidity, float pressure);
    float compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure);

    private:
    const float speed_of_sound_default = 331.45;  // m/s
    const float temperature_default = 20.0;  // C
    const float humidity_default = 0.0;  // %
    const float pressure_default = 101.325;   // kPa

};


#endif //RSCALIBRATION_RANGECALIBRATION_H