from helper_functions import get_subfolder_names


folder1_path = "ARJAe"
folder2_path = "Human"

def compare_folders(folder1, folder2):
    subfolders1 = set(get_subfolder_names(folder1))
    subfolders2 = set(get_subfolder_names(folder2))
    common_folders = subfolders1 & subfolders2
    unique_folders_folder1 = subfolders1 - subfolders2
    unique_folders_folder2 = subfolders2 - subfolders1
    return list(common_folders), list(unique_folders_folder1), list(unique_folders_folder2)

if __name__ == "__main__":

    common_folders, unique_folders_folder1, unique_folders_folder2 = compare_folders(folder1_path, folder2_path)

    print("Common: " + str(common_folders))
    print("Only in folder 1: " + str(unique_folders_folder1))
    print("Only in folder 2: " + str(unique_folders_folder2))
