"""Check all folders in the provided directory for any that are above 10,000 files"""
import csv
import os
import sys

input_dir = sys.argv[1]

log_path = os.path.join(input_dir, 'file_count_check.csv')
with open(log_path, 'w', newline='') as log:
    log_writer = csv.writer(log)
    log_writer.writerow(['Folder', 'Files', 'Files_OK'])

for folder_name in os.listdir(input_dir):
    # Skips metadata files.
    if folder_name.endswith('.csv'):
        continue
    
    # Gets the number of files at all levels.
    file_count = 0 
    for root, dirs, files in os.walk(os.path.join(input_dir, folder_name)):
       file_count += len(files)
   
    # Saves size information to a log, including comparing it to the desired maximum.
    with open(log_path, 'a', newline='') as log:
        log_writer = csv.writer(log)
        log_writer.writerow([folder_name, file_count, file_count < 10000])