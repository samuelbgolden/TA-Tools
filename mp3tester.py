import argparse
import os
import yaml
import shutil
import subprocess


def main():

    TESTING_ENV = "C:/Users/samgo/src/samuelbgolden/TA-Tools/mp3-tester"

    # add dir arg
    parser = argparse.ArgumentParser(description="grades MP3 of CS340 S21")
    parser.add_argument('dir', help="path to directory with the student code")
    parser.add_argument('-p', '--printsrc',
                        help='print students code?', action='store_true')
    args = parser.parse_args()

    # construct paths to needed files
    yaml_file = os.path.join(args.dir, 'package.yaml')
    src_file1 = os.path.join(args.dir, 'src/MP3a.hs')
    src_file2 = os.path.join(args.dir, 'src/MP3b.hs')
    test_file = os.path.join(args.dir, 'test/MP3Spec.hs')

    # check that those files exist
    if not os.path.exists(yaml_file):
        print(f"Could not find yaml file at {yaml_file}")
        return

    if not os.path.exists(src_file1):
        print(f"Could not find MP3a.hs at {src_file1}")
        return

    if not os.path.exists(src_file2):
        print(f"Could not find MP3b.hs at {src_file2}")
        return

    if not os.path.exists(test_file):
        print(f"Could not find MP3Spec.hs at {test_file}")
        return

    # opening files in sublime
    p = subprocess.Popen(
        f"code {src_file1} {src_file2} {test_file}", shell=True)

    # load yaml data to get student info
    yaml_data = yaml.safe_load(open(yaml_file, 'r'))
    print(
        f"student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")

    # copy file from original location to testing environment
    testing_dest = os.path.join(TESTING_ENV, 'src')
    shutil.copy(src_file1, testing_dest)
    shutil.copy(src_file2, testing_dest)

    if args.printsrc:
        # printing code
        print("******************** FILE SRC MP2a ********************\n")
        code = open(src_file1, 'r')
        for line in code.readlines():
            print('/t' + line, end='')

        print("******************** FILE SRC MP2b ********************\n")
        code = open(src_file2, 'r')
        for line in code.readlines():
            print('/t' + line, end='')

        print("\n****************** END FILE SRC ******************")

    # run tests
    print("\nRunning 'stack build'..............................\n")
    p1 = subprocess.Popen(
        "stack build", cwd=os.path.abspath(TESTING_ENV), shell=True)
    p2 = subprocess.Popen(
        "stack build", cwd=os.path.abspath(args.dir), shell=True)
    p1.wait()
    p2.wait()

    print("\nRunning student and tester tests.....................\n")
    print("\n\n========================= TESTER =========================")
    p1 = subprocess.Popen(f"echo {yaml_data['author']} & echo TESTER & stack test", cwd=os.path.abspath(
        TESTING_ENV), shell=True)
    p1.wait()
    print("\n\n========================= STUDENT TESTS =========================")
    p2 = subprocess.Popen(
        f"echo {yaml_data['author']} & echo STUDENT & stack test --coverage", cwd=os.path.abspath(args.dir), shell=True)
    p2.wait()
    print("\n\n========================= EXEC =========================")
    p3 = subprocess.Popen(f"echo {yaml_data['author']} & echo EXEC & stack exec mp3 10000", cwd=os.path.abspath(
        TESTING_ENV), shell=True)
    p3.wait()

    # remove copied file from testing environment
    os.remove(os.path.join(testing_dest, 'MP3a.hs'))
    os.remove(os.path.join(testing_dest, 'MP3b.hs'))

    print(
        f"\nDone testing student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")


if __name__ == '__main__':
    main()
