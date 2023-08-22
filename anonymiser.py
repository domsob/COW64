import random
import shutil
import os
from helper_functions import get_subfolder_names, create_directory_if_not_exists, get_files_in_folder_and_subfolder


random.seed(42)    # Change this seed here! 

input_folder = 'responses'
output_folder = 'responses_anon'
tracking_filename = 'anon_tracking_file.csv'

if __name__ == '__main__':

    if os.path.exists(output_folder):
        print('responses_anon folder already exists. Please delete it before running this script.')
        exit()
    else:
        os.makedirs(output_folder)

    tracking_file_contents = 'original_path;anonymised_path' + '\n'

    problem_list = [x for x in get_subfolder_names(input_folder) if not x.endswith('human') and not x.endswith('generated')]

    for problem in problem_list:
        current_problem_files = get_files_in_folder_and_subfolder(input_folder + '/' + problem)
        anon_letters = ['a', 'b']
        random.shuffle(anon_letters)
        for problem_file in current_problem_files:
            create_directory_if_not_exists(output_folder + '/' + problem)
            run_number = problem_file.split('/')[-1].split('_')[0]
            if '_human_' in problem_file:
                shutil.copy(problem_file, output_folder + '/' + problem + '/' + anon_letters[0] + '_' + run_number + '.txt')
                tracking_file_contents += problem_file + ';' + output_folder + '/' + problem + '/' + anon_letters[0] + '_' + run_number + '.txt' + '\n'
            else:
                shutil.copy(problem_file, output_folder + '/' + problem + '/' + anon_letters[1] + '_' + run_number + '.txt')
                tracking_file_contents += problem_file + ';' + output_folder + '/' + problem + '/' + anon_letters[1] + '_' + run_number + '.txt' + '\n'

    with open(tracking_filename, 'w') as file:
        file.write(tracking_file_contents)  
