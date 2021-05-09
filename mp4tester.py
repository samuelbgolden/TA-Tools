import argparse
import os
import yaml
import shutil
import subprocess

def main():

    TESTING_ENV = "C:/Users/samgo/Desktop/Google Drive/School/TACS340/2021/repos/mp4Tester"

    # add dir arg
    parser = argparse.ArgumentParser(description="grades MP4 of CS340 S21")
    parser.add_argument('dir', help="path to directory with the student code")
    parser.add_argument('-p','--printsrc', help='print students code?', action='store_true')
    args = parser.parse_args()

    # construct paths to needed files
    yaml_file = os.path.join(args.dir, 'package.yaml')
    src_file1 = os.path.join(args.dir, 'src/MP4.hs')

    # check that those files exist
    if not os.path.exists(yaml_file):
        print(f"Could not find yaml file at {yaml_file}")
        return

    if not os.path.exists(src_file1):
        print(f"Could not find MP3a.hs at {src_file1}")
        return



    # opening files in sublime
    p = subprocess.Popen(f"subl {src_file1}", shell=True)


    # load yaml data to get student info
    yaml_data = yaml.load(open(yaml_file, 'r'))
    print(f"student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")

    # copy file from original location to testing environment
    testing_dest = os.path.join(TESTING_ENV,'src')
    shutil.copy(src_file1, testing_dest)

    if args.printsrc:
        # printing code
        print("******************** FILE SRC MP4 ********************/n")
        code = open(src_file1, 'r')
        for line in code.readlines():
            print('/t' + line, end='')

        print("/n****************** END FILE SRC ******************")


    # run tests
    print("/nRunning 'stack build'............................../n")
    p1 = subprocess.Popen("stack build",cwd=os.path.abspath(TESTING_ENV), shell=True)
    p1.wait()   

    print("/nRunning tests...................../n")
    print("/n/n========================= TESTER =========================")
    p1 = subprocess.Popen(f"echo {yaml_data['author']} & echo TESTER & stack test", cwd=os.path.abspath(TESTING_ENV), shell=True)
    p1.wait()


    # remove copied file from testing environment
    os.remove(os.path.join(testing_dest,'MP4.hs'))

    print(f"/nDone testing student name: '{yaml_data['author']}', student email: '{yaml_data['maintainer']}'")


if __name__ == '__main__':
    main()