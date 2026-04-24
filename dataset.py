import kagglehub
import shutil
import os

# Download latest version
path = kagglehub.dataset_download("terminus7/pokemon-challenge")

print("Original path to dataset files:", path)

# Skopiowanie pobranych plików do lokalnego folderu 'dataset'
target_dir = "dataset"
os.makedirs(target_dir, exist_ok=True)
shutil.copytree(path, target_dir, dirs_exist_ok=True)

print(f"Files copied to directory: {target_dir}")