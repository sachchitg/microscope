import cv2
import glob
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import tifffile as tiff

class Stitcher:
    def __init__(self, file_root, dust_file, width=3280, height=2464):
        self.file_root = file_root
        self.dust = dust_file
        self.width = width
        self.height = height
        #load conf
        try:
            with open('./PANAKEIA.conf') as infile:
                import json
                json_data = json.load(infile)
                self.x_length = json_data['x_length']
                self.y_length =  json_data['y_length']
                self.x_start = int(self.x_length*2/5)
                self.x_end = int(self.x_length*3/5)
                self.y_start = int(self.y_length*2/5)
                self.y_end = int(self.y_length*3/5)
                self.move_per_iteration = 240
                self.x_count = len(range(self.x_start, self.x_end, self.move_per_iteration))
                self.y_count = len(range(self.y_start, self.y_end, self.move_per_iteration))
                self.image_count = self.x_count*self.y_count
        except IOError as e:
            pass

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

    def enhance(self, input_image, mask_image):
        img = cv2.imread(input_image)
        mask = cv2.imread(mask_image)
        input_layer = self._convert_np_float(img)
        mask_layer = self._convert_np_float(mask)
        
        blended_image = self._grain_extract(input_layer, mask_layer, 1.0)
        adjusted_image = self._adjust_brightness(blended_image.astype('uint8'))
        brightness = ImageEnhance.Brightness(Image.fromarray(adjusted_image)).enhance(1.7)
        contrast = ImageEnhance.Contrast(brightness).enhance(1.1)
        return np.array(contrast)

    def prepare_files(self):
        for file in glob.glob(self.file_root + '*.jpg'):
            inp = str(file)
            name = str(file)[len(self.file_root):].split('.')[0]
            parts = name.split('-')
            output = './tmp/' + parts[0] + '-' + parts[1] + '-' + parts[2] +  '.jpg'
            res = self.enhance(inp, self.dust)
            cv2.imwrite(output, res)

    def save_for_ImageJ(self):
        self.prepare_files()
        
        y_counter = 1
        for y_pos in range(self.y_start, self.y_end, self.move_per_iteration):
            x_counter = 1
            for x_pos in range(self.x_start, self.x_end, self.move_per_iteration):
                img_path = './tmp/' + 'img' + '-' + str(int(x_pos/8)*8) + '-' + str(int(y_pos/8)*8) +  '.jpg'
                img = cv2.imread(img_path)

                tiff.imsave('./tile/' + 'tile_' + str(x_counter) + str(y_counter) + '.tif', img[...,::-1])
                x_counter +=1
            y_counter +=1

    def tile(self):
        tile_image = np.zeros((self.height*self.y_count,self.width*self.x_count,3), np.uint8) 

        self.prepare_files()
        
        y_counter = self.y_count
        for y_pos in range(self.y_start, self.y_end, self.move_per_iteration):
            x_counter = self.x_count
            for x_pos in range(self.x_start, self.x_end, self.move_per_iteration):
                img_path = './tmp/' + 'img' + '-' + str(int(x_pos/8)*8) + '-' + str(int(y_pos/8)*8) +  '.jpg'
                img = cv2.imread(img_path) 

                print img_path

                h_from = (y_counter-1)*self.height
                h_to = y_counter*self.height
                w_from = (x_counter-1)*self.width
                w_to = x_counter*self.width

                tile_image[h_from:h_to, w_from:w_to] = img

                x_counter -= 1
            y_counter -= 1

        return tile_image

s = Stitcher('./blood-new/','./dust.jpg')
img = s.tile()
cv2.imwrite('blood.jpg', img)