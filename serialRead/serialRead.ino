/* 05.10.2020
 * The stepper goes reverse and forward with different speed.
 * The maximum speed of the current model is around 14 RPM. 
 * - 2 miliseconds delay means -> 2 * 2048 = 4096 ms for 1 rev. 
 *    60/(4096/1000) = 14.64 RPM with 2 ms delay; [measured ~=14.15 rpm forward   ~= 14.38 rpm backwards]
 * - 3 ms delay -> 3*2048 = 6144 ms for 1 rev; 
 *    60/6.144 = 9.76 RPM with 3 ms delay
*/
#include "StepperMotor.h"

#define STEPPER_PIN_1 10
#define STEPPER_PIN_2 9
#define STEPPER_PIN_3 6
#define STEPPER_PIN_4 5

long timeVar = 0;
long prevMillis = 0;
long millisPrint = 0;
    
StepperMotor StepMotor; 
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
 StepMotor.initStepper(STEPPER_PIN_1, STEPPER_PIN_2,STEPPER_PIN_3,  STEPPER_PIN_4);

}
double az = 0;
double el = 0;
bool azimuthdone = false;
void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() >0){
//    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//    delay(1000);                       // wait for a second
//    digitalWrite(LED_BUILTIN, LOW);
    String s = Serial.readString();
    String s1 = s.substring(0,s.indexOf(","));
    String s2 = s.substring(s.indexOf(",")+1);
    az = s1.toDouble(); //azimuth
    el = s2.toDouble(); //elevation
    Serial.print("az: ");
    Serial.println(az);
    Serial.print("el: ");
    Serial.println(el);
    // The code belows rotates the servo 2 times with the maximum speed(2ms between step)
    // then it rotates reverse with same speed
  /*
  StepMotor.rotateSteps(true, 1024, 4);
  delay(2000);
  */
   
    
   
    }
    
    if(abs(az)>0){
    az-=11.0/64*(az>0?1:-1);
    StepMotor.rotateSteps(az>0,1,4);
    delay(1);
   }
   else if (abs(el)>0) {
    if (!azimuthdone){
      delay(1000);
      azimuthdone=true;
    }
    el-=11.0/64*(el>0?1:-1);
    StepMotor.rotateSteps(el>0,1,4);
    delay(1);
   }
}
