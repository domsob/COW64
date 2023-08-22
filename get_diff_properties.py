from helper_functions import get_subfolder_names, remove_java_comments


generated_folder = 'ARJAe'
human_folder = 'Human'
threshold = 1500

def print_files_loc(problem_name, problem_list, folder_name, threshold_def, type_def, use_threshold=True, print_header=True):
    if use_threshold:
        print('Threshold for ' + type_def + ' is ' + str(threshold_def) + ' LOC:')
    if print_header:
        print('Type,Bug,LOC')
    for problem_name in problem_list:
        with open(folder_name + '/' + problem_name + '/long_diff.patch', "r") as file:
            contents = file.read()

        contents = remove_java_comments(contents.strip())
        if len(contents.split('\n')) > threshold_def or use_threshold == False:
            print(type_def + ',' + problem_name + ',' + str(len(contents.split('\n'))))

def print_num_affected_lines(problem_name, problem_list, folder_name, type_def, print_header=True):
    if print_header:
        print('Type,Bug,Affected_lines')
    for problem_name in problem_list:
        with open(folder_name + '/' + problem_name + '/long_diff.patch', "r") as file:
            contents = file.read()
            lines = contents.split('\n')
            counter = 0
            for line in lines:
                if line.startswith('+  ') or line.startswith('-  '):
                    counter += 1
            print(type_def + ',' + problem_name + ',' + str(counter))

if __name__ == "__main__":

    generated_problems = get_subfolder_names(generated_folder)
    human_problems = get_subfolder_names(human_folder)

    # print_files_loc(generated_folder, generated_problems, generated_folder, threshold, 'Generated', False, True)
    # print_files_loc(human_folder, human_problems, human_folder, threshold, 'Human', False, False)

    print_num_affected_lines(generated_folder, generated_problems, generated_folder, 'Generated', True)
    print_num_affected_lines(human_folder, human_problems, human_folder, 'Human', False)


