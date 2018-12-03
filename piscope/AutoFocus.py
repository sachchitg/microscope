import cv2
import os
import numpy as np
from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
import logging

class AutoFocus:
    def __init__(self, microscope, camera, logger, sweepsteps=4, steps=20, min_steps=1,
                 max_sweep_steps=95, number_of_times=2, precision=0.99):
        self.microscope = microscope
        self.steps = steps
        self.sweepsteps = sweepsteps
        self.steps_original = steps
        self.min_steps = min_steps
        self.max_sweep_steps = max_sweep_steps
        self.max_pos_after_sweep = 0
        self.image_count = 0
        self.f_values = []
        self.f_max = 0.0
        self.z_motor_pos_at_f_max = 0
        self.z_first_fine_tune_position = 0
        self.ind_at_f_max = 0
        self.precision = precision
        self.number_of_times = number_of_times
        self.camera = camera
        self.logger = logger

    def get_max(self):
        """Get current best focual quality"""
        return self.f_max

    def get_max_position(self):
        return self.z_motor_pos_at_f_max

    def get_max_index(self):
        return self.ind_at_f_max

    def full(self):
        self.steps = self.steps_original
        self.microscope.move_to('z', 0)
        self.microscope.wait_to_finish('z')

        self.logger.info('Sweep')

        self.sweep()

        self.max_pos_after_sweep = self.get_max_position()
        self.microscope.move_to('z', self.max_pos_after_sweep)
        self.microscope.wait_to_finish('z')

        self.steps = int(0.5*self.steps)

        self.logger.info('Fine Tune')

        if self.fine_tune(self.get_max(), self.get_max_position()):
            x_pos = self.microscope.get_position('x')
            y_pos = self.microscope.get_position('y')
            z_pos = self.microscope.get_position('z')
            self.z_first_fine_tune_position = z_pos
            self.camera.snapshot(x_pos, y_pos, z_pos)
            self.image_count = 0

    def tune(self, start_position):
        self.steps = self.steps_original
        self.microscope.move_to('z', start_position)
        self.microscope.wait_to_finish('z')

        self.steps = int(0.5*self.steps)

        if self.fine_tune(self.get_max(), self.get_max_position()):
            x_pos = self.microscope.get_position('x')
            y_pos = self.microscope.get_position('y')
            z_pos = self.microscope.get_position('z')
            self.z_first_fine_tune_position = z_pos
            self.camera.snapshot(x_pos, y_pos, z_pos)
            self.image_count = 0

    def capture(self):
        x_pos = self.microscope.get_position('x')
        y_pos = self.microscope.get_position('y')
        z_pos = self.microscope.get_position('z')
        self.camera.snapshot(x_pos, y_pos, z_pos)

    def move_and_capture(self, step):
        self.microscope.move('z', step)
        self.microscope.wait_to_finish('z')
        z_motor_pos = self.microscope.get_position('z')
        image = self.camera.memshot()
        fc = self.camera.get_focal_quality(image)
        self.logger.info('Position: %d, Quality: %f', z_motor_pos, fc)
        return [fc, z_motor_pos]

    def fine_tune(self, fmax, fmaxpos,
                  previous_direction=True, up_or_down=True, times_checked=0):
        f_above = 0.0
        f_below = 0.0
        f_above_pos = 0
        f_below_pos = 0

        self.logger.info('Position: %d, Quality: %f', fmaxpos, fmax)

        if not previous_direction and self.steps > self.min_steps:
            self.steps = int(0.5*self.steps)
        elif self.steps <= self.min_steps:
            self.steps = self.min_steps

        [fmax, fmaxpos] = self.move_and_capture(0)

        self.z_motor_pos_at_f_max = fmaxpos
        self.f_max = fmax

        if up_or_down:
            [f_above, f_above_pos] = self.move_and_capture(self.steps)
            if f_above >= (2.0-self.precision)*fmax:
                self.fine_tune(f_above, f_above_pos, True, True)
            else:
                [f_below, f_below_pos] = self.move_and_capture(-2*self.steps)
                if f_below >= (2.0-self.precision)*fmax:
                    self.fine_tune(f_below, f_below_pos, False, False)
                else:
                    self.microscope.move_to('z', fmaxpos)
                    self.microscope.wait_to_finish('z')
                    if times_checked == self.number_of_times and self.steps > self.min_steps:
                        self.steps = self.min_steps
                        times_checked += 1
                        self.fine_tune(fmax, fmaxpos, False, False, times_checked)
                    elif times_checked < self.number_of_times and self.steps > self.min_steps:
                        times_checked += 1
                        self.fine_tune(fmax, fmaxpos, False, False, times_checked)
                    else:
                        return True
        else:
            [f_below, f_below_pos] = self.move_and_capture(-self.steps)
            if f_below > (2.0-self.precision)*fmax:
                self.fine_tune(f_below, f_below_pos, True, False)
            else:
                [f_above, f_above_pos] = self.move_and_capture(2*self.steps)
                if f_above > (2.0-self.precision)*fmax:
                    self.fine_tune(f_above, f_above_pos, False, True)
                else:
                    self.microscope.move_to('z', fmaxpos)
                    self.microscope.wait_to_finish('z')
                    if times_checked == self.number_of_times and self.steps > self.min_steps:
                        self.steps = self.min_steps
                        times_checked += 1
                        self.fine_tune(fmax, fmaxpos, False, True, times_checked)
                    elif times_checked < self.number_of_times and self.steps > self.min_steps:
                        times_checked += 1
                        self.fine_tune(fmax, fmaxpos, False, True, times_checked)
                    else:
                        return True
        return True

    def reset(self):
        self.image_count = 0
        self.z_first_fine_tune_position = 0
        self.steps = self.steps_original

        self.microscope.move_to('x', 0)
        self.microscope.move_to('y', 0)
        self.microscope.move_to('z', 0)

        self.microscope.wait_to_finish('x')
        self.microscope.wait_to_finish('y')
        self.microscope.wait_to_finish('z')


    def sweep(self):
        do_sweeping = True
        while do_sweeping:
            image = self.camera.memshot()
            z_motor_pos = self.microscope.get_position('z')
            step = self.sweepsteps
            self.microscope.move('z', step)
            fc = self.camera.get_focal_quality(image)

            self.logger.info('Position: %d, Quality: %f', z_motor_pos, fc)

            if fc > self.f_max:
                self.f_values.append(fc)
                self.z_motor_pos_at_f_max = z_motor_pos
                self.ind_at_f_max = self.f_values.index(fc)
                self.f_max = fc
                self.logger.info('Max Position: %d, Max Quality: %f', z_motor_pos, fc)

            self.image_count += 1

            self.microscope.wait_to_finish('z')

            if self.image_count >= self.max_sweep_steps:
                do_sweeping = False
                self.image_count = 0

    def scan(self, slide_id):
        x_sf = 1./3.
        x_ef = 2./3.
        y_sf = 1./3.
        y_ef = 2./3.
        move_per_iteration = 240

        self.camera.set_snapshot_directory(slide_id)

        self.camera.collect_dust_data()

        if self.microscope.is_calibrated():
            x_length = self.microscope.get_length('x')
            y_length = self.microscope.get_length('y')
            z_length = self.microscope.get_length('z')
            json_data = {'x_length': x_length,
                         'y_length': y_length,
                         'z_length': z_length,
                         'x_sf' : x_sf,
                         'x_ef' : x_ef,
                         'y_sf' : y_sf,
                         'y_ef' : y_ef,
                         'move_per_iteration' : move_per_iteration}

            with open('./' + str(slide_id) + '/' + 'PANAKEIA.conf', "w") as outfile:
                import json
                json.dump(json_data, outfile, indent=4)

        #Move to middle and get full focus value
        x_length = self.microscope.get_length('x')
        y_length = self.microscope.get_length('y')
        x_mid = int(x_length*1./2.)
        y_mid = int(y_length*1./2.)

        self.microscope.move_to('x', x_mid)
        self.microscope.move_to('y', y_mid)

        self.microscope.wait_to_finish('x')
        self.microscope.wait_to_finish('y')

        self.full()
        self.z_first_fine_tune_position = self.microscope.get_position('z')

        #Move to start position of ROI
        x_start = int(x_length*x_sf)
        x_end = int(x_length*x_ef)
        y_start = int(y_length*y_sf)
        y_end = int(y_length*y_ef)

        for y_pos in range(y_start, y_end, move_per_iteration):
            for x_pos in range(x_start, x_end, move_per_iteration):
                self.microscope.move_to('x', x_pos)
                self.microscope.move_to('y', y_pos)

                self.microscope.wait_to_finish('x')
                self.microscope.wait_to_finish('y')

                self.tune(self.max_pos_after_sweep)
                self.capture()

        self.reset()

