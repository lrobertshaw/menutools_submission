###!/usr/bin/python

import optparse
import ConfigParser
import os
import sys
import shutil
import subprocess


class TaskConfig:
    def __init__(self, taskName, cfgfile):
        print 'TN: {}'+taskName
        self.task_name = taskName
        self.version = cfgfile.get('Common', 'version')
        self.cmssw_config = cfgfile.get('Common', 'cmssw_config')
        self.input_directory = cfgfile.get(taskName, 'input_directory')
        self.splitting_mode = cfgfile.get(taskName, 'splitting_mode')
        self.splitting_granularity = cfgfile.get(taskName, 'splitting_granularity')
        self.task_dir = '{}/{}/{}'.format(cfgfile.get('Common', 'name'),
                                          cfgfile.get('Common', 'version'),
                                          taskName)
        self.output_dir = '{}/{}/{}/{}'.format(cfgfile.get('Common', 'output_dir_base'),
                                               self.task_name,
                                               cfgfile.get('Common', 'mode'),
                                               self.version)
        self.job_flavor = cfgfile.get(taskName, 'job_flavor')

    def __str__(self):
        return 'task-name {}: version {}'.format(self.task_name, self.version)


def splitFiles(files, splitting_mode, splitting_granularity):
    split_files = []
    if splitting_mode == 'file_based':
        size = int(splitting_granularity)
        split_files = [files[i:i+size] for i in range(0, len(files), size)]
    else:
        print 'Splitting-Mode: {} is not implemented! Exiting...'.format(splitting_mode)
        sys.exit(6)
    return split_files


def getJobParams(mode, task_conf):
    params = {}
    if mode == 'NTP':
        input_files = ['root://eoscms.cern.ch/'+os.path.join(task_conf.input_directory, file_name) for file_name in os.listdir(task_conf.input_directory) if file_name.endswith('.root')]
        # print input_files
        print '# of files: {}'.format(len(input_files))
        split_files = splitFiles(input_files, task_conf.splitting_mode, task_conf.splitting_granularity)
        n_jobs = len(split_files)
        # the first 2 are compulsory for all modes
        params['NJOBS'] = n_jobs
        params['INFILES'] = split_files
        params['TEMPL_NEVENTS'] = -1
        params['TEMPL_TASKDIR'] = task_conf.task_dir
        params['TEMPL_TASKCONFDIR'] = '{}/conf'.format(task_conf.task_dir)
        params['TEMPL_ABSTASKCONFDIR'] = os.path.join(os.environ["PWD"], params['TEMPL_TASKCONFDIR'])
        params['TEMPL_OUTFILE'] = 'ntuple.root'
        params['TEMPL_OUTDIR'] = task_conf.output_dir
        params['TEMPL_JOBFLAVOR'] = task_conf.job_flavor
    else:
        print 'Mode: {} is not implemented! Exiting...'.format(mode)
        sys.exit(4)
    return params


def createJobConfig(mode, params):
    custom_template_filename = 'templates/jobCustomization_{}_cfg.py'.format(mode)
    for job_idx in range(0, params['NJOBS']):
        input_files = params['INFILES'][job_idx]
        input_file_names = ['\'{}\''.format(file_name) for file_name in input_files]
        file_list = ',\n'.join(input_file_names)
        custom_template_file = open(custom_template_filename)
        custom_template = custom_template_file.read()
        custom_template_file.close()
        custom_template = custom_template.replace('TEMPL_INFILES', file_list)
        templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
        for key in templs_keys:
            custom_template = custom_template.replace(key, str(params[key]))

        job_config_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'job_config_{}.py'.format(job_idx)), 'w')
        job_config_file.write(custom_template)
        job_config_file.close()


def createCondorConfig(mode, params):
    condor_template_name = 'templates/condorSubmit_{}.sub'.format(mode)
    condor_template_file = open(condor_template_name)
    condor_template = condor_template_file.read()
    condor_template_file.close()
    condor_template = condor_template.replace('TEMPL_NJOBS', str(params['NJOBS']))
    templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
    for key in templs_keys:
        condor_template = condor_template.replace(key, str(params[key]))

    condor_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'condorSubmit.sub'), 'w')
    condor_file.write(condor_template)
    condor_file.close()


