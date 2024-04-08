import os
import gzip
import csv

import osFunctions

LOGS_DIR = "logs"
JOIN = " joined the game"
LEAVE = " left the game"

on_off_log = []

# Handling missing logs
logsExist = osFunctions.check_for_directory(LOGS_DIR, fail_response=f"No logs directory found, please upload your .log.gz files to '{LOGS_DIR}'")
if logsExist:
    if os.listdir(LOGS_DIR) == []:
        osFunctions.quit(f"No regions found in '{LOGS_DIR}', please upload at least one .log.gz file and try again")
else:
    osFunctions.quit("")

for gunzip_name in os.listdir(LOGS_DIR): # Iterate through every gunzip file
    gunzip = gzip.open("logs/" + gunzip_name) # Open the file
    contents = gunzip.read() # Read the file
    split_contents = str(contents).split(r"\r\n") # Split into an array where each item is a line
    for line in split_contents: # Iterating through every line of the file
        split_line = line.split(":") # Allowing us to trim off all the stuff at the start

        trim_line = split_line[len(split_line)-1] # And pick out just the last bit, which is what we're interested in
        if JOIN in trim_line:
            activity = True
            username = trim_line.replace(JOIN, "").lstrip()
        elif LEAVE in trim_line:
            activity = False
            username = trim_line.replace(LEAVE, "").lstrip()
        else:
            continue

        date = gunzip_name.split("-")
        timestamp = f"{date[0]}/{date[1]}/{date[2]} {split_line[0].lstrip("[")}:{split_line[1]}:{split_line[2][:2]}"
        on_off_log.append((timestamp, username, activity))
        print((timestamp, username, activity))

file = open("data.csv", "w", newline="")
writer = csv.writer(file)
for log in on_off_log:
    writer.writerow(log)
file.close()