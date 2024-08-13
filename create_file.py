import os

if __name__ == "__main__":
    directory = "/Users/fatema/Desktop/workspace/LanguageCommunicator/hindi_gen_feb_09/hindi_gen/Test_data/week3"

    # create files named 1.txt, 2.txt, ..., 20.txt in the directory
    for i in range(1, 50):
        filename = os.path.join(directory, f"{i}.txt")
        with open(filename, "w") as file:
            file.write(f" ")

