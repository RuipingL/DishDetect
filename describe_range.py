import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from gtts import gTTS
import os
import string
from pathlib import Path

# Get the current working directory


# Read the sam_mask_label.txt file
label_file_path = 'Output/Panoptic_Results/target/sam_mask_label/sam_mask_label.txt'

with open(label_file_path, 'r') as file:
    lines = file.readlines()

# Parse the content 
data = [line.strip().split(',') for line in lines]

df = pd.DataFrame(data[1:], columns = data[0])

df = df.astype(
    {'id':'int',
    'category_id':'int',
    'category_name':'string',
    'category_count_ratio':'float',
    'mask_count_ratio':'float'}
)

# Remove the background
df = df[df['category_id'] != 0]

# Get unique category names
unique_categories = df['category_name'].unique()

# Create a dictionary to store the new DataFrames
category_dataframes = {}

# Loop through the unique category names
for category in unique_categories:
    # Create a new DataFrame for each category
    category_df = df[df['category_name'] == category]
    # Store the DataFrame in the dictionary
    category_dataframes[f'{category.replace(" ", "_")}'] = category_df


# Load the sam_masks
masks = np.load('Output/Panoptic_Results/target/sam_mask/masks.npy')

height, width = masks[0].shape


# Transform cartesian coordinate into polar coordinate
def cartesian_to_polar(x, y, origin_x, origin_y):
    dx = x - origin_x
    dy = origin_y - y # Reverse the y direction
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dx, dy)
    theta = np.degrees(theta) % 360
    return r, theta

# Determine clock direction of the centroid
def theta_to_clock_section(theta):
    section = int(((theta-15) % 360) // 30) + 1
    return section

def find_longest_zero_sequence(arr):
    start_idx = []
    end_idx = []
    if arr[0] == 0:
        start_idx = [0]
    for i in range(1, len(arr)-1):
        if arr[i] == 0 and arr[i-1]!=0:
            start_idx.append(i)
        if arr[i] == 0 and arr[i+1]!=0:
            end_idx.append(i)
    if arr[-1] == 0:
        end_idx.append(len(arr)-1)
    differences = [a - b for a, b in zip(end_idx, start_idx)]
    max_diff_index = differences.index(max(differences))
    return start_idx[max_diff_index], end_idx[max_diff_index]
            

def contour_to_theta(contour, origin_x, origin_y, r_min):
    points_num = len(contour)
    theta_idx = [0]*720
    r_=0
    convert=False
    for i in range(points_num):
        px, py = contour[i][0]
        r, theta = cartesian_to_polar(px, py, origin_x, origin_y)
        if r>r_min:
            theta_idx[int(theta)] = theta_idx[int(theta)]+1
    theta_idx[360:]= theta_idx[:360]
    theta_end, theta_start = find_longest_zero_sequence(theta_idx)
    return theta_end%360, theta_start%360
        
    
    
    

# Take the center of the picture as the origin of the coordinate
origin_x, origin_y = width // 2, height // 2

# Store the centroids polar coordinates
polar_coords = []

for name, dataframe in category_dataframes.items():
    merged_image = np.zeros((height, width), dtype=np.uint8)
    for i in range(len(dataframe['id'])):
        index = dataframe.iloc[i, dataframe.columns.get_loc('id')]
        image = masks[index].astype(np.uint8)
        merged_image = cv.bitwise_or(merged_image, image)
        
        # Apply morphological operations to close gaps
        kernel = np.ones((5,5),np.uint8)
        merged_image = cv.morphologyEx(merged_image, cv.MORPH_CLOSE, kernel)

    
    # find contours
    contours, _ = cv.findContours(merged_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # filter contours by area
    min_area = 1000
    
    filtered_contours = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > min_area:
            filtered_contours.append(contour)

    # Calculate moments and centroids
    centroids = []
    for contour in filtered_contours:
        M = cv.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centroids.append((cX, cY))
            r, theta = cartesian_to_polar(cX, cY, origin_x, origin_y)
            if r > 50:
                theta_end, theta_start = contour_to_theta(contour, origin_x, origin_y,r)
                if abs(theta_start-theta_end)>=30:
                    theta_start = theta_start+15
                    theta_end = theta_end -15
                clock_start = theta_to_clock_section(theta_start)
                clock_end = theta_to_clock_section(theta_end)
                polar_coords.append(([clock_start, clock_end], name))
            else:
                polar_coords.append((None, name))

    merged_image = cv.cvtColor(merged_image, cv.COLOR_GRAY2BGR)
    # Draw filtered and approximated contours and centroids
    for contour, centroid in zip(filtered_contours, centroids):
        color = tuple(np.random.randint(0, 255, size=3).tolist())
        cv.drawContours(merged_image, [contour], -1, color, 3)
        if centroid is not None:
            cv.circle(merged_image, centroid, 5, (0, 0, 255), -1)  # Draw the centroid as a red dot
    

    #This code snippet can be used to verify whether the centroids are correctly be found or not by plotting them

#     plt.figure(figsize=(6,6))
#     plt.imshow(cv.cvtColor(merged_image, cv.COLOR_BGR2RGB))
#     plt.title(f'Merged Image of {name}')
#     plt.axis('on')
#     plt.show()
    


# Prepare the describtion text
def remove_punctuation(text):
    translator = str.maketrans('_',' ', string.punctuation)
    return text.translate(translator)

descriptions = []


for clock, name in polar_coords:
    if clock is None: 
        text = f'The {name} is in the center of the plate.'
    elif clock[0]==clock[1]:
        text = f"The {name} is in the direction of {clock[0]} 'o clock."
    else:
        text = f"The {name} is from {clock[0]} to {clock[1]} 'o clock."
    descriptions.append(text)

# Combine all descriptions into a single string
combined_text = "\n".join(descriptions)
# Remove punctuations in the text
cleaned_text = remove_punctuation(combined_text)

# Create a gTTS object
tts = gTTS(text=cleaned_text, lang='en')


new_directory_name = 'output_final'

new_directory_path = Path(new_directory_name)

# Check if the directory already exists or not
if not new_directory_path.exists():
    new_directory_path.mkdir()

# speech_file_path = new_directory_path/ 'speech.mp3'

# # Save the audio to a file
# tts.save(speech_file_path)

text_file_path = new_directory_path/ 'description.txt'
# Save the describtion text to a file
with open(text_file_path, 'w') as file:
    file.write(combined_text)

print(combined_text)
