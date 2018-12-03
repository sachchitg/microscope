/*
  Stage.cpp - Library for controlling the stage of microscope
*/
#include "Arduino.h"
#include "Stage.h"
#include <kissStepper.h>

Stage::Stage() {
  calibrated = false;
  begin_calibration = false;
  calibration_x = false;
  calibration_y = false;
  calibration_z = false;

  string_complete = false;
  input_string = (char *)malloc(MAX_LENGTH);
  str_pos = 0;
}

void Stage::begin()
{
  Serial.begin(9600);

  mot_X = new kissStepper(kissPinAssignments(10, 9),kissMicrostepConfig(MICROSTEP_8));
  mot_Y = new kissStepper(kissPinAssignments(11, 3),kissMicrostepConfig(MICROSTEP_8));
  mot_Z = new kissStepper(kissPinAssignments(6, 5),kissMicrostepConfig(MICROSTEP_128));
  
  mot_X->begin(MICROSTEP_8, 200);
  mot_Y->begin(MICROSTEP_8, 200);
  mot_Z->begin(MICROSTEP_128, 200);

  _x_interval = 15;
  _y_interval = 15;
  _z_interval = 15;
  _print_interval = 5000;

  resetMotor(mot_X, MICROSTEP_8);
  resetMotor(mot_Y, MICROSTEP_8);
  resetMotor(mot_Z, MICROSTEP_128);

  _x_pos = mot_X->getPos();
  _y_pos = mot_Y->getPos();
  _z_pos = mot_Z->getPos();

  _x_factor = 1;
  _y_factor = 1;
  _z_factor = 1;

  _x_target = 0;
  _y_target = 0;
  _z_target = 0;

  Serial.println("Microscope controller Firmware v0.1.11");
}

void Stage::resetMotor(kissStepper* mot, uint8_t mode)
{
    delay(100);
    mot->stop();
    mot->setAccel(0);
    mot->setMaxSpeed(200);
    mot->setDriveMode((driveMode_t)mode);
    mot->moveTo(0);
    while (mot->work());
    delay(100);
}

void Stage::loop()
{
  // Handle calibration event
  if(begin_calibration){
     do_calibrate();
  }
  else
  {
    // Check limits in each direction - if required stop motor
    // Otherwise move one step
    if((millis() -_z_last_step) > _z_interval)
    {
        update(mot_Z, _z_target, _z_factor);
        _z_last_step = millis();
        _z_pos = mot_Z->getPos();
    }
    if((millis() -_x_last_step) > _x_interval)
    {
        update(mot_X, _x_target, _x_factor);
        _x_last_step = millis();
        _x_pos = mot_X->getPos();
    }
    if((millis()-_y_last_step) > _y_interval)
    {
        update(mot_Y, _y_target, _y_factor);
        _y_last_step = millis();
        _y_pos = mot_Y->getPos();
    }
  }

//  if((millis() -_print_last_step) > _print_interval){
//    _print_last_step = millis();
//    Serial.print("X: ");
//    Serial.print(String(mot_X->getPos()));
//    Serial.print(", Y: ");
//    Serial.print(String(mot_Y->getPos()));
//    Serial.print(", Z: ");
//    Serial.println(String(mot_Z->getPos()));
//  }
}

void Stage::update(kissStepper* mot, int32_t targetPos, int32_t factor)
{
   int32_t currPos = mot->getPos();
   
   if(currPos <= mot->reverseLimit) {
      mot->stop();
   }
   else if(currPos >= mot->forwardLimit)
   {
        mot->stop();
   }
   else
   {
      if(targetPos - currPos > 0)
     { 
        mot->moveTo(currPos+mot->fullStepVal/factor);
        while (mot->work());
     }
      if(targetPos - currPos < 0)
      {
        mot->moveTo(currPos-mot->fullStepVal/factor);
        while (mot->work());
      }
   }
}


