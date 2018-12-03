/*
  Stage.h - Library for controlling the stage
*/
#include "Arduino.h"
#include <Wire.h>
#include <kissStepper.h>

#ifndef Stage_h
#define Stage_h

// Number of full steps in one revolution of the motor
const long motorFullStPerRev = 200; 

// Define motor selections
#define X_STEPPER 0
#define Y_STEPPER 1
#define Z_STEPPER 2

// String length
#define MAX_LENGTH 40

// Z_DELTA
#define Z_DELTA 0

class Stage
{
  public:
    Stage();

    void begin();
    void loop();

    void calibrate();
    void markCalibrated();

    int32_t getPosition(int stepper);
    int32_t getDistanceToGo(int stepper);
    int32_t getLength(int stepper);
    int32_t getMoveState(int stepper);

    void Move(int stepper, int32_t steps);
    void MoveTo(int stepper,int32_t position);

    void setMode(int stepper, uint8_t mode);
    void setLength(int stepper, int32_t length);
    void setFactor(int stepper, int32_t factor);

    void serialEvent();

  private:
    void update(kissStepper* mot, int32_t targetPos, int32_t factor);
    void setMotorDriveMode(kissStepper* mot, uint8_t mode);
    void do_calibrate();

    void processString();
    void resetMotor(kissStepper* mot, uint8_t mode);
    void handleCommand(char* cmd, char* arg);

    boolean begin_calibration;;
    boolean calibrated;
    boolean calibration_x;
    boolean calibration_y;
    boolean calibration_z;

    int32_t _x_pos; // current position of the X motor
    int32_t _y_pos; // current position of the Y motor
    int32_t _z_pos; // current position of the Z motor

    int32_t _x_factor; // current dividing factor of the X motor
    int32_t _y_factor; // current dividing factor of the Y motor
    int32_t _z_factor; // current dividing factor of the Z motor

    int32_t _x_length; // movable length over target area on X direction
    int32_t _y_length; // movable length over target area on Y direction
    int32_t _z_length; // movable length over target area on Z direction (dependent on objective working length, for 40X about 0.6 mm)

    int32_t _x_target; // current target position set in X direction relative to (0,0,0)
    int32_t _y_target; // current target position set in Y direction relative to (0,0,0)
    int32_t _z_target; // current target position set in Z direction relative to (0,0,0)

    kissStepper* mot_X; // Stepper motor object in X axis
    kissStepper* mot_Y; // Stepper motor object in Y axis
    kissStepper* mot_Z; // Stepper motor object in Z axis
    
    long _x_last_step;
    long _y_last_step;
    long _z_last_step;
    long _print_last_step;

    long _x_interval;
    long _y_interval;
    long _z_interval;
    long _print_interval;

    boolean string_complete; //Flag to indicate command received
  
    char *input_string; //Raw string from serial
    char *command;
    char *arg; //Argument given with command
  
    int str_pos; //String position counter
};

#endif
