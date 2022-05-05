# Snakemake qsub profile

Snakemake cookiecutter profile for running jobs on computerome, using thin nodes.
Derived from [jaicher/snakemake-qsub][cluster-sync]. Status script is from
[Snakemake-Profiles/pbs-torque][pbs-torque].
Deploy using [cookiecutter][cookiecutter-repo] (easily installed using conda or
pip) by running:

   [cluster-sync]: https://github.com/jaicher/snakemake-qsub
   [pbs-torque]: https://github.com/Snakemake-Profiles/pbs-torque
   [cookiecutter-repo]: https://github.com/audreyr/cookiecutter
   
Does not support snakemake grouping.
   
```
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake gh:kiefer-ch/snakemake-qsub-computerome 
```

## Configuration

This command will prompt for parameters to set. 

Once complete, it will allow you to run Snakemake with the cluster
configuration using the `--profile` flag. For example, if the profile name
was `thinnode`, then you can run:

```
snakemake --profile thinnode {...}
```

## Specification of resources/cluster settings

Individual snakemake rules can have the following parameters specified in the
Snakemake file:
+ `threads`: the number of threads needed for the job. If not specified,
  assumed to be 1.
+ `resources`
    - `mem_mb`: the memory required for the rule in megabytes. If not present,
        falls back to the default value entered when configuring the profile.
    - `runtime`: the walltime required for the rule in minutes. If not present,
        falls back to the cluster setting of 1 h.
