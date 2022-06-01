# Submission tools for batch job management (CERN HT-Condor & CMS CRAB)

## How-to submit jobs

Inline help:

`python3 submit.py --help`

Create the Job configuration using the command:

`python3 submit.py -f submit.yaml --create`

Submit the jobs to the queues via the command:

`python submit.py -f submit.yaml --submit`

## Configuration file



The conf file uses the `YAML` format. You can find several examples in this directory. Most of the parameters should be self explenatory. 
Each task corresponds to a sample.

The tool supports:
* **HT-Condor local submission**: each task will be mapped to a dedicated condor cluster.
Input files can be specified via the dataset name using `input_dataset` or via the directory where the files sit using `input_directory`. The implemented input splitting modes are: `file_based` and `lumi_based` (in the sense of LS).
For the `job_flavor` and other condor parameters please refer to the [CERN Condor documentation](http://batchdocs.web.cern.ch/batchdocs/local/index.html)

* **CRAB remote submission**: this is controlled setting the `crab: True` parameter. In this case the input needs to be specified using `input_dataset` and for the configuration of `splitting_mode` and `splitting_granularity` you need to refer to the [CMS CRAB Sw Guide](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab). The rest of the parameters can be customized via the template file `crab_MODE.py` (see the documentation about the template structure in the following).


## How to modify the template structure

If you want to add a new set of templates you need to define a new mode (`MODE`) in:

https://github.com/cerminar/submission/blob/master/submit.py#L101

Note the code assumes that all keys starting with `TEMPL_` are variables in the templated files that need to be replaced.

And create the corresponding template files in the directory
`templates/`

You need 1 or 2 templated files:
1. `condorSubmit_MODE.sub`: this defines the structure of the Condor submission file. If you don't need to modify it you can use the `condorSubmit_DEFAULT.sub` one (see [CERN Condor documentation](http://batchdocs.web.cern.ch/batchdocs/local/index.html));
2. `jobCustomization_MODE_cfg.py.` which defines what needs to be changed for each job of the cluster.
3. `run_MODE.sh`: this is the script which actually gets executed on the node, setups the config and calls cmsRun. Again a `run_DEFAULT.sh` exists and should work for most cases.
