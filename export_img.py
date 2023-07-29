import pydicom as dicom
import os
import cv2
import numpy as np

# Specify the .dcm folder path
folder_path = "matched_dicom"
# Specify the output jpg/png folder path
jpg_folder_path = "images"
# make it True if you want in PNG format
PNG = False

images_path = os.listdir(folder_path)
for n, image_filename in enumerate(images_path):
    ds = dicom.dcmread(os.path.join(folder_path, image_filename))
    
    # Get pixel data as numpy array
    pixel_array_numpy = ds.pixel_array
    
    # Apply rescale and intercept if present
    if 'RescaleSlope' in ds:
        rescale_slope = ds.RescaleSlope
        pixel_array_numpy = pixel_array_numpy * rescale_slope
    if 'RescaleIntercept' in ds:
        rescale_intercept = ds.RescaleIntercept
        pixel_array_numpy = pixel_array_numpy + rescale_intercept
    
    # Apply windowing if present
    if 'WindowCenter' in ds and 'WindowWidth' in ds:
        window_center = np.mean(ds.WindowCenter)
        window_width = np.mean(ds.WindowWidth)
        window_min = window_center - (window_width / 2)
        window_max = window_center + (window_width / 2)
        pixel_array_numpy = np.clip(pixel_array_numpy, window_min, window_max)
    
    # Normalize to 8-bit range if needed (0 to 255)
    pixel_array_numpy = (pixel_array_numpy - np.min(pixel_array_numpy)) / (np.max(pixel_array_numpy) - np.min(pixel_array_numpy)) * 255.0
    
    # Convert to uint8
    pixel_array_numpy = pixel_array_numpy.astype(np.uint8)
    
    # Save the image
    if PNG == False:
        image_filename = image_filename.replace('.dcm', '.jpg')
    else:
        image_filename = image_filename.replace('.dcm', '.png')
    cv2.imwrite(os.path.join(jpg_folder_path, image_filename), pixel_array_numpy)
    
    if n % 50 == 0:
        print('{} image converted'.format(n))

