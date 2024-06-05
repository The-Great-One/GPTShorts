import glob
import json
import ast
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

# Path to SRT files
srt_files = glob.glob('Generated_Files/out_*.srt')

# Function to analyze SRT file
def analyze_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''
As an expert video editor, your task is to analyze a timescript (.srt) file and identify segments that have the potential to go viral. Follow these guidelines:

    Segment Duration: Each segment should be between 15 to 60 seconds long.
    Content Continuity: Extract continuous segments that form a complete speech or coherent narrative. Avoid using single sentences.
    Exclusions: Do not include introductory or overly generic speeches. Focus on engaging and impactful content.
    Selection Criteria: Choose segments that are emotional, informative, or humorous to capture attention quickly.
    Combination of Timestamps: Combine multiple continuous lines to form the complete segment if needed.
    Complete Analysis: Analyze the entire file and provide the maximum number of segments that meet the criteria. Do not limit the number to 4-5 segments.
    Viewer Impact: Ensure the segments are meaningful and provide valuable content to the viewers, so they get something substantial after watching.

Powerful Conversation Cues:

To identify key segments, consider the following:

    Thesis Statements: Look for opening statements or restatements like "I'd like to discuss..." or "In essence..."
    Counterarguments: Look for concessions or objections like "That's a valid point, however..." or "I disagree with..."
    Supporting Evidence: Look for statistics, expert opinions, or examples like "According to a recent study..." or "As [expert name] points out..."
    Logical Reasoning: Look for cause & effect, analogies, or hypotheticals like "because," "It's like..." or "Imagine a scenario..."
    Emotional Appeals: Look for personal stories, appeals to values, or figurative language like "This is a matter of..." or vivid descriptions.

For each selected segment, provide the following in the specified format and no other text:

{ "start_time": "start_time_value", "end_time": "end_time_value", "duration": "duration_value", "script": "script_value", "title": "title_value", "caption": "caption_value" }

Example format for your response:

{ "start_time": "97.19", "end_time": "127.43", "duration": "30", "script": "And that was the moment I realized everything was about to change. The decision I made that day was the turning point, leading me to where I am now. It's incredible how a single choice can have such a profound impact on your life.", "title": "The Turning Point of My Life", "caption": "🌟 The Turning Point of My Life 🌟 Sometimes, a single choice can change everything. Here's the moment that transformed my journey and led me to where I am now. 🚀✨ #LifeChangingMoment #PersonalGrowth #Inspiration #Motivation #TurningPoint #TransformYourLife #DecisionsMatter #LifeJourney #ViralVideo #Empowerment #SpeakerName" }

By following these guidelines, you will identify segments that maximize engagement and have the potential to become viral.
'''
            },
            {
                "role": "user",
                "content": srt_content,
            }
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content

def GPT_Analyser():
    # Process each SRT file
    all_timestamps = []
    for srt_file in srt_files:
        print(f"Analyzing {srt_file}")
        result = analyze_srt(srt_file)
        all_timestamps.append(result)

    # Save raw results to JSON file
    with open('Generated_Files/raw_data.json', 'w') as f:
        json.dump(all_timestamps, f, indent=4)

    # Clean and reformat the JSON data
    cleaned_data = []
    for item in all_timestamps:
        try:
            item = item.replace("json", "").replace("```", "").replace("\n", "").replace("}{", "},{")       
            segments = ast.literal_eval(item)
            cleaned_data.extend(segments)
        except Exception as e:
            print(f"Error processing item: {item}, Error: {e}")

    # Save cleaned data to JSON file
    with open('Generated_Files/data.json', 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    print("Data has been processed and saved to data.json")