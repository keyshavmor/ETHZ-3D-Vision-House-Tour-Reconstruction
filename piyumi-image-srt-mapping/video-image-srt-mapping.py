import pandas as pd
import cv2
import re
import nltk
nltk.download('averaged_perceptron_tagger')

# Parse subtitle file
sub_file = 'piyumi_house_tour.srt'
with open(sub_file, 'r') as f:
    sub_data = f.read()

subs = sub_data.split('\n\n')

subtitles = []
for i, subtitle in enumerate(subs):
    if(i<=(len(subs)-2)):
        sub_idx = subtitle.split('\n')[0]
        sub_time = subtitle.split('\n')[1].split(' --> ')
        start_time = pd.Timestamp(sub_time[0])
        start_time = start_time.time()
        end_time = pd.Timestamp(sub_time[1])
        end_time = end_time.time()
        sub_title = subtitle.split('\n')[2]
        sub_meta = {
            'idx': sub_idx,
            'start_time': start_time,
            'end_time': end_time,
            'text': sub_title
        }
        subtitles.append(sub_meta)

# Extract video metadata
video_file = 'HouseTourVO1.mp4'
cap = cv2.VideoCapture(video_file)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate time duration of each frame
frame_duration = 1 / frame_rate

# Map each subtitle time stamp to a corresponding frame
frame_map = []
temp_start_frame = 0
# Filter the tokens to keep only the nouns
for sub in subtitles:
    nouns = []
    start_minute = sub['start_time'].minute
    start_second = sub['start_time'].second
    start_microsecond = sub['start_time'].microsecond
    start_seconds = start_minute*60+start_second+start_microsecond/1000000
    end_minute = sub['end_time'].minute
    end_second = sub['end_time'].second
    end_microsecond = sub['end_time'].microsecond
    end_seconds = end_minute*60+end_second+end_microsecond/1000000
    subtitle_duration = end_seconds - start_seconds
    num_frames = subtitle_duration/frame_duration
    start_frame = int(temp_start_frame + 1)
    end_frame = int(temp_start_frame + num_frames)
    temp_start_frame = end_frame
    for frame_num in range(start_frame, end_frame + 1):
        sub_text = sub['text']
        sub_text = sub_text.replace('\n', ' ')
        sub_text = re.sub(r'[^\w\s]', '', sub_text)
        sub_text = sub_text.lower()
        words = sub_text.split()
        keywords = set(words)
        tagged_words = nltk.pos_tag(words)
        for word, tag in tagged_words:
            if tag.startswith('N'):
                nouns.append(word)
        labels = set(nouns)
        print(labels)
        frame_map.append({
            'sub_idx': sub['idx'],
            'frame_num': frame_num,
            'time_stamp': sub['start_time'].strftime('%H:%M:%S.%f'),
            'keywords': keywords,
            'labels': labels
        })

# Convert dictionary to pandas dataframe
df = pd.DataFrame(frame_map)

# Export dataframe to Excel sheet
df.to_excel('frame_map.xlsx', index=False)



