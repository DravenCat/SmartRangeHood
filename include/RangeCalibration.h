#ifndef RSCALIBRATION_RANGECALIBRATION_H
#define RSCALIBRATION_RANGECALIBRATION_H


class RangeCalibration {

    public:
    static float calculateSpeedOfSound(float temperature, float humidity, float pressure);
    static float compensateUltrasonicDistance(float rawDistance, float temperature, float humidity, float pressure);
};


#endif //RSCALIBRATION_RANGECALIBRATION_H