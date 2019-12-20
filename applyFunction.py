"""
This function will submit a specified number of sbatch jobs. Each sbatch job (I call them applyFunctionDaemons) will traverse the directory tree which starts from root. While traversing the directory tree, a daemon will look for a certain condition that indicates it is in the proper place to apply a function. Once it finds the right place, it will check that another daemon is not already working or has finished working in that place. If no daemon has, it will apply the function. Once it's done, it will move onto another directory until there are none left or it runs out of time.

For simplicity, the function will not require any arguments.
"""
import os
import argparse

DaemonPath = "applyFunctionDaemon.py"
cwd = os.getcwd()

def getPaths(root,file):
    paths=[]
    for path,dirs,files in os.walk(root):
        if file not in files and len(dirs)==0: #This is not wild card-able need to give exact filename
            paths.append(path)
    return paths

def partitionList(array, partitions):
    if partitions > len(array):
        length=1
        partitions=len(array)
    else:
        length = len(array)//partitions #Get length of each partition 
    partitionedList = [array[i-length:i] for i in range(length,length*partitions+1,length)] #Partition the array.
    partitionedList[-1].extend(array[length*partitions:]) #Add leftover elements of array to the last partition.
    return partitionedList

def writePathsFile(filename,paths):
    with open(filename,"w") as file:
        for path in paths:
            file.write(path+"\n")

parse=argparse.ArgumentParser()
parse.add_argument("-r", "--root", dest="root", help="Root directory to start searching from.")
parse.add_argument("-f", "--function", dest="function", help="The path to the function to be run. e.g. $PWD/functions/HelloWorld.py") #This will be what goes in wrap? Whole thing will need to be given in quotes.
parse.add_argument("-j", "--jobs", dest="jobs")
parse.add_argument("-t", "--time", dest="time")
parse.add_argument("-o", "--outputFile", dest="outputFile")
args = parse.parse_args()

if not os.path.exists(args.root):
    print("Invalid path.")
else:
    paths = getPaths(args.root,args.outputFile)
    partitionedPaths = partitionList(paths, int(args.jobs))
    for job in range(int(args.jobs)):
        filename = f"applyFunctionDaemonPaths{job}.txt"
        writePathsFile(filename,partitionedPaths[job])
        os.system(f"sbatch -t {args.time} --wrap=\"python3 -u {os.path.join(cwd,DaemonPath)} -f \'{args.function}\' -p {filename}\"")
        #os.system(f"python {os.path.join(cwd,DaemonPath)} --function \"{args.function}\" --paths {filename}")
