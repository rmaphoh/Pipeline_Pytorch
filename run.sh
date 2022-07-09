#!/bin/bash  
# RUN FILE FOR DEEP RETINAL IMAGE ANALYSIS SYSTEM
# YUKUN ZHOU 25/09/2021

date
rm -rf ./Results/*
# STEP 1 IMAGE PREPROCESSING (EXTRA BACKGROUND REMOVE, SQUARE)

echo "### Preprocess Start ###"
cd M0_Preprocess
python EyeQ_process_main.py

# STEP 2 IMAGE QUALITY ASSESSMENT

echo "### Image Quality Assessment ###"

cd ../Classification_model_Pytorch
sh test_outside.sh

# STEP 3 OPTIC DISC & VESSEL & ARTERY/VEIN SEG
echo "### Segmentation Modules ###"

cd ../Segmentation_model_Pytorch
sh test_outside.sh

# STEP 4 METRIC MEASUREMENT
echo "### Feature measuring ###"

cd ../M3_feature_whole_pic/retipy/
python create_datasets_macular_centred.py

echo "### Done ###"


# STEP 5 CORRELATION ANALYSIS
#

date
