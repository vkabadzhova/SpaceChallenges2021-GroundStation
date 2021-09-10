//#define STEPS_PER_REV 2070 // 2048; For model "28BYJ-48"
#define STEPS_PER_REV 4076 // 2048; For model "28BYJ-48"

class StepperMotor
{
  public:
    int pin1, pin2, pin3, pin4;
    void initStepper(int p1, int p2, int p3, int p4); // initializes the stepper motor; 4 digital pins
    void OneStep(bool dir); // the stepper moves one step(1/2048); true or false for direction
    void rotateSteps(bool dir, int steps, int microsecondsSpeed); // the stepper moves N amount of steps, when microseconds are 2000 ~= 15RPM; 3000 microseconds = 10 RPM
    void rotateRev(bool dir, int revs, int microsecondsSpeed); // the stepper makes full rotation
  private:
    int step_number = 0;
};
