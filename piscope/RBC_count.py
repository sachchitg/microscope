import numpy as np
import cv2
import sys
import os

class RBCCounter:
    def __init__(self, inpath, outpath, tolerance=50, output_image=True, output_stats=True):
        self.inpath = inpath
        self.outpath = outpath
        self.tolerance = int(tolerance) * 0.01
        self.original_image = cv2.imread(self.inpath)
        self.width, self.height, self.channels = self.original_image.shape
        self.output_image = output_image
        self.output_stats = output_stats
        self.file_name = os.path.splitext(os.path.basename(inpath))[0]
    
    def calc_sloop_change(self, histo, mode, tolerance):
        sloop = 0
        for i in range(0, len(histo)):
            if histo[i] > max(1, tolerance):
                sloop = i
                return sloop
            else:
                sloop = i
    
    def _gen_properties(self):
        self.hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)

        self.color_image = self.original_image.copy()

        self.b_channel, self.g_channel, self.r_channel = cv2.split(self.color_image)
        
        self.blue_hist = cv2.calcHist([self.color_image], [0], None, [256], [0, 256])
        self.green_hist = cv2.calcHist([self.color_image], [1], None, [256], [0, 256])
        self.red_hist = cv2.calcHist([self.color_image], [2], None, [256], [0, 256])
        
        self.blue_mode = self.blue_hist.max()
        self.blue_tolerance = np.where(self.blue_hist == self.blue_mode)[0][0] * self.tolerance
        
        self.green_mode = self.green_hist.max()
        self.green_tolerance = np.where(self.green_hist == self.green_mode)[0][0] * self.tolerance
        
        self.red_mode = self.red_hist.max()
        self.red_tolerance = np.where(self.red_hist == self.red_mode)[0][0] * self.tolerance
        
        self.sloop_blue = self.calc_sloop_change(self.blue_hist, self.blue_mode, self.blue_tolerance)
        self.sloop_green = self.calc_sloop_change(self.green_hist, self.green_mode, self.green_tolerance)
        self.sloop_red = self.calc_sloop_change(self.red_hist, self.red_mode, self.red_tolerance)
        
        self.gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.gray_hist = cv2.calcHist([self.original_image], [0], None, [256], [0, 256])
        
        self.largest_gray = self.gray_hist.max()
        self.threshold_gray = np.where(self.gray_hist == self.largest_gray)[0][0]


    def filter_big_cells(self, image):
        #threshold blue ranges
        #BGR ordering
        lower_blue = np.array([115,30,20])
        upper_blue = np.array([173,98,90])

        mask = cv2.inRange(image, lower_blue, upper_blue)
        return mask

    def filter_small_cells(self, image):
        #threshold pink/red ranges
        #BGR ordering
        lower_pink = np.array([111,48,90])
        upper_pink = np.array([204,190,218])

        mask = cv2.inRange(image, lower_pink, upper_pink)
        return mask

    def find_big_cells(self, contours, big_bound):
        big_cells = []

        for c in contours:
            c_area = cv2.contourArea(c)

            if c_area > big_bound:
                big_cells.append(c)

        return big_cells

    def find_small_cells(self, contours, small_bound):
        small_cells = []

        for c in contours:
            c_area = cv2.contourArea(c)

            if c_area > small_bound:
                small_cells.append(c)

        return small_cells

    def count(self):
        self._gen_properties()

        self.mask = self.filter_small_cells(self.color_image)

        gr_img = cv2.adaptiveThreshold(self.mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 85, 4)
        _, contours, hierarchy = cv2.findContours(gr_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        c2 = [i for i in contours if cv2.boundingRect(i)[3] > 35]
        cv2.drawContours(self.color_image, c2, -1, (0, 0, 255), 1)

        cp = [cv2.approxPolyDP(i, 0.015 * cv2.arcLength(i, True), True) for i in c2]

        countRedCells = len(c2)

        for c in cp:
            xc, yc, wc, hc = cv2.boundingRect(c)
            cv2.rectangle(self.color_image, (xc, yc), (xc + wc, yc + hc), (0, 255, 0), 1)

        if self.output_image:
            cv2.imwrite(self.outpath + self.file_name + '.jpg', self.color_image)

        if self.output_stats:
            with open(self.outpath + self.file_name + '.stats', mode='w') as f:
                f.write('RBC: ' + str(countRedCells) + '\n')

    def WBCcount(self):
        self._gen_properties()

        self.mask = self.filter_big_cells(self.color_image)

        gr_img = cv2.adaptiveThreshold(self.mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 85, 4)
        _, contours, hierarchy = cv2.findContours(gr_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        c2 = [i for i in contours if cv2.boundingRect(i)[3] > 35]
        cv2.drawContours(self.color_image, c2, -1, (0, 0, 255), 1)

        cp = [cv2.approxPolyDP(i, 0.015 * cv2.arcLength(i, True), True) for i in c2]

        countRedCells = len(c2)

        for c in cp:
            xc, yc, wc, hc = cv2.boundingRect(c)
            cv2.rectangle(self.color_image, (xc, yc), (xc + wc, yc + hc), (0, 255, 0), 1)

        if self.output_image:
            cv2.imwrite(self.outpath + self.file_name + '-wbc.jpg', self.color_image)

        if self.output_stats:
            with open(self.outpath + self.file_name + '-wbc.stats', mode='w') as f:
                f.write('WBC: ' + str(countRedCells) + '\n')


ctr = RBCCounter('./blood-new-processed/img-4664-2880-1792-2017-11-08-08-59-52.jpg', './tmp/')
ctr.count()
ctr.WBCcount()