#include "StepperMotor.h"
#include <Arduino.h>


void StepperMotor::initStepper(int p1, int p2, int p3, int p4)
{
    pin1 = p1;
    pin2 = p2;
    pin3 = p3;
    pin4 = p4;
    pinMode(pin1, OUTPUT);
    pinMode(pin2, OUTPUT);
    pinMode(pin3, OUTPUT);
    pinMode(pin4, OUTPUT);
}
void StepperMotor::OneStep(bool dir)
{
    if (dir) {
        switch (step_number) {
        case 0:
            digitalWrite(pin1, HIGH);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, LOW);
            break;
        case 1:
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, HIGH);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, LOW);
            break;
        case 2:
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, HIGH);
            digitalWrite(pin4, LOW);
            break;
        case 3:
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, HIGH);
            break;
        }
    }
    else {
        switch (step_number) {
        case 0:
            digitalWrite(pin1 , LOW);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, HIGH);
            break;
        case 1:
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, HIGH);
            digitalWrite(pin4, LOW);
            break;
        case 2:
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, HIGH);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, LOW);
            break;
        case 3:
            digitalWrite(pin1, HIGH);
            digitalWrite(pin2, LOW);
            digitalWrite(pin3, LOW);
            digitalWrite(pin4, LOW);
        }
    }
    step_number++;
    if (step_number > 3) {
        step_number = 0;
    }
}


void StepperMotor::rotateSteps(bool dir, int steps, int microsecondsSpeed)
{
//  if(microsecondsSpeed>3000)// Can't be lower than 10 RPM
//    microsecondsSpeed = 3000;
//  if(microsecondsSpeed<2000) // Can't be faster than 15 RPM, because the motor will not work
//    microsecondsSpeed = 2000;

  for(int i =0; i<steps; i++)
  {
    OneStep(dir);
      delay(microsecondsSpeed);
    //  delayMicroseconds(microseondsSpeed); It doesn't work with this!
  }
}

void StepperMotor::rotateRev(bool dir, int revs, int microsecondsSpeed)
{
//  if(microsecondsSpeed>3000)// Can't be lower than 10 RPM
//    microsecondsSpeed = 3000;
//  if(microsecondsSpeed<2000) // Can't be faster than 15 RPM, because the motor will not work
//    microsecondsSpeed = 2000;

  for(int i = 0; i<revs; i++)
  {
    for(int j =0; j<STEPS_PER_REV; j++)
    {
      OneStep(dir);
      delay(2);
      //  delayMicroseconds(2000); It doesn't work with this!

    }
  }
}
