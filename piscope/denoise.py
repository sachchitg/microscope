import cv2
import glob
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def _compose_alpha(img_in, img_layer, opacity):
    """
    Calculate alpha composition ratio between two images.
    """

    comp_alpha = np.minimum(img_in[:, :, 3], img_layer[:, :, 3])*opacity
    new_alpha = img_in[:, :, 3] + (1.0 - img_in[:, :, 3])*comp_alpha
    np.seterr(divide='ignore', invalid='ignore')
    ratio = comp_alpha/new_alpha
    ratio[ratio == np.NAN] = 0.0
    return ratio

def _convert_np_float(img_in):
    b_channel, g_channel, r_channel = cv2.split(img_in)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
    img_out = np.array(cv2.merge((b_channel, g_channel, r_channel, alpha_channel))).astype(float)
    return img_out

def grain_extract(img_in, img_layer, opacity):
    assert img_in.dtype == np.float, 'Input variable img_in should be of numpy.float type.'
    assert img_layer.dtype == np.float, 'Input variable img_layer should be of numpy.float type.'
    assert img_in.shape[2] == 4, 'Input variable img_in should be of shape [:, :,4].'
    assert img_layer.shape[2] == 4, 'Input variable img_layer should be of shape [:, :,4].'
    assert 0.0 <= opacity <= 1.0, 'Opacity needs to be between 0.0 and 1.0.'

    img_in /= 255.0
    img_layer /= 255.0

    ratio = _compose_alpha(img_in, img_layer, opacity)

    comp = np.clip(img_in[:, :, :3] - img_layer[:, :, :3] + 0.5, 0.0, 1.0)

    ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in[:, :, :3] * (1.0 - ratio_rs)
    img_out = np.nan_to_num(np.dstack((img_out, img_in[:, :, 3])))  # add alpha channel and replace nans
    return img_out*255.0

def adjust_brightness(img):
    clahe = cv2.createCLAHE(clipLimit=2., tileGridSize=(16,16))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR


def enhance(input_image, mask_image):
    img = cv2.imread(input_image)
    mask = cv2.imread(mask_image)
    input_layer = _convert_np_float(img)
    mask_layer = _convert_np_float(mask)
    
    blended_image = grain_extract(input_layer, mask_layer, 1.0)
    adjusted_image = adjust_brightness(blended_image.astype('uint8'))
    brightness = ImageEnhance.Brightness(Image.fromarray(adjusted_image)).enhance(1.5)
    contrast = ImageEnhance.Contrast(brightness).enhance(1.1)
    return np.array(contrast)

mask = './dust.jpg'
file_root = './100ximages/'
for file in glob.glob(file_root + '*.jpg'):
    inp = str(file)
    output = './100ximages-processed/' + str(file)[len(file_root):]
    res = enhance(inp, mask)
    cv2.imwrite(output, res)
    print inp