import argparse
import os
import subprocess
import shutil

parser = argparse.ArgumentParser(
                    prog='Get ARJA-e Defects4J diffs',
                    )

parser.add_argument("-d", "--defects4JPath")
parser.add_argument("-e", "--ARJAePath")

args = parser.parse_args()

def get_project(bug_name : str) -> str:
    for project in os.scandir(f"{args.defects4JPath}/project_repos"):
        if bug_name.split("_")[0].lower() in project.name:
            return project.name
        

def checkout_project(project_name, bug_number):
    cmd_str = f"defects4j checkout -p {project_name} -v {bug_number}b -w ./current"
    subprocess.check_call(cmd_str.split(" "))

outDir = "ARJAe"
for bugFile in os.scandir(args.ARJAePath):
    try:
        if os.path.exists("current"):    
            shutil.rmtree("current")
        project_name = get_project(bugFile.name)
        d4j_name = bugFile.name.split("_")[0]
        bug_number =  bugFile.name.split("_")[1]
        short_diff_lines = ""
        with open(bugFile) as bfp:
            short_diff_lines = bfp.readlines()
        try:
            origFile = short_diff_lines[1].replace("\t"," ").split(" ")[1]
        except IndexError as e:
            continue
        origFile = f"current/{'/'.join(origFile.split('/')[1:])}"
        print(origFile  )
        checkout_project(d4j_name, bug_number)
        origSource = open(origFile).readlines()
        count = 0
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
        diff_code = short_diff_lines
        new_source = origSource
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
        out_dir = f"ARJAeTest/{project_name}"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        with open(f"{out_dir}/long_diff.patch", "w") as ldp:
            ldp.writelines(new_source)
        for i in range(len(short_diff)):
            short_diff_lines[i] = short_diff_lines[i] + "\n"
        with open(f"{out_dir}/short_diff.patch", "w") as sdp:
            sdp.writelines(short_diff_lines)
    except Exception as e:
        print(e)
        continue
    finally:
        if os.path.exists("current"):    
            shutil.rmtree("current")