#ifndef RSCALIBRATION_RANGECALIBRATION_H
#define RSCALIBRATION_RANGECALIBRATION_H


class RangeCalibration {

    public:
    float calculateSpeedOfSound(float temperature, float humidity, float pressure);
    float compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure);

    private:
    const float speed_of_sound_default = 343.5;
    const float temperature_default = 20.0;
};


#endif //RSCALIBRATION_RANGECALIBRATION_H