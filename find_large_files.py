from helper_functions import get_subfolder_names, remove_java_comments


generated_folder = 'ARJAe'
human_folder = 'Human'
threshold = 1500

def print_large_files(problem_name, problem_list, folder_name, threshold_def, type_def):
    for problem_name in problem_list:
        with open(folder_name + '/' + problem_name + '/long_diff.patch', "r") as file:
            contents = file.read()

        contents = remove_java_comments(contents.strip())
        if len(contents.split('\n')) > threshold_def:
            print(type_def, problem_name, len(contents.split('\n')))

if __name__ == "__main__":

    generated_problems = get_subfolder_names(generated_folder)
    human_problems = get_subfolder_names(human_folder)

    print_large_files(generated_folder, generated_problems, generated_folder, threshold, 'Generated')
    print_large_files(human_folder, human_problems, human_folder, threshold, 'Human')


