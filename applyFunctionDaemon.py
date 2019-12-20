"""
This daemon will traverse the directory tree which starts from root. While traversing the directory tree, it will look for directories with no sub-directories. Once it finds the right place, it will check that another daemon is not already working or has finished working in that place. If no daemon has, it will apply the function. Once it's done, it will move onto another directory until there are none left or it runs out of time.
"""
import os
import argparse

cwd = os.getcwd()

parse = argparse.ArgumentParser()
parse.add_argument("-f", "--function", dest="function") #This will be what goes in wrap? Whole thing will need to be given in quotes.
parse.add_argument("-p", "--paths", dest="paths")
args = parse.parse_args()

with open(args.paths,"r") as file:
	paths = [path.rstrip("\n") for path in file.readlines()]
os.remove(args.paths)

for path in paths:
    os.chdir(path)
    try:
        os.system(f"{args.function}")
    except:
        print(f"Not running in {path}. Experienced an error.")
    os.chdir(cwd)

os.chdir(cwd)