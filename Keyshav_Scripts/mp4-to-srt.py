import moviepy.editor as mp
import pysrt
import pandas as pd
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Download NLTK resources (if not already downloaded)
nltk.download('averaged_perceptron_tagger')

# Video file path
video_path = 'apartment-final-tour.mp4'

# SRT subtitle file path
subtitle_path = 'final-apartment-tour-final.srt'

# Read the video
video = mp.VideoFileClip(video_path)

# Get the frame rate of the video
frame_rate = video.fps

# Read the SRT subtitle file
subs = pysrt.open(subtitle_path)

# Initialize empty lists for frames and keywords
frames = []
keywords = []

# Iterate through each subtitle
for sub in subs:
    # Calculate the start and end time of the subtitle in seconds
    start_time = sub.start.seconds + sub.start.minutes * 60 + sub.start.hours * 3600
    end_time = sub.end.seconds + sub.end.minutes * 60 + sub.end.hours * 3600

    # Convert the start and end time to frame numbers
    start_frame = int(start_time * frame_rate)
    end_frame = int(end_time * frame_rate)

    # Add the keyword to the list for each frame within the subtitle's duration
    for frame_num in range(start_frame, end_frame + 1):
        frames.append(frame_num)
        keywords.append(sub.text)

# Create a DataFrame to store the mapping
data = pd.DataFrame({'Frame': frames, 'Keyword': keywords})

# Tokenize the keywords and perform POS tagging
data['Tokenized'] = data['Keyword'].apply(word_tokenize)
data['POS'] = data['Tokenized'].apply(pos_tag)

# Extract nouns and adjectives from the POS tagged keywords
nouns_adjectives = []
for pos_tags in data['POS']:
    filtered_tags = [word for word, tag in pos_tags if tag.startswith('NN') or tag.startswith('JJ')]
    nouns_adjectives.append(filtered_tags)

# Add the extracted nouns and adjectives to the 'labels' column
data['labels'] = nouns_adjectives

# Save the data to an Excel file
excel_path = 'test.xlsx'
data.to_excel(excel_path, index=False)

# Excel file path
excel_path = 'test.xlsx'

# CSV file path
csv_path = 'frame_label_map.csv'

# Read the Excel file
data = pd.read_excel(excel_path)

# Select only the "Frame" and "labels" columns
selected_data = data[['Frame', 'labels']]

# Save the selected data to a CSV file
selected_data.to_csv(csv_path, index=False)
