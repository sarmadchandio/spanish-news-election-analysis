import os
import json
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import multiprocessing as mp


PATH = 'candidates_csvs/'


def collect_transcripts(candidate, videos):
    transcript_dict = {}
    for i, vid_id in enumerate(videos):
        # We are assuming there are no "yt-shorts" in the list of videos
        # vid_id = vid.split('v=')[1]                
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid_id, languages=['es'])
            formatter = TextFormatter()
            # .format_transcript(transcript) turns the transcript into a String.
            string_formatted = formatter.format_transcript(transcript)
            transcript_dict[vid_id] = string_formatted
        
        except Exception as e:
            # print(e)
            transcript_dict[vid_id] = 'transcript_disabled'
        

        if i % 100 == 0:
            print(f'{candidate:<15}  Video {i+1:>4}/{len(videos):<4}', flush=True)


    
    with open(f'data/transcripts/{candidate}.json', 'w') as outfile:
        json.dump(transcript_dict, outfile, indent=2)
        

if __name__ == '__main__':
    processes = []
    for filename in os.listdir(PATH):
        if filename.endswith('.csv'):
            candidate = filename.split('.csv')[0].split('_')[0].replace(' ', '_').lower()
            if candidate+'.json' in os.listdir('data/transcripts/'):
                print(f'{candidate} already exists. Skipping...')
                continue
            df = pd.read_csv(f'{PATH}{filename}')
            # the 3rd column is the list of video ids
            videos = df.iloc[:, 2].tolist()
            # print(f'Candidate: {candidate}')
            # print(f'Videos: {videos}')

            # use multiprocessing to speed up the process
            p = mp.Process(target=collect_transcripts, args=(candidate, videos))
            p.start()
            processes.append(p)

    for process in processes:
        process.join()

    print('Done!')





            
            