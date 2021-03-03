import argparse
import subprocess
import yaml

def main():
    parser = argparse.ArgumentParser(description="grade some CODE dude let's GO")
    parser.add_argument('src', help="path to the directory with all students' code")
    parser.add_argument('template', help="path to template text file for reports; each line should follow the format 'key: <potential score>'")
    parser.add_argument('tester', help="path to python file to pass individual repo to")
    parser.add_argument('output', help="path to dir for report outputs and progress record")
    parser.add_argument('studentlist', help="path to list of student information in format: 'username,fname,lname,email'")
    parser.add_argument('-v', '--verbose', help="more print statements")
    args = parser.parse_args()

    print(args)






if __name__ == '__main__':
    main()