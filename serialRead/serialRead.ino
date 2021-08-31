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
#define STEP_DELAY 2 // fastest possible for current motor

#define RAND_BTN_PIN 19
#define MANUAL_X_PIN A6
#define MANUAL_Y_PIN A7

#define STEPPER_PIN_1 10
#define STEPPER_PIN_2 9
#define STEPPER_PIN_3 6
#define STEPPER_PIN_4 5

#define STEPPER_PIN_5 7
#define STEPPER_PIN_6 2
#define STEPPER_PIN_7 3
#define STEPPER_PIN_8 4

#define HOME_X_PIN 8 
#define HOME_Y_PIN 11
#define HOME_Y45_PIN 12

long timeVar = 0;
long prevMillis = 0;
long millisPrint = 0;

double rx=0;
double ry=0;
    
StepperMotor StepMotor1;
StepperMotor StepMotor2; 
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(HOME_X_PIN, INPUT);
pinMode(HOME_Y_PIN, INPUT);
pinMode(HOME_Y45_PIN, INPUT);
pinMode(RAND_BTN_PIN, INPUT);
pinMode(MANUAL_X_PIN, INPUT);
pinMode(MANUAL_Y_PIN, INPUT);
 StepMotor1.initStepper(STEPPER_PIN_1, STEPPER_PIN_2,STEPPER_PIN_3,  STEPPER_PIN_4);
 StepMotor2.initStepper(STEPPER_PIN_5, STEPPER_PIN_6,STEPPER_PIN_7,  STEPPER_PIN_8);

}
double getSignedAngle(double angle) {
  angle-=((int)angle/360)*360;
  if (angle>180)
    angle-=360;
   else if (angle<-180)
    angle+=360;
  return angle;
}
bool risingEdgeX = false;
bool risingEdgeY = false;
bool risingEdgeY45 = false;
bool risingEdgeRandBtn = true;
bool manualRotation = false;
void loop() {
  // put your main code here, to run repeatedly:
//  Serial.print("Rand btn: ");
//  Serial.println(digitalRead(RAND_BTN_PIN));
//  Serial.print("Manual X: ");
//  Serial.println(analogRead(MANUAL_X_PIN));
//  Serial.print("Manual Y: ");
//  Serial.println(analogRead(MANUAL_Y_PIN));

  double az,el;
  if(digitalRead(MANUAL_X_PIN)){
    StepMotor1.OneStep(true);
    delay(2);
    }
  if(digitalRead(MANUAL_Y_PIN)){
    StepMotor1.OneStep(false);
    delay(2);
    }
  
  if (Serial.available() <= 0){ return;}
  String s = Serial.readString();
  String s1 = s.substring(0,s.indexOf(","));
  String s2 = s.substring(s.indexOf(",")+1);
  
  
  az = s1.toDouble(); //azimuth
  el = s2.toDouble(); //elevation 
  double dx = getSignedAngle(-(rx-az));
  double dy = getSignedAngle(-(ry-el))*-1;
  int stepsx = abs(dx/360*STEP_SIZE);
  int stepsy = abs(dy/360*STEP_SIZE);
  int loopsize = max(stepsx,stepsy);


  
  for (int i=0; i<loopsize; i++){
    if(stepsx>0){
      stepsx--;
      StepMotor1.OneStep(dx>0);
      rx=getSignedAngle(rx+360.0/STEP_SIZE*(dx>0 ? 1 : -1 ));
    }
    if(stepsy>0){
      stepsy--;
      StepMotor2.OneStep(dy>0);  
      ry=getSignedAngle(ry + 360.0/STEP_SIZE*(dy<0 ? 1 : -1 ));
    }
    delay(STEP_DELAY);
    if(digitalRead(HOME_X_PIN) and !risingEdgeX) {
      rx=-50;
      Serial.println("Reset RX"); 
    }
    if(!digitalRead(HOME_Y_PIN) and risingEdgeY) {
      ry=20;
      dy = getSignedAngle(-(ry-el))*-1;
      stepsy = abs(dy/360*STEP_SIZE);
      Serial.println("Reset RY"); 
    }
    if(digitalRead(HOME_Y45_PIN) and !risingEdgeY45) {
      ry=45;
      Serial.println("Reset RY"); 
    }
    risingEdgeX = digitalRead(HOME_X_PIN);
    risingEdgeY = digitalRead(HOME_Y_PIN);
    risingEdgeY45 = digitalRead(HOME_Y45_PIN);
  }
 
  
  Serial.print("Rx: ");
  Serial.println(rx);
  Serial.print("Ry: ");
  Serial.println(ry);

  //end
}
