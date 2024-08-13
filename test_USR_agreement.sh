#!/bin/sh
#!/bin/sh
import os

directory = "/Users/fatema/Desktop/workspace/LanguageCommunicator/hindi_gen_feb_09/hindi_gen/inter_annotator"  # replace with the full path to the directory

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        base = os.path.splitext(filename)[0]
        newname = os.path.join(directory, base)
        os.rename(os.path.join(directory, filename), newname)
