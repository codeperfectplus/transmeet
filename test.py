# cython: language_level=3
import os
from pathlib import Path

filepath = "/home/admin/Documents/MeetingSummarizer/transmeet/clients/transcription_client.py"

# get the file name from the path
filename = Path(filepath).stem
# remove extension
print(filename)