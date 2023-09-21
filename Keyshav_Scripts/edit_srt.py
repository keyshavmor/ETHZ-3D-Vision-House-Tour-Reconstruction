import re

class Subtitle:
    def __init__(self, index, start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text

def parse_srt_file(srt_file):
    with open(srt_file, 'r') as f:
        content = f.read().strip()
    
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|$)'
    matches = re.findall(pattern, content, flags=re.DOTALL)
    
    subtitles = []
    for match in matches:
        index = int(match[0])
        start = match[1]
        end = match[2]
        text = match[3].strip()
        subtitle = Subtitle(index, start, end, text)
        subtitles.append(subtitle)
    
    return subtitles

def add_silence_subtitles(srt_file):
    subtitles = parse_srt_file(srt_file)
    
    new_subtitles = []
    for i in range(len(subtitles) - 1):
        subtitle1 = subtitles[i]
        subtitle2 = subtitles[i + 1]
        
        start_time = subtitle1.end
        end_time = subtitle2.start
        
        silence_subtitle = Subtitle(subtitle1.index + 1, start_time, end_time, 'silence')
        new_subtitles.append(silence_subtitle)
    
    updated_subtitles = []
    for subtitle in subtitles:
        updated_subtitles.append(subtitle)
        for new_subtitle in new_subtitles:
            if new_subtitle.start == subtitle.end:
                updated_subtitles.append(Subtitle(new_subtitle.index, new_subtitle.start, new_subtitle.end, new_subtitle.text))
                updated_subtitles.append(Subtitle('', '', '', ''))
    
    with open('final-apartment-tour-new.txt', 'w') as f:
        for subtitle in updated_subtitles:
            if subtitle.index:
                f.write(f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{subtitle.text}\n\n")
            else:
                f.write("\n")

# Example usage
add_silence_subtitles('final-apartment-tour-old.srt')

with open('final-apartment-tour-new.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    for line in input_file:
        # Strip any whitespace from the line
        line = line.strip()
        # Check if the line has only one character or an integer
        if len(line) == 1 or line.isdigit():
            continue
        # Write the line to the output file
        output_file.write(line + '\n')

with open('output.txt', 'r') as input_file, open('output.srt', 'w') as output_file:
    # Keep track of whether the previous line was empty
    previous_line_empty = False
    for line in input_file:
        # Strip any whitespace from the line
        line = line.strip()
        # Check if the line is empty
        if not line:
            # If the previous line was also empty, skip writing the first empty line
            if previous_line_empty:
                previous_line_empty = True
                continue
            # Otherwise, mark the current line as empty and write it to the output file
            else:
                previous_line_empty = True
                output_file.write(line + '\n')
        else:
            # If the line is not empty, write it to the output file and mark the previous line as not empty
            output_file.write(line + '\n')
            previous_line_empty = False

with open('output.srt', 'r') as input_file, open('final-apartment-tour-final.srt', 'w') as output_file:
    index = 1
    for line in input_file:
        if '-->' in line:
            # Add the index before the timestamp
            output_file.write(str(index) + '\n')
            output_file.write(line)
            index += 1
        else:
            output_file.write(line)




