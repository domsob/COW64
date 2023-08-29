import os
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser(
                    prog='Get Defects4J diffs',
                    )
parser.add_argument("-d", "--defects4JPath")

args = parser.parse_args()

def checkout_project(project_name, bug_number):
    cmd_str = f"defects4j checkout -p {project_name} -v {bug_number}b -w ./current"
    subprocess.call(cmd_str.split(" "))

def reverse_diff(diff):
    return subprocess.check_output(f"interdiff -q {diff} /dev/null".split(" ")).decode()

for patchFile in os.scandir("ARJAe"):
    try:
        if os.path.exists("current"):    
            shutil.rmtree("current")
        if os.path.exists(f"Human/{patchFile.name}"):
            continue
        d4j_name = patchFile.name.split("_")[0]
        bug_number =  patchFile.name.split("_")[1]
        bug_file = f"{args.defects4JPath}/framework/projects/{d4j_name}/patches/{bug_number}.src.patch"
        short_diff_lines = reverse_diff(bug_file).split("\n")
        hunks = []
        hunk = []
        for line in short_diff_lines:
            if line.startswith("@@ "):
                hunks.append(hunk)
                hunk = []
            hunk.append(line)
        if not hunk.__eq__([]):
            hunks.append(hunk)
        offset = 0
        try:
            origFile = hunks[0][0].replace("\t"," ").split(" ")[1]
        except IndexError as e:
            continue
        origFile = f"current/{'/'.join(origFile.split('/')[1:])}"
        

        checkout_project(d4j_name, bug_number)
        new_source = open(origFile).readlines()
        for short_diff in hunks[-1:0:-1]:
            for i in range(len(short_diff)):
                short_diff[i] = short_diff[i] + "\n"
            
            count = 0
            newOffset = 0
            for line in short_diff:
                if line.startswith("+"):
                    newOffset += 1
                if line.startswith("-"):
                    newOffset -= 1
                count += 1
                if line.startswith("@@"):
                    token = line.split(" ")[2].replace("-","").replace("+","")
                    tokens = token.split(",")
                    start = int(tokens[0])
                    tokens = token.split(",")
                    length  = int(tokens[1])
                    break
            diff_code = short_diff[count:]
            first = new_source[:start-1]
            last = new_source[start-1+length:]
            new_source = first + diff_code + last
            offset += newOffset
        out_dir = f"Human/{patchFile.name}"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        with open(f"{out_dir}/long_diff.patch", "w") as ldp:
            ldp.writelines(new_source)
        for i in range(len(short_diff_lines)):
            short_diff_lines[i] = short_diff_lines[i] + "\n"
        with open(f"{out_dir}/short_diff.patch", "w") as sdp:
            sdp.writelines(short_diff_lines)
    except:
        continue