def createJobExecutable(mode, params):
    shutil.copy('templates/run_{}.sh'.format(mode), '{}/run.sh'.format(params['TEMPL_TASKCONFDIR']))
    params_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'params.sh'), 'w')
    templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
    for key in templs_keys:
        params_file.write('{}={}\n'.format(key.split('_')[1], str(params[key])))
    params_file.close()


def createTaskSetup(task_config, config_file):
    mode = config_file.get('Common', 'mode')
    pwd = os.environ["PWD"]
    if not os.path.exists(task_config.task_dir):
        print "   creating task directory {}".format(task_config.task_dir)
        os.makedirs(task_config.task_dir)
        os.mkdir(task_config.task_dir+'/conf/')
        os.mkdir(task_config.task_dir+'/logs/')

    if not os.path.exists(task_config.output_dir):
        print '   ERROR: output dir {} doesn\'t exist: please create it first!'.format(task_config.output_dir)
        print sys.exit(2)

    shutil.copy(task_config.cmssw_config, '{}/conf/input_cfg.py'.format(task_config.task_dir))

    params = getJobParams(mode, task_config)
    createJobConfig(mode, params)
    createCondorConfig(mode, params)
    createJobExecutable(mode, params)
    return


def submitTask(task_config):
    condor_cmd = 'condor_submit {}/conf/condorSubmit.sub'.format(task_config.task_dir)
    try:
        print subprocess.check_output(condor_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(condor_cmd)
        print e.output


def getCondorCluster(task_config):
    # clusterId = 529700
    condorLogs = [x for x in os.listdir(os.path.join(task_config.task_dir, 'logs')) if x.endswith('.log')]
    condorLogs.sort()
    clusterId = condorLogs[-1].split('.')[1]
    # print condorLogs
    return clusterId


def printStatus(clusterId):
    condor_cmd = 'condor_q {}'.format(clusterId)
    try:
        print subprocess.check_output(condor_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(condor_cmd)
        print e.output

def printWait(task_conf, clusterId):
    condor_cmd = 'condor_wait -wait 1 -status {}/logs/condor.{}.log'.format(task_conf.task_dir, clusterId)
    try:
        print subprocess.check_output(condor_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(condor_cmd)
        print e.output


def main():
    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('-f', '--file', dest='CONFIGFILE', help='specify the ini configuration file')
    parser.add_option("--create", action="store_true", dest="CREATE", default=False, help="create the job configuration")
    parser.add_option("--submit", action="store_true", dest="SUBMIT", default=False, help="submit the jobs to condor")
    parser.add_option("--status", action="store_true", dest="STATUS", default=False, help="check the status of the condor tasks")

    global opt, args
    (opt, args) = parser.parse_args()

    cfgfile = ConfigParser.ConfigParser()
    cfgfile.optionxform = str

    cfgfile.read(opt.CONFIGFILE)

    tasks = cfgfile.get('Common', 'tasks').split(',')
    task_configs = []
    for task in tasks:
        task_configs.append(TaskConfig(task, cfgfile))

    for task_conf in task_configs:
        print task_conf

    if opt.CREATE:
        for task_conf in task_configs:
            print '-- Creating task {}'.format(task_conf.task_name)
            # 1 create local dir
            createTaskSetup(task_conf, cfgfile)
    elif opt.SUBMIT:
        for task_conf in task_configs:
            print '-- Submitting task {}'.format(task_conf.task_name)
            # 1 create local dir
            submitTask(task_conf)
    elif opt.STATUS:
        for task_conf in task_configs:
            print '-- Status of task {}'.format(task_conf.task_name)
            clusterId = getCondorCluster(task_conf)
            printStatus(clusterId)
            printWait(task_conf, clusterId)
            print '   out dir: {}'.format(task_conf.output_dir)


if __name__ == "__main__":
    main()
