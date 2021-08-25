/* 05.10.2020
 * The stepper goes reverse and forward with different speed.
 * The maximum speed of the current model is around 14 RPM. 
 * - 2 miliseconds delay means -> 2 * 2048 = 4096 ms for 1 rev. 
 *    60/(4096/1000) = 14.64 RPM with 2 ms delay; [measured ~=14.15 rpm forward   ~= 14.38 rpm backwards]
 * - 3 ms delay -> 3*2048 = 6144 ms for 1 rev; 
 *    60/6.144 = 9.76 RPM with 3 ms delay
*/
#include "StepperMotor.h"

#define STEP_SIZE 2048 // !!! how may steps do you need to make a full revolution

#define STEPPER_PIN_1 10
#define STEPPER_PIN_2 9
#define STEPPER_PIN_3 6
#define STEPPER_PIN_4 5



long timeVar = 0;
long prevMillis = 0;
long millisPrint = 0;

double rx=0;
double ry=0;
    
StepperMotor StepMotor; 
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
 StepMotor.initStepper(STEPPER_PIN_1, STEPPER_PIN_2,STEPPER_PIN_3,  STEPPER_PIN_4);

}
double getSignedAngle(double angle) {
  angle-=((int)angle/360)*360;
  if (angle>180)
    angle-=360;
   else if (angle<-180)
    angle+=360;
  return angle;
}
void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available() >0){
    String s = Serial.readString();
    String s1 = s.substring(0,s.indexOf(","));
    String s2 = s.substring(s.indexOf(",")+1);
    
    double az,el;
    az = s1.toDouble(); //azimuth
    el = s2.toDouble(); //elevation 
    double dx = getSignedAngle(-(rx-az));
    double dy = getSignedAngle(-(ry-el));
    StepMotor.rotateSteps(dx>0,abs(dx*STEP_SIZE/360.0),3); //direction, steps, microsspeed (3 is best)
    delay(1000);
    StepMotor.rotateSteps(dy>0,abs(dy*STEP_SIZE/360.0),3); // 1 step is 1/2048 revs
    rx=az;
    ry=el;
    Serial.print("Rx: ");
    Serial.println(rx);
    Serial.print("Ry: ");
    Serial.println(ry);
  }
}
