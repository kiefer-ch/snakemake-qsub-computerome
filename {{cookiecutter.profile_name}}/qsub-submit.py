#!/usr/bin/env python
"""
qsub-submit.py

Script to wrap qsub command (no sync) for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes.
    - `runtime`: Expecteted time requirements in minutes.

Author: Christoph Engelhard, based on Joseph K Aiche
"""

import sys  # for command-line arguments (get jobscript)
from pathlib import Path  # for path manipulation
from snakemake.utils import read_job_properties  # get info from jobscript
from snakemake.shell import shell  # to run shell command nicely


# get the jobscript (last argument)
jobscript = sys.argv[-1]


# read the jobscript and get job properties
job = read_job_properties(jobscript)


# get resources information
threads = job.get("threads", 1)
resources = job.get("resources", dict())
mem_mb = resources.get("mem_mb", int({{cookiecutter.default_mem_mb}}))
runtime = resources.get("runtime", None)


# set up resources part of command
resources_cmd = " -l nodes=1:ppn={threads}:thinnode"
resources_cmd += ",mem={mem_mb}mb"
# if runtime specified, use it
if runtime:
    # make sure it is integer
    runtime = int(runtime)
    # runtime needs to be specified in HH:MM:SS, but is currently in minutes
    runtime_hr = runtime // 60
    runtime_min = runtime % 60
    # add to resources command
    resources_cmd += ",walltime=%02d:%02d:00" % (runtime_hr, runtime_min)


# get the rule
rule = job.get("rule", "jobname")
# get the wildcards
wildcards = job.get("wildcards", dict())
wildcards_str = ";".join("{}={}".format(k, v) for k, v in wildcards.items())
if not wildcards_str:
    # if there aren't wildcards, this is a unique rule
    wildcards_str = "unique"


# determine names to pass through for job name, logfiles
log_dir = cluster.get("logdir", "{{cookiecutter.default_cluster_logdir}}")
# get the name of the job
jobname = "smk.{0}.{1}".format(rule, wildcards_str)
# get the output file name
out_log = "{}.out".format(jobname)
err_log = "{}.err".format(jobname)
# get logfile paths
out_log_path = str(Path(log_dir).joinpath(out_log))
err_log_path = str(Path(log_dir).joinpath(err_log))


# set up jobinfo part of command
jobinfo_cmd = (" -o {out_log_path:q} -e {err_log_path:q} -N {jobname:q}")


# get command to do cluster command (no sync)
submit_cmd = "qsub -W group_list={{cookiecutter.group_name}} -A {{cookiecutter.group_name}} -m n"


# run commands
shell_stdout = shell(
    # qsub submit command
    submit_cmd
    # specify required threads/resources
    + resources_cmd
    # specify job name, output/error logfiles
    + jobinfo_cmd
    # finally, the jobscript
    + " {jobscript}",
    read=True  # get byte string from stdout
)

# obtain job id from this, and print
print(shell_stdout.strip())
