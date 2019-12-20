# applyFunction
Slurm compatible script to run generic functions in parallel throughout a specified directory tree.

Welcome to applyFunction.py! This program is a total hack that probably isn't necessary if you now how to use slurm properly!

This program will run an arbitrary command in every leaf directory of a root directory. It will do this using a specified number of sbatch jobs. The leaf directories will be equal distributed amongst the different sbatch jobs.

The reason you'd want to do this is to run a program WAY more times than your allotted 410 jobs will allow at one time.

The basic command is python3 applyFunction.py -r "path/to/a/directory/tree" -f "function $PWD/path/to/function" -j someInteger -t hh:mm:ss -o "n/a"

The -r flag is the path to the directory you want to run a function in. -f is the function command. "function" is something like python/python3 or "math -script" for mathematica. After the function flag is the path to the actual function. The $PWD is required. The -j flag is the number of sbatch jobs to use. The max number of jobs is 410. the -t flag i the amount of time for each sbatch job. The hh:mm:ss format is hours:seconds:seconds. the maximum amount of time is 72 hours. I don't think -o does anything.

When you enter this command two things will happen. First, a bunch of sbatch jobs will be submitted. Second, and you may not actually see them because they get deleted as soon as the sbatch job starts, a bunch of files called "applyFunctionDaemonPaths.txt" files will be created. These pass the paths asscoaited with each job on to the sub program which actually runs the program in the different directories.

Here's an example:
python3 applyFunction.py -r "../output/v4/combinedSweep0_T5.0" -f "math -script $PPWD/functions/GetLastFrame.wl" -j 5 -t 02:00:00 -o "n/a"

This will run GetLastFrame.wl in every directory in combinedSweep0_T5.0. It will split all the paths into five sbatch jobs that will each run for two hours.

A couple notes, you have to load the module for whatever program you want to use. Second the program assumes you are in the directory of the whatever leaf you're at.