// Start is assumed (0,0), and it is upper left corner 
//  (0,0)--------->---------------------A
//  |                                   |
//  |                                   V
//  |                                   |
//  |                                   |
//  ------------------------------------B
// Move in x direction forward till user marks end by keypress
// Move in y direction forward till user marks end by keypress
// This will be position A and then B respectively.
// For Z: Fixed for 40X. Take start position as 0 and move down
void Stage::do_calibrate()
{
  
  if(calibration_z)
  {
    if((millis() -_z_last_step) > _z_interval)
    {
        _z_pos = mot_Z->getPos();
        mot_Z->moveTo(_z_pos+mot_Z->fullStepVal);
        while (mot_Z->work());
        _z_last_step = millis();
        _z_pos = mot_Z->getPos();
    }
  }
  else if(calibration_x)
  {
    if((millis() -_x_last_step) > _x_interval)
    {
        _x_pos = mot_X->getPos();
        mot_X->moveTo(_x_pos+mot_X->fullStepVal);
        while (mot_X->work());
        _x_last_step = millis();
        _x_pos = mot_X->getPos();
    }
  }
  else if(calibration_y)
  {
    if((millis()-_y_last_step) > _y_interval)
    {
        _y_pos = mot_Y->getPos();
        mot_Y->moveTo(_y_pos+mot_Y->fullStepVal);
        while (mot_Y->work());
        _y_last_step = millis();
        _y_pos = mot_Y->getPos();
    }
  }else{}
}

void Stage::calibrate()
{ 
  Serial.println("OK");
  begin_calibration = true;
  calibration_x = true;
  calibration_y = false;
  calibration_z = false;
}

void Stage::markCalibrated()
{ 
  calibrated = true;
  MoveTo(X_STEPPER,0);
  MoveTo(Y_STEPPER,0);
  MoveTo(Z_STEPPER,0);
}

int32_t Stage::getPosition(int stepper)
{
  if(calibrated)
  {
    switch(stepper) {
      case X_STEPPER:
        _x_pos = mot_X->getPos();
        return _x_pos;
        break;
      case Y_STEPPER:
        _y_pos = mot_Y->getPos();
        return _y_pos;
        break;
      case Z_STEPPER:
        _z_pos = mot_Z->getPos();
        return _z_pos;
        break;
    }
  }
}

int32_t Stage::getMoveState(int stepper)
{
  switch(stepper) {
    case X_STEPPER:
      return (int32_t)mot_X->getMoveState();
      break;
    case Y_STEPPER:
      return (int32_t)mot_Y->getMoveState();
      break;
    case Z_STEPPER:
      return (int32_t)mot_Z->getMoveState();
      break;
  }
}

int32_t Stage::getDistanceToGo(int stepper)
{
  switch(stepper) {
    case X_STEPPER:
      _x_pos = mot_X->getPos();
      return _x_target - _x_pos;
      break;
    case Y_STEPPER:;
      _y_pos = mot_Y->getPos();
      return _y_target - _y_pos;
      break;
    case Z_STEPPER:
      _z_pos = mot_Z->getPos();
      return _z_target - _z_pos;
      break;
  }
}

int32_t Stage::getLength(int stepper)
{
  switch(stepper) {
    case X_STEPPER:
      return _x_length;
      break;
    case Y_STEPPER:
      return _y_length;
      break;
    case Z_STEPPER:
      return _z_length;
      break;
  }
}

void Stage::setLength(int stepper, int32_t length)
{
  switch(stepper) {
    case X_STEPPER:
      _x_length = length;
      break;
    case Y_STEPPER:
      _y_length = length;
      break;
    case Z_STEPPER:
      _z_length = length;
      break;
  }
}

void Stage::setFactor(int stepper, int32_t factor)
{
  switch(stepper) {
    case X_STEPPER:
      _x_factor = factor;
      break;
    case Y_STEPPER:
      _y_factor = factor;
      break;
    case Z_STEPPER:
      _z_factor = factor;
      break;
  }
}

