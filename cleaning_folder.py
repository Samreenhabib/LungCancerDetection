import os
import pandas as pd
import shutil

def find_subfolder_with_keyword(root_folder, keyword):
    matching_folders = {}
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path) and keyword.lower() in folder_name.lower():
            folder_name = os.path.basename(root_folder)
            if folder_name not in matching_folders:
                matching_folders[folder_name] = []
            matching_folders[folder_name].append(folder_path)

    return matching_folders

def delete_thorax_folders(root_folder):
    keyword = "thorax"
    thorax_folder = {}
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path):
            matching_folders = find_subfolder_with_keyword(folder_path, keyword)
            if matching_folders:
                for folder_name, folder_paths_to_delete in matching_folders.items():
                    for folder_path_to_delete in folder_paths_to_delete:
                        shutil.rmtree(folder_path_to_delete)
                        print(f"Deleted folder: {folder_path_to_delete}")
                    thorax_folder.setdefault(folder_name, []).extend(folder_paths_to_delete)
        else:
            print(f"Ignored file: {folder_path}")

    return thorax_folder

if __name__ == "__main__":
    root_folder = "patient_data-1"
    deleted_thorax_folders = delete_thorax_folders(root_folder)
    
    print("All matching folders:")
    print(deleted_thorax_folders)




# import os
# import pandas as pd
# import shutil

# def find_subfolder_with_keyword(root_folder, keyword):
#     matching_folders = {}
#     for folder_name in os.listdir(root_folder):
#         folder_path = os.path.join(root_folder, folder_name)
#         if os.path.isdir(folder_path) and keyword.lower() in folder_name.lower():
#             folder_name = os.path.basename(root_folder)
#             matching_folders[folder_name] = folder_path

#     return matching_folders

# if __name__ == "__main__":
#     root_folder = "patient_data-1"
#     thorax_folder = {}

#     for folder in os.listdir(root_folder):
#         folder_path = os.path.join(root_folder, folder)
#         if os.path.isdir(folder_path):
#             keyword = "thorax"
#             matching_folders = find_subfolder_with_keyword(folder_path, keyword)
#             if matching_folders:
#                 # Delete folders that contain 'thorax' in their filename
#                 for _, folder_path_to_delete in matching_folders.items():
#                     shutil.rmtree(folder_path_to_delete)
#                     print(f"Deleted folder: {folder_path_to_delete}")
#                 thorax_folder.update(matching_folders)


# import os
# import pandas as pd

# def find_subfolder_with_keyword(root_folder, keyword):
#     matching_folders = {}
#     for folder_name in os.listdir(root_folder):
#         folder_path = os.path.join(root_folder, folder_name)
#         if os.path.isdir(folder_path) and keyword.lower() in folder_name.lower():
#             folder_name = os.path.basename(root_folder)
#             matching_folders[folder_name] = folder_path

#     return matching_folders

# if __name__ == "__main__":
#     root_folder = "patient_data-1"
#     thorax_folder = {}

#     for folder in os.listdir(root_folder):
#         folder_path = os.path.join(root_folder, folder)
#         if os.path.isdir(folder_path):
#             keyword = "thorax"
#             matching_folders = find_subfolder_with_keyword(folder_path, keyword)
#             if matching_folders:
#                     thorax_folder.update(matching_folders)
    
#     print("All matching folders:")
#     print(thorax_folder)

#     # Convert dictionary to pandas DataFrame
#     df = pd.DataFrame(list(thorax_folder.items()), columns=["Parent Folder", "Matching Subfolder"])

#     # Save DataFrame to Excel
#     excel_file = "matching_thorax_folders.xlsx"
#     df.to_excel(excel_file, index=False)

#     print(f"Data saved to {excel_file}.")