class Camera:
    def __init__(self, working_folder, width=640, height=480):
        self.working_folder = working_folder
        self.working_directory = None
        self.width = width
        self.height = height
        self.cam = PiCamera(resolution=(self.width, self.height), framerate=30)
        self.cam.iso = 100
        # Wait for the automatic gain control to settle
        sleep(2)
        self.cam.start_preview()
        # Now fix the values
        #self.cam.shutter_speed = self.cam.exposure_speed
        #self.cam.exposure_mode = 'off'
        #g = self.cam.awb_gains
        #self.cam.awb_mode = 'off'
        #self.cam.awb_gains = g
        self.dust = None
        
    def _compose_alpha(self, img_in, img_layer, opacity):
        comp_alpha = np.minimum(img_in[:, :, 3], img_layer[:, :, 3])*opacity
        new_alpha = img_in[:, :, 3] + (1.0 - img_in[:, :, 3])*comp_alpha
        np.seterr(divide='ignore', invalid='ignore')
        ratio = comp_alpha/new_alpha
        ratio[ratio == np.NAN] = 0.0
        return ratio

    def _convert_np_float(self, img_in):
        b_channel, g_channel, r_channel = cv2.split(img_in)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
        img_out = np.array(cv2.merge((b_channel, g_channel, r_channel, alpha_channel))).astype(float)
        return img_out

    def _grain_extract(self, img_in, img_layer, opacity):
        assert img_in.dtype == np.float, 'Input variable img_in should be of numpy.float type.'
        assert img_layer.dtype == np.float, 'Input variable img_layer should be of numpy.float type.'
        assert img_in.shape[2] == 4, 'Input variable img_in should be of shape [:, :,4].'
        assert img_layer.shape[2] == 4, 'Input variable img_layer should be of shape [:, :,4].'
        assert 0.0 <= opacity <= 1.0, 'Opacity needs to be between 0.0 and 1.0.'

        img_in /= 255.0
        img_layer /= 255.0

        ratio = self._compose_alpha(img_in, img_layer, opacity)

        comp = np.clip(img_in[:, :, :3] - img_layer[:, :, :3] + 0.5, 0.0, 1.0)

        ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
        img_out = comp * ratio_rs + img_in[:, :, :3] * (1.0 - ratio_rs)
        img_out = np.nan_to_num(np.dstack((img_out, img_in[:, :, 3])))  # add alpha channel and replace nans
        return img_out*255.0

    def _adjust_brightness(self, img):
        clahe = cv2.createCLAHE(clipLimit=2., tileGridSize=(16,16))
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels
        l2 = clahe.apply(l)  # apply CLAHE to the L-channel
        lab = cv2.merge((l2,a,b))  # merge channels
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR


    def _enhance(self, img):
        input_layer = self._convert_np_float(img)
        mask_layer = self._convert_np_float(self.dust)
        
        blended_image = self._grain_extract(input_layer, mask_layer, 1.0)
        adjusted_image = self._adjust_brightness(blended_image.astype('uint8'))

        return adjusted_image

    def __del__(self):
        self.cam.close()

    def set_snapshot_directory(self, folder_name):
        from os import path
        directory = self.working_folder + folder_name + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.working_directory = directory

    def collect_dust_data(self):
        self.dust = np.empty((240 * 320 * 3,), dtype=np.uint8)
        self.cam.capture(self.dust, 'bgr', resize=(320, 240))
        self.dust = self.dust.reshape((240, 320, 3))

        sleep(2)

        image_path = ''
        if self.working_directory:
            image_path = self.working_folder + self.working_directory + \
                     'dust.jpg'
        else:
            image_path = self.working_folder + \
                     'dust.jpg'

        image_file = open(image_path, 'wb')
        #sleep(2)
        self.cam.capture(image_file)
        image_file.close()

    def snapshot(self, x_position, y_position, z_position):
        position_str = str(x_position) + '-' + str(y_position) + '-' + str(z_position) + '-'
        image_path = ''
        if self.working_directory:
            image_path = self.working_folder + self.working_directory + \
                     'img-' + position_str + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        else:
            image_path = self.working_folder + \
                     'img-' + position_str + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'

        image_file = open(image_path, 'wb')
        sleep(2)
        self.cam.capture(image_file)
        image_file.close()
        return image_file

    def memshot(self):
        image = np.empty((240 * 320 * 3,), dtype=np.uint8)
        sleep(2)
        self.cam.capture(image, 'bgr', resize=(320, 240))
        image = image.reshape((240, 320, 3))
        return image

    def get_focal_quality(self, image):
        eimage = self._enhance(image)
        gimg = cv2.cvtColor(eimage, cv2.COLOR_BGR2GRAY)
        [height, width] = gimg.shape

        intensity = 0.0
        intensity_squared_sum = 0.0
        for i in range(0, width-1):
            for j in range(0, height-1):
                intensity += gimg[j][i]

        mean_intensity = intensity/float(width*height)

        if mean_intensity == 0.0:
            mean_intensity = 1e-10

        for i in range(0, width-1):
            for j in range(0, height-1):
                intensity_squared_sum += (float(gimg[j][i]) - mean_intensity)*(float(gimg[j][i]) - mean_intensity)

        f_quality = intensity_squared_sum/(float(width*height)*mean_intensity)
        return f_quality

##cam = Camera('./')
##cam.set_snapshot_directory('test')
##for i in range(0,25):
##    img = cam.memshot()
##    cam.snapshot(0,0,0)
##    sleep(5)