void Stage::Move(int stepper, int32_t steps)
{
  switch(stepper) {
    case X_STEPPER:
      _x_pos = mot_X->getPos();
      _x_target = _x_pos + steps*mot_X->fullStepVal/_x_factor;
      break;
    case Y_STEPPER:
      _y_pos = mot_Y->getPos();
      _y_target = _y_pos + steps*mot_Y->fullStepVal/_y_factor;
      break;
    case Z_STEPPER:
      _z_pos = mot_Z->getPos();
      _z_target = _z_pos + steps*mot_Z->fullStepVal/_z_factor;
      break;
  }
}

void Stage::MoveTo(int stepper, int32_t position)
{
  if(calibrated){
    switch(stepper) {
      case X_STEPPER:
        _x_target = int32_t(position/mot_X->fullStepVal)*mot_X->fullStepVal;
        break;
      case Y_STEPPER:
        _y_target = int32_t(position/mot_Y->fullStepVal)*mot_Y->fullStepVal;
        break;
      case Z_STEPPER:
        _z_target = int32_t(position/mot_Z->fullStepVal)*mot_Z->fullStepVal;
        break;
    }
  }
}

void Stage::setMode(int stepper, uint8_t mode)
{
  switch(stepper) {
    case X_STEPPER:
      setMotorDriveMode(mot_X, mode);
      break;
    case Y_STEPPER:
      setMotorDriveMode(mot_Y, mode);
      break;
    case Z_STEPPER:
      setMotorDriveMode(mot_Z, mode);
      break;
  }
}

void Stage::setMotorDriveMode(kissStepper* mot, uint8_t mode)
{
    switch(mode)
    {
    case 1:
        mot->setDriveMode(FULL_STEP);
        break;
    case 2:
        mot->setDriveMode(HALF_STEP);
        break;
    case 4:
        mot->setDriveMode(MICROSTEP_4);
        break;
    case 8:
        mot->setDriveMode(MICROSTEP_8);
        break;
    case 16:
        mot->setDriveMode(MICROSTEP_16);
        break;
    case 32:
        mot->setDriveMode(MICROSTEP_32);
        break;
    case 64:
        mot->setDriveMode(MICROSTEP_64);
        break;
    case 128:
        mot->setDriveMode(MICROSTEP_128);
        break;
    }
}

void Stage::serialEvent()
{
  while (Serial.available()) {
    // get the new byte:
    char in_char = (char)Serial.read(); 
    // add it to the inputString:
    if ((str_pos<MAX_LENGTH) && (in_char!='\n'))
    {
      input_string[str_pos] = in_char;
      str_pos++;
    }
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (in_char == '\n') {
      string_complete = true;
      // End a string with a null
      if (str_pos<MAX_LENGTH)
        input_string[str_pos]='\0';
      else
        input_string[MAX_LENGTH-1]='\0';
      str_pos = 0;
      processString();
    }
  }
}

void Stage::processString(){
  
  //Split received string into command and argument
  command = input_string;
  arg = input_string;

  for (int i=0; i<MAX_LENGTH; i++)
  {
    if (input_string[i]=='\0')
      break;
    if (input_string[i]==' ')
    {
      input_string[i] = '\0';
      arg++;
      break;
    }
    arg++;
  }
  // Handle event if any
  if (string_complete) {
    if(begin_calibration)
    {
      if(calibration_x)
      {
        //Stop X motor and set X limit
        mot_X->stop();
        _x_pos = mot_X->getPos();
        _x_length = _x_pos;
        calibration_x = false;
        calibration_y = true;
        calibration_z = false;
      }
      else if(calibration_y)
      {
        //Stop Y motor and set Y limit
        mot_Y->stop();
        _y_pos = mot_Y->getPos();
        _y_length = _y_pos;
        calibration_x = false;
        calibration_y = false;
        calibration_z = true;
      }
      else
      {
        //Stop Z motor and set Z limit
        mot_Z->stop();
        _z_pos = mot_Z->getPos();
        _z_length = _z_pos + Z_DELTA;
        calibration_x = false;
        calibration_y = false;
        calibration_z = false;
        begin_calibration = false;
        calibrated = true;
        MoveTo(X_STEPPER,0);
        MoveTo(Y_STEPPER,0);
        MoveTo(Z_STEPPER,0);
      }
    }
    else
    {
      //Handle commands for movement other than Calibration
      handleCommand(command,arg);
    }
    // Reset input str
    string_complete = false;
  }
}

