import argparse
import subprocess
import os
import yaml

def main():
    parser = argparse.ArgumentParser(description="grade some CODE dude let's GO")
    parser.add_argument('src', help="path to the directory with all students' code")
    parser.add_argument('template', help="path to template text file for reports; should be a YAML file with each line as '<string key>:<int val>'")
    parser.add_argument('tester', help="path to python file to pass individual repo to")
    parser.add_argument('output', help="path to dir for report outputs and progress record")
    parser.add_argument('-v', '--verbose', help="more print statements", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        print("Received the following args:")
        print(f"\tsrc:{args.src}")
        print(f"\ttemplate:{args.template}")
        print(f"\ttester:{args.tester}")
        print(f"\toutput:{args.output}")
        print(f"\tverbose:{args.verbose}")

    if args.verbose:
        print('Opening src directory...')

    path, dirs, files = next(os.walk(args.src))

    if args.verbose:
        print(f"\tsrc dir name: {path}")
        print(f"\tFound {len(dirs)} directories and {len(files)} files.")

    if args.verbose:
        print("Loading report template...")

    grades_template = yaml.load(open(args.template, 'r'))
    assert isinstance(grades_template, dict)
    max_grade = sum(list(grades_template.values()))

    if args.verbose:
        print("\tloaded the following data from YAML file: ")
        print('\t'+str(grades_template))
        print('\t maximum possible grade: ' + str(max_grade))

    if args.verbose:
        print("Syncing dirs list with existing reports in output directory...")

    path1, dirs1, files1 = next(os.walk(args.output))
    for name in [f.split('.')[0] for f in files1]:
        dirs.remove(name)

    if args.verbose:
        print(f"\t{len(files1)} reports found, {len(dirs)} dirs remaining to grade")

    if args.verbose:
        print("\nStarting grading loop...")

    while True:
        curr = dirs.pop(0)

        grades = {}
        for k in grades_template.keys():
            grades[k] = 0

        print("\n\n CURRENT DIRECTORY: " + curr)

        decision = str(input("run tester on dir (y/n)? 'n' will skip to next... "))
        if decision in ['y','Y']:
            pass
        elif decision in ['n','N']:
            continue
        else:
            print('Could not understand input, stopping...')
            return

        cmd = "python " + args.tester + " " + os.path.join(args.src, curr)
        p = subprocess.Popen(cmd)
        p.wait()

        student_identifier = str(input("Enter the current student's identifier: "))

        for k in grades.keys():
            q = f"grade for {k} out of {grades_template[k]} (use ':' to add a note)? "
            while True:
                grade_input = str(input(q)).split(':')
                try:
                    if len(grade_input) == 1:
                        grades[k] = (grade_input[0], "")
                    elif len(grade_input) == 2:
                        grades[k] = (grade_input[0],grade_input[1])
                    break
                except e:
                    print('bad grade input... please try again')

        total_grade = sum([float(x[0]) for x in grades.values()])

        print("Final grades:")
        for k,v in grades.items():
            print('\t',k,v)
        print(f"Final grade: {total_grade}/{max_grade}")

        while True:
            decision = str(input("'g' to generate report and move on\n'n' to write a note and then generate report and move on\n'r' to retest and regrade\n's' to skip report generation and move on\n"))
            if decision in ['g','G']:
                outfile = os.path.join(args.output, curr+'.txt')
                gen_report(outfile,grades,student_identifier,"",grades_template)
                break
            elif decision in ['n','N']:
                note = str(input('\tnote: '))
                outfile = os.path.join(args.output, curr+'.txt')
                gen_report(outfile,grades,student_identifier,note,grades_template)
                break
            elif decision in ['r','R']:
                dirs.insert(0,curr)
                break
            elif decision in ['s','S']:
                break
            else:
                print("Couldn't understand your input...")

    print("Done grading! Nice job!")
        

def gen_report(filename, grades, student_id, note, template):
    f = open(filename, 'x')
    lines = [student_id,'\n\n']
    for k in grades.keys():
        grade,n= grades[k]
        line = f"{k}: {grade}/{template[k]}"
        if n:
            line += " | " + n
        line +='\n'

        lines.append(line)

    total = sum([float(x[0]) for x in grades.values()])
    max_grade = sum(list(template.values()))

    lines.append('\n')
    lines.append(f"Total grade: {total}/{max_grade}")
    if note:
        lines.append('\n')
        lines.append('Notes: ' + note)

    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    main()