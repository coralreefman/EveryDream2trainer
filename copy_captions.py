import os
import shutil
from pathlib import Path

def process_files(dir_path, process_function, log_file='process_log.txt', *args, **kwargs):
    """
    General function to process files in a directory with a given processing function, logs files without specified strings.

    Args:
    - dir_path: The path to the directory containing files.
    - process_function: The function to apply to the content of each file.
    - log_file: Path to the log file where paths of files that do not contain specified strings will be written.
    - args, kwargs: Arguments and keyword arguments for the processing function.
    """
    path = Path(dir_path)
    with open(log_file, 'w') as log:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = Path(root) / file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if any string is not found, and if so, log the file path
                    if 'strings_to_remove' in kwargs and not any(s in content for s in kwargs['strings_to_remove']):
                        log.write(f"{file_path}\n")

                    # Apply the specified processing function
                    modified_content = process_function(content, *args, **kwargs)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

def replace_characters(text, replace_newline=True, dot_rule=True):
    """
    Replace specific characters in text based on the given rules.

    Args:
    - text: The input text to process.
    - replace_newline: Boolean, whether to replace newlines with ', '.
    - dot_rule: Boolean, whether to replace '.' with ',' unless preceded by a capital letter.
    """
    result = []
    i = 0
    while i < len(text):
        if text[i] == '.' and dot_rule:
            if i > 0 and text[i-1].isupper():
                result.append('.')
            else:
                result.append(',')
        elif text[i] == '\n' and replace_newline:
            result.append(', ')
        else:
            result.append(text[i])
        i += 1

    return ''.join(result)

def remove_strings(text, strings_to_remove):
    """
    Remove specified strings from the text.

    Args:
    - text: The input text to process.
    - strings_to_remove: List of strings to remove from the text.
    """
    for string in strings_to_remove:
        text = text.replace(string, "")
    return text

# def remove_strings_from_files(dir_path, strings_to_remove):
#     # Create a Path object for the directory
#     path = Path(dir_path)

#     # Walk through the directory
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file.endswith('.txt'):
#                 # Construct the full file path
#                 file_path = Path(root) / file
                
#                 # Read the content of the file
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
                
#                 # Remove the specified strings
#                 for string in strings_to_remove:
#                     content = content.replace(string, "")
                
#                 # Write the updated content back to the file
#                 with open(file_path, 'w', encoding='utf-8') as f:
#                     f.write(content)

def copy_txt_files_with_structure(source_dir, destination_dir):
    # Create a Path object for source and destination directories
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_path):
        for file in files:
            # Check if the file ends with .txt
            if file.endswith('.txt'):
                # Construct the full file path
                file_path = Path(root) / file
                # Create a relative path to maintain the directory structure
                relative_path = file_path.relative_to(source_path)
                # Create the destination file path
                destination_file_path = destination_path / relative_path
                
                # Ensure the destination directory exists
                destination_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file to the destination
                shutil.copy(file_path, destination_file_path)

def copy_jpg_files_with_structure(source_dir, destination_dir):
    # Create Path objects for the source and destination directories
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith('.jpg'):  # Check if the file is a JPEG
                # Construct the full file path
                file_path = Path(root) / file
                # Create a relative path to maintain the directory structure
                relative_path = file_path.relative_to(source_path)
                # Create the destination file path
                destination_file_path = destination_path / relative_path

                # Ensure the destination directory exists
                destination_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file to the destination
                shutil.copy(file_path, destination_file_path)

def copy_images_and_text_to_single_folder(source_dir, destination_dir):
    # Supported image formats and text files
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    text_extension = '.txt'

    # Create Path objects for the source and destination directories
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    # Ensure the destination directory exists
    destination_path.mkdir(parents=True, exist_ok=True)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_path):
        for file in files:
            # Check file extension
            if file.lower().endswith(tuple(image_extensions)) or file.lower().endswith(text_extension):
                # Construct the full file path
                file_path = Path(root) / file
                # Create the destination file path (not preserving the directory structure)
                destination_file_path = destination_path / file

                # Check if file already exists to prevent overwriting
                if not destination_file_path.exists():
                    # Copy the file to the destination
                    shutil.copy(file_path, destination_file_path)
                else:
                    # If file exists, rename and copy
                    base, extension = os.path.splitext(file)
                    counter = 1
                    new_file = f"{base}_{counter}{extension}"
                    new_destination_file_path = destination_path / new_file
                    while new_destination_file_path.exists():
                        counter += 1
                        new_file = f"{base}_{counter}{extension}"
                        new_destination_file_path = destination_path / new_file
                    shutil.copy(file_path, new_destination_file_path)

def sync_text_files(folder_a, folder_b):
    """
    For each image in folder A, if a corresponding .txt file exists in folder B,
    copy it to the corresponding location in folder A.
    """
    # Create a set of image file extensions to look for
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}

    # Walk through folder A to find all image files
    for root, dirs, files in os.walk(folder_a):
        for file in files:
            # Check if the file is an image
            if Path(file).suffix.lower() in image_extensions:
                # Construct the base name to match .txt files
                base_name = Path(file).stem
                
                # Walk through folder B to find corresponding .txt files
                for b_root, b_dirs, b_files in os.walk(folder_b):
                    for b_file in b_files:
                        if Path(b_file).stem == base_name and Path(b_file).suffix == '.txt':
                            # Construct source path in folder B
                            source_path = Path(b_root) / b_file
                            # Construct target path in folder A with the same relative path
                            relative_path = Path(b_root).relative_to(folder_b)
                            target_path = Path(root) / relative_path / b_file
                            # Make sure the target directory exists
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            # Copy file from folder B to folder A
                            shutil.copy(source_path, target_path)
                            print(f"Copied '{source_path}' to '{target_path}'")


# remove newlines / replace with ',''. replace '.' with ','
# if none of the strings to remove are in there , add filename to a new list

strings_to_remove = [
    "1. Medium: ",
    "2. Subject Matter: ",
    "3. Colors: ",
    "4. Composition: ",
    "5. Brushstrokes: ",
    "5. Keywords: ",
    "6. Time Period:",
    "5. Influences:",
]

source_directory = '/home/studio/Code/image_tools/output'
destination_directory = '/home/studio/Desktop/captions'

# copy_txt_files_with_structure(source_directory, destination_directory)
# remove_strings_from_files(destination_directory, strings_to_remove)
# copy_jpg_files_with_structure(source_directory, destination_directory)
copy_images_and_text_to_single_folder(destination_directory, "/home/studio/HOME0001 Dropbox/Carl Rethmann/StudioCKT/painting-dataset-captions-18-04-24")

process_files(source_directory, replace_characters)  # for character replacement
process_files(source_directory, remove_strings, strings_to_remove)  # for string removal
