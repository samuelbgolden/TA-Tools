import argparse
import os
import yaml
import shutil
import subprocess

def main():

    TESTING_ENV = "C:/Users/samgo/Desktop/Google Drive/School/TACS340/2021/repos/mp1Tester"

    # add dir arg
    parser = argparse.ArgumentParser(description="grades MP1 of CS340 S21")
    parser.add_argument('dir', help="path to   directory with the student code")
    args = parser.parse_args()

    # construct paths to needed files
    yaml_file = os.path.join(args.dir, 'package.yaml')
    src_file = os.path.join(args.dir, 'src/MP1.hs')

    # check that those files exist
    if not os.path.exists(yaml_file):
        print(f"Could not find yaml file at {yaml_file}")
        return

    if not os.path.exists(src_file):
        print(f"Could not find MP1.hs at {src_file}")
        return

    # load yaml data to get student info
    yaml_data = yaml.load(open(yaml_file, 'r'))
    print(f"student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")

    # copy file from original location to testing environment
    testing_dest = os.path.join(TESTING_ENV,'src')
    print(testing_dest)
    shutil.copy(src_file, testing_dest)

    # printing code
    print("******************** FILE SRC ********************\n")
    code = open(src_file, 'r')
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
    print("\n.....................Running 'stack exec mp1'.....................\n")
    p = subprocess.Popen("stack exec mp1",cwd=TESTING_ENV)
    p.wait()

    # remove copied file from testing environment
    os.remove(os.path.join(testing_dest,'MP1.hs'))

    print(f"\nDone testing student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")


if __name__ == '__main__':
    main()