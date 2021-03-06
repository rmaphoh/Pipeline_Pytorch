#!/usr/bin/env python3

# Retipy - Retinal Image Processing on Python
# Copyright (C) 2017  Alejandro Valdes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
script to estimate the linear tortuosity of a set of retinal images, it will output the values
to a file in the output folder defined in the configuration. The output will only have the
estimated value and it is sorted by image file name.
"""

import argparse
import glob
# import numpy as np
import os
import h5py
import shutil
import pandas as pd
# import scipy.stats as stats

from retipy import configuration, retina, tortuosity_measures


if os.path.exists('../../Results/M2/artery_vein/artery_binary_skeleton/.ipynb_checkpoints'):
    shutil.rmtree('../../Results/M2/artery_vein/artery_binary_skeleton/.ipynb_checkpoints') 
if os.path.exists('../../Results/M2/binary_vessel/binary_skeleton/.ipynb_checkpoints'):
    shutil.rmtree('../../Results/M2/binary_vessel/binary_skeleton/.ipynb_checkpoints') 
if os.path.exists('../../Results/M2/artery_vein/vein_binary_skeleton/.ipynb_checkpoints'):
    shutil.rmtree('../../Results/M2/artery_vein/vein_binary_skeleton/.ipynb_checkpoints')
if not os.path.exists('../../Results/M3/'):
    os.makedirs('../../Results/M3/')

parser = argparse.ArgumentParser()

parser.add_argument(
    "-c",
    "--configuration",
    help="the configuration file location",
    default="resources/retipy.config")
args = parser.parse_args()

CONFIG = configuration.Configuration(args.configuration)
binary_FD_binary,binary_VD_binary,binary_Average_width= [],[],[]
name_list = []

Binary_PATH = '../../Results/M2/binary_skeleton/'

for filename in sorted(glob.glob(os.path.join(Binary_PATH, '*.png'))):

    try:
        segmentedImage = retina.Retina(None, filename, store_path='../../Results/M2/binary_vessel/')

        window_sizes = [912]
        window = retina.Window(
            segmentedImage, window_sizes[-1], min_pixels=CONFIG.pixels_per_window)
        FD_binary,VD_binary,Average_width, t2, t4, td = tortuosity_measures.evaluate_window(window, CONFIG.pixels_per_window, CONFIG.sampling_size, CONFIG.r_2_threshold,store_path='../../Results/M2/binary_vessel/')

        binary_FD_binary.append(FD_binary)
        binary_VD_binary.append(VD_binary)
        binary_Average_width.append(Average_width)
        name_list.append('./test_data/' + filename.split('/')[-1])
    
    except:
        pass


Data4stage2 = pd.DataFrame({'image':name_list, 'Fractal_dimension':binary_FD_binary, 'Vessel_density':binary_VD_binary, 'Average_width':binary_Average_width})
Data4stage2.to_csv('../../Results/M3/Macular_Measurement.csv', index = None, encoding='utf8')
