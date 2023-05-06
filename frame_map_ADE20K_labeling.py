import pandas as pd

# read the excel files
frame_map_extended = pd.read_excel('frame_map.xlsx')
keyshav_house_labels = pd.read_excel('keyshav_house_ADE20K_labels.xlsx')

# create a dictionary to map keywords to labels
label_dict = dict(zip(keyshav_house_labels['LABELS'], keyshav_house_labels['ADE20K']))

# function to map a keyword to its corresponding label
def map_label(keyword):
    if keyword in label_dict:
        return label_dict[keyword]
    else:
        return 'Not a label'

# extract each keyword from the 5th column and map it to its corresponding label
labels = []
for row in frame_map_extended.itertuples():
    keywords = row[5].replace('{','').replace('}','').replace('\'','').split(', ')
    label_list = [map_label(keyword) for keyword in keywords]
    labels.append(str(label_list))

# write the labels back to the 6th column
frame_map_extended['ADE20K Labels'] = labels

# save the updated DataFrame to a new excel file
frame_map_extended.to_excel('frame_map.xlsx', index=False)