void Stage::handleCommand(char* cmd, char* arg)
{
  String cmdString = String(cmd); //Convert to string for endsWith functions
  //Get the axis for stepper commands
  char axisC = cmdString.charAt(0);
  int axis;
  switch(axisC) {
    case 'x':
      axis = X_STEPPER;
      break;
    case 'y':
      axis = Y_STEPPER;
      break;
    case 'z':
      axis = Z_STEPPER;
      break;
  }  
  
  if (cmdString.endsWith("_move"))
  {
    //Relative move
    int32_t steps = atol(arg);
    Move(axis, steps);
    Serial.println("OK");
  }
  else if(cmdString.endsWith("_move_to"))
  {
    //Absolute move
    if(calibrated)
    {
 
      int32_t position = atol(arg);
      //Check position is in range
      if(position>=0 && position<=getLength(axis))
      {
        MoveTo(axis, position);
        Serial.println("OK");
      }
      else
      {
        Serial.println("ERR: POSITION OUT OF RANGE");
      }
    }
    else
    {
      Serial.println("ERR: NOT CALIBRATED");
    }
  }
  else if(cmdString.endsWith("calibrate"))
  {
    //Calibrate the stage
    calibrate();
  }
  else if(cmdString.endsWith("_get_length"))
  {
    //Return length if calibrated
    if(calibrated)
    {
      Serial.print("RETURN:");
      Serial.println(getLength(axis));
      Serial.println("OK");
    }
    else
    {
      Serial.println("ERR: NOT CALIBRATED");
    }
  }
  else if(cmdString.endsWith("_get_position"))
  {
    if(calibrated)
    {
      Serial.print("RETURN:");
      Serial.println(getPosition(axis));
      Serial.println("OK");
    }
    else
    {
      Serial.println("ERR: NOT CALIBRATED");
    }
  }
  else if(cmdString.endsWith("_get_distance_to_go"))
  {
    Serial.print("RETURN:");
    Serial.println(getDistanceToGo(axis));  
    Serial.println("OK");  
  }
  else if(cmdString.endsWith("_get_state"))
  {
    Serial.print("RETURN:");
    Serial.println(getMoveState(axis));  
    Serial.println("OK"); 
  }
  else if(strcmp("is_calibrated", cmd)==0)
  {
    Serial.print("RETURN:");
    Serial.println(calibrated);
    Serial.println("OK");
  }
  else if(cmdString.endsWith("_set_length"))
  {
    //Set pre defined calibration for the stage
    int32_t length = atol(arg);
    setLength(axis, length);
    Serial.println("OK");
  }
  else if(cmdString.endsWith("_set_mode"))
  {
    //Set pre defined calibration for the stage
    uint8_t mode = atol(arg);
    setMode(axis, mode);
    Serial.println("OK");
  }
  else if(cmdString.endsWith("_set_factor"))
  {
    //Set pre defined calibration for the stage
    uint8_t factor = atol(arg);
    setFactor(axis, factor);
    Serial.println("OK");
  }

  else if(strcmp("mark_calibrated", cmd)==0)
  {
    markCalibrated();
    Serial.println("OK");
  }
  else
  {
    //Print error message if command unknown.
    Serial.println("ERR: UNKNOWN COMMAND");
  }
}



