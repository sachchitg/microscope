/*
  StageDriver.ino - Firmware for the Arduino 

*/
#include <Wire.h>
#include "Stage.h"

Stage stage = Stage();

void setup() {
  // put your setup code here, to run once:
  stage.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  stage.loop();
}

void serialEvent() {
  //Attach SerialControl to the Serial event
  stage.serialEvent();
}

void serialEventRun(void){
  //Hack to fix broken IDE functionality for Due
  if(Serial.available()) serialEvent();
}

