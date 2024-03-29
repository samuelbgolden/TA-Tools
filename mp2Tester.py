import argparse
import os
import yaml
import shutil
import subprocess

def main():

    TESTING_ENV = "C:/Users/samgo/src/samuelbgolden/TA-Tools/mp2Tester"

    # add dir arg
    parser = argparse.ArgumentParser(description="grades MP2 of CS340 S22")
    parser.add_argument('dir', help="path to directory with the student code")
    parser.add_argument('-p','--printsrc', help='print students code?', action='store_true')
    args = parser.parse_args()

    # construct paths to needed files
    yaml_file = os.path.join(args.dir, 'package.yaml')
    src_file1 = os.path.join(args.dir, 'src/MP2a.hs')
    src_file2 = os.path.join(args.dir, 'src/MP2b.hs')

    # check that those files exist
    if not os.path.exists(yaml_file):
        print(f"Could not find yaml file at {yaml_file}")
        return

    if not os.path.exists(src_file1):
        print(f"Could not find MP2a.hs at {src_file1}")
        return

    if not os.path.exists(src_file2):
        print(f"Could not find MP2b.hs at {src_file2}")
        return

    # load yaml data to get student info
    yaml_data = yaml.safe_load(open(yaml_file, 'r'))
    print(f"student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")

    # copy file from original location to testing environment
    testing_dest = os.path.join(TESTING_ENV,'src')
    print(testing_dest)
    shutil.copy(src_file1, testing_dest)
    shutil.copy(src_file2, testing_dest)

    if args.printsrc:
        # printing code
        print("******************** FILE SRC MP2a ********************\n")
        code = open(src_file1, 'r')
        for line in code.readlines():
            print('\t' + line, end='')

        print("******************** FILE SRC MP2b ********************\n")
        code = open(src_file2, 'r')
        for line in code.readlines():
            print('\t' + line, end='')

        print("\n****************** END FILE SRC ******************")


    # run tests
    print("\n.....................Running 'stack build'.....................\n")
    p = subprocess.Popen("stack build",cwd=TESTING_ENV)
    p.wait()
    print("\n.....................Running 'stack test'.....................\n")
    p = subprocess.Popen("stack test",cwd=TESTING_ENV)
    p.wait()
    print("\n.....................Running 'stack exec mp2'.....................\n")
    p = subprocess.Popen("stack exec mp2",cwd=TESTING_ENV)
    p.wait()

    # remove copied file from testing environment
    os.remove(os.path.join(testing_dest,'MP2a.hs'))
    os.remove(os.path.join(testing_dest,'MP2b.hs'))

    print(f"\nDone testing student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")


if __name__ == '__main__':
    main()