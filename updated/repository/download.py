# from datasets import load_dataset

# # Load the Hindi dataset in streaming mode
# hindi_dataset = load_dataset("allenai/c4", "hi", split="train", streaming=True)

# # Specify the path to save the dataset locally
# save_path_hi = "c4_hi.txt"  # Change this to your desired path

# # Download and save the dataset line by line
# with open(save_path_hi, "w", encoding="utf-8") as file:
#     for entry in hindi_dataset:
#         file.write(f"{entry}\n")  # Write each entry to the file

# print(f"Hindi dataset saved to: {save_path_hi}")
# from datasets import load_dataset

# dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/hin")

from datasets import load_dataset

# Load the dataset
dataset = load_dataset("ai4bharat/sangraha", data_dir="verified/hin")

# Specify the local path where you want to store the dataset
save_path = "/home/user/varsh/dataset_hi/c4_hi.txt"

# Save the dataset locally

dataset.save_to_disk(save_path)

print(f"Dataset saved to: {save_path}")
