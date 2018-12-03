from os import path
import serial
from time import sleep
from datetime import datetime
from twisted.internet import endpoints
from twisted.web import xmlrpc, server
from AutoFocus import AutoFocus, Camera
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('PANAKEIA.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

class Microscope:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)

	    #Flash the DTR pin to reset the Arduino (Needed so the Arduino is in a known state)
        self.ser.setDTR(False)
        sleep(0.22)
        self.ser.setDTR(True)

        for index in range(1):
            line = self.ser.readline()
            print index, line

    def __del__(self):
        self.ser.close()

    def run_command(self, command):
        """TODO: Description"""
        logger.info('Running command %s', command)
        self.ser.write(command)
        line = ''
        return_value = ''
        while line != 'OK\r\n':
            line = self.ser.readline()
            logger.info('Response %s', line)
            if line.startswith('ERR:'):
                raise Exception(line)
            if line.startswith('RETURN:'):
                return_value = line.split(':')[1].strip()
        return return_value

    def check_axis(self, axis):
        """Checks that the axis string corresponds to a valid axis"""
        if axis not in ['x', 'y', 'z']:
            raise Exception('Not a valid axis!')

    def calibrate(self):
        """Starts the calibration procedure for the Microscope"""
        command = 'calibrate\n'
        self.run_command(command)

    def is_calibrated(self):
        """Check if the microscope is calibrated"""
        command = 'is_calibrated\n'
        line = self.run_command(command)
        if line == '1':
            return True
        else:
            return False

    def get_length(self, axis):
        """Returns the length of the specified axis"""
        self.check_axis(axis)
        command = axis + '_get_length\n'
        length = self.run_command(command)
        return int(length)

    def get_position(self, axis):
        """Get the current position of the specified axis"""
        self.check_axis(axis)
        command = axis + '_get_position\n'
        position = self.run_command(command)
        return int(position)

    def get_distance_to_go(self, axis):
        """Get the distance between current and target position of the specified axis"""
        self.check_axis(axis)
        command = axis + '_get_distance_to_go\n'
        distance = self.run_command(command)
        return int(distance)

    def get_state(self, axis):
        """Get the current state of the motor STOPPED=0,FWD=1,BACKWAD=-1"""
        self.check_axis(axis)
        command = axis + '_get_state\n'
        state = self.run_command(command)
        return int(state)

    def move(self, axis, steps):
        """Move the specified axis relative to current position"""
        self.check_axis(axis)
        command = axis + '_move ' + str(steps) + '\n'
        self.run_command(command)

    def move_to(self, axis, position):
        """Move the specified axis to an absolute position"""
        self.check_axis(axis)
        command = axis + '_move_to ' + str(position) + '\n'
        self.run_command(command)

    def wait_to_finish(self, axis):
        """Wait for the axis to complete work"""
        state = self.get_distance_to_go(axis)
        while state != 0:
            sleep(1)
            state = self.get_distance_to_go(axis)

    def set_mode(self, axis, mode):
        """Set microstepping mode of the specified axis"""
        self.check_axis(axis)
        command = axis + '_set_mode ' + str(mode) + '\n'
        self.run_command(command)

    def set_length(self, axis, length):
        """Set working length of the specified axis"""
        self.check_axis(axis)
        command = axis + '_set_length ' + str(length) + '\n'
        self.run_command(command)

    def set_factor(self, axis, factor):
        """Set the step factor of the specified axis"""
        self.check_axis(axis)
        command = axis + '_set_factor ' + str(factor) + '\n'
        self.run_command(command)

    def mark_calibrated(self):
        """Loaded previous calibration - mark as calibrated"""
        command = 'mark_calibrated' + '\n'
        self.run_command(command)


class MicroscopeServer(xmlrpc.XMLRPC):

    def __init__(self, serial_port, allowNone=True, useDateTime=False):
        self.serial_port = serial_port
        xmlrpc.XMLRPC.__init__(self, allowNone, useDateTime)

    def xmlrpc_initialize(self):
        self.microscope = Microscope(self.serial_port)

        try:
            with open('./PANAKEIA.conf') as infile:
                import json
                json_data = json.load(infile)
                self.microscope.set_length('x', json_data['x_length'])
                self.microscope.set_length('y', json_data['y_length'])
                self.microscope.set_length('z', json_data['z_length'])
                self.microscope.mark_calibrated()

                self.camera = Camera('./')

                max_sweep_steps = 8

                self.focus_control = AutoFocus(self.microscope, self.camera, logger,
                                               sweepsteps=4, steps=20,
                                               min_steps=1, max_sweep_steps=max_sweep_steps,
                                               number_of_times=2, precision=0.99)

        except IOError as e:
            pass

    def xmlrpc_raw(self, command):
        """TODO: Description"""
        ret = self.microscope.run_command(command)
        return ret

    def xmlrpc_calibrate(self):
        """TODO: Description"""
        self.microscope.calibrate()

    def xmlrpc_is_calibrated(self):
        """TODO: Description"""
        calibrated = self.microscope.is_calibrated()
        return calibrated

    def xmlrpc_get_length(self, axis):
        """TODO: Description"""
        length = self.microscope.get_length(axis)
        return length

    def xmlrpc_get_position(self, axis):
        """TODO: Description"""
        position = self.microscope.get_position(axis)
        return position

    def xmlrpc_get_distance_to_go(self, axis):
        """TODO: Description"""
        distance = self.microscope.get_distance_to_go(axis)
        return distance

    def xmlrpc_get_state(self, axis):
        """TODO: Description"""
        state = self.microscope.get_state(axis)
        return state

    def xmlrpc_move(self, axis, position):
        """TODO: Description"""
        self.microscope.move(axis, position)

    def xmlrpc_move_to(self, axis, position):
        """TODO: Description"""
        self.microscope.move_to(axis, position)

    def xmlrpc_set_mode(self, axis, mode):
        """TODO: Description"""
        self.microscope.set_mode(axis, mode)

    def xmlrpc_set_length(self, axis, length):
        """TODO: Description"""
        self.microscope.set_length(axis, length)

    def xmlrpc_set_factor(self, axis, factor):
        """TODO: Description"""
        self.microscope.set_factor(axis, factor)

    def xmlrpc_save_calibration(self):
        """TODO: Description"""
        if self.microscope.is_calibrated():
            x_length = self.microscope.get_length('x')
            y_length = self.microscope.get_length('y')
            z_length = self.microscope.get_length('z')
            json_data = {'x_length': x_length,
                         'y_length': y_length,
                         'z_length': z_length}

            with open("./PANAKEIA.conf", "w") as outfile:
                import json
                json.dump(json_data, outfile, indent=4)

    def xmlrpc_focus(self):
        self.focus_control.full()

    def xmlrpc_scan(self, slide_id):
        self.focus_control.scan(slide_id)

    def xmlrpc_take_picture(self):
        """Takes a photograph with datetime string for filename"""
        x_pos = self.microscope.get_position('x')
        y_pos = self.microscope.get_position('y')
        z_pos = self.microscope.get_position('z')
        image_path = self.camera.snapshot(x_pos, y_pos, z_pos)


if __name__ == '__main__':
    from twisted.internet import reactor

    r = MicroscopeServer('/dev/ttyACM0')
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 7080)
    endpoint.listen(server.Site(r))
    reactor.run()

