#!/usr/bin/env python3

import os
import shutil
import cv2
from PIL import Image
import pytesseract
# from gpt4all import GPT4All
from typing import Dict
import pandas as pd

import evadb

from pytube import YouTube, extract  # noqa: E402
from youtube_transcript_api import YouTubeTranscriptApi  # noqa: E402

MAX_CHUNK_SIZE = 10000
# temporary file paths
MENU_PATH = os.path.join("evadb_data", "tmp", "menu.csv")


def receive_user_input():
    username = str(
        input("What's your name?\n")
    )
    print(f"Welcome {username}!\n")

def download_youtube_video_transcript(video_link: str):
    """Downloads a YouTube video's transcript.

    Args:
        video_link (str): url of the target YouTube video.
    """
    video_id = extract.video_id(video_link)
    print("⏳ Transcript download in progress...")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print("✅ Video transcript downloaded successfully.")
    return transcript

def group_transcript(transcript: dict):
    """Group video transcript elements when they are too short.

    Args:
        transcript (dict): downloaded video transcript as a dictionary.

    Returns:
        str: full transcript as a single string.
    """
    new_line = ""
    for line in transcript:
        new_line += " " + line["text"]

    return new_line

def partition_transcript(raw_transcript: str):
    """Group video transcript elements when they are too large.

    Args:
        transcript (str): downloaded video transcript as a raw string.

    Returns:
        List: a list of partitioned 
        transcript
    """
    if len(raw_transcript) <= MAX_CHUNK_SIZE:
        return [{"text": raw_transcript}]

    k = 2
    while True:
        if (len(raw_transcript) / k) <= MAX_CHUNK_SIZE:
            break
        else:
            k += 1
    chunk_size = int(len(raw_transcript) / k)

    partitioned_transcript = [
        {"text": raw_transcript[i : i + chunk_size]}
        for i in range(0, len(raw_transcript), chunk_size)
    ]
    if len(partitioned_transcript[-1]["text"]) < 30:
        partitioned_transcript.pop()
    return partitioned_transcript

def cleanup():
    """Removes any temporary file / directory created by EvaDB."""
    if os.path.exists("evadb_data"):
        shutil.rmtree("evadb_data")

if __name__ == "__main__":
    # llm = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
    # llm = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
    cursor = evadb.connect().cursor()
    api_key = str(input("🔑 Enter your OpenAI key: "))
    os.environ["OPENAI_KEY"] = api_key
    img_file = "image/menu4.jpg"
    img = Image.open(img_file)
    ocr_result = pytesseract.image_to_string(img)
    print(ocr_result)
    content = [{"text": ocr_result}]    
    df = pd.DataFrame(content)
    df.to_csv(MENU_PATH)

    # load chunked transcript into table
    cursor.drop_table("Menu", if_exists=True).execute()
    cursor.query(
        """CREATE TABLE IF NOT EXISTS Menu (text TEXT(50));"""
    ).execute()
    cursor.load(MENU_PATH, "Menu", "csv").execute()

    question = f""" Give me a list of words that appear on the given text and are related to the following: food, ingredients, cooking-style.
    No repeated items.
    """

    if len(cursor.table("Menu").select("text").df()["menu.text"]) == 1:
        print("Capoo")
        print(cursor.table("Menu")
            .select(f"ChatGPT('{question}', text)")
            .df()["chatgpt.response"][0])

    cleanup()

    print("done")

    # response = llm.generate(question)
    # print(response)



# if __name__ == "__main__":
#     llm = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
#     # receive_user_input()
#     # response = llm.generate("What is the 7 wonders of the world?")
#     # print(response)
#     transcript = download_youtube_video_transcript("https://www.youtube.com/watch?v=StwHvQuT9pI")
#     # print(transcript)

#     try:
#         # establish evadb api cursor
#         cursor = evadb.connect().cursor()

#         raw_transcipt = None

#         if transcript is not None:
#             raw_transcript_string = group_transcript(transcript)

#         if raw_transcript_string is not None:
#             partitioned_transcript = partition_transcript(raw_transcript_string)
#             df = pd.DataFrame(partitioned_transcript)
#             df.to_csv(TRANSCRIPT_PATH)

#         # load chunked transcript into table
#         cursor.drop_table("Transcript", if_exists=True).execute()
#         cursor.query(
#             """CREATE TABLE IF NOT EXISTS Transcript (text TEXT(50));"""
#         ).execute()
#         cursor.load(TRANSCRIPT_PATH, "Transcript", "csv").execute()

#         content = cursor.table("Transcript").select("text").df()["transcript.text"][0]
#         if len(cursor.table("Transcript").select("text").df()["transcript.text"]) == 1:
#             print("Printing content...\n")
#             print(content)
#             print(type(content))
#             # question = f""" Given the following transcript from a youtube video: {content}
#             # What is the video about?
#             # """
#             # response = llm.generate(question)
#             # print("Response:\n")
#             # print(response)
#         else:
#             print("Ooooops")
#     except Exception as e:
#         print("Session ended with error.")
#         print(e)

    