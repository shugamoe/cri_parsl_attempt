#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from parsl.config import Config
from parsl.data_provider.files import File
from parsl.channels import LocalChannel
from parsl.executors import HighThroughputExecutor
from parsl.providers import TorqueProvider
from parsl.addresses import address_by_route, address_by_query, address_by_hostname
from parsl.launchers import SingleNodeLauncher
from parsl.utils import get_all_checkpoints
from parsl.dataflow.memoization import id_for_memo


sbayesr_config = Config(
    checkpoint_mode = "task_exit",
    checkpoint_files = get_all_checkpoints(),
    executors=[
        HighThroughputExecutor(
            label="standard_16gb_1core",
            cores_per_worker=1,
            address=address_by_hostname(), # Gets cri16in001 as address
            worker_debug = False,
            provider=TorqueProvider(
                channel=LocalChannel(), # Default if not given
                launcher=SingleNodeLauncher(),
                worker_init=("module load gcc/6.2.0; module load plink/2.0; "
                            "cd {0}; pwd; "
                            "module load python/3.8.1; "
                            "python3 -c 'import parsl; print(parsl.__version__)'; "
                            "export PATH=~/.local/bin:$PATH; "
                            "export PYTHONPATH='{0}:{{PYTHONPATH}}'").format(os.getcwd()),
                walltime="6:00:00",
                scheduler_options="#PBS -l mem=16gb",
                init_blocks=1,
                min_blocks=0,
                max_blocks=30,
                nodes_per_block=1,
                parallelism=1
            ),
        ),
	HighThroughputExecutor(
            label="plink2_express_2gb_1core",
            cores_per_worker=1,
            address=address_by_hostname(), # Gets cri16in001 as address
            #  address=address_by_query(), # Gets 128.135.245.36 as address
            # address=address_by_route(), # Gets 10.50.178.250 as address
            # address="128.135.245.36",
            worker_debug = True,
            provider=TorqueProvider(
                channel=LocalChannel(), # Default if not given
                launcher=SingleNodeLauncher(),
                worker_init=("module load gcc/6.2.0; module load plink/2.0; "
                            "cd {0}; pwd; "
                            "module load python/3.8.1; "
                            "python3 -c 'import parsl; print(parsl.__version__)'; "
                            "export PATH=~/.local/bin:$PATH; "
                            "export PYTHONPATH='{0}:{{PYTHONPATH}}'").format(os.getcwd()),
                walltime="01:00:00",
                scheduler_options="#PBS -l mem=2gb",
                init_blocks=0,
                min_blocks=0,
                max_blocks=45,
                nodes_per_block=1,
                parallelism=1
            ),
        ),
	HighThroughputExecutor(
            label="plink1_express_2gb_1core",
            cores_per_worker=1,
            address=address_by_hostname(), # Gets cri16in001 as address
            #  address=address_by_query(), # Gets 128.135.245.36 as address
            # address=address_by_route(), # Gets 10.50.178.250 as address
            # address="128.135.245.36",
            worker_debug = True,
            provider=TorqueProvider(
                channel=LocalChannel(), # Default if not given
                launcher=SingleNodeLauncher(),
                worker_init=("module load gcc/6.2.0; module load plink/1.90; "
                            "cd {0}; pwd; "
                            "module load python/3.8.1; "
                            "python3 -c 'import parsl; print(parsl.__version__)'; "
                            "export PATH=~/.local/bin:$PATH; "
                            "export PYTHONPATH='{0}:{{PYTHONPATH}}'").format(os.getcwd()),
                walltime="01:00:00",
                scheduler_options="#PBS -l mem=2gb",
                init_blocks=0,
                min_blocks=0,
                max_blocks=45,
                nodes_per_block=1,
                parallelism=1
            ),
        ),
    ],
)


@id_for_memo.register(File)
def id_for_memo_File(f, output_ref=False):
    import os
    if output_ref:
        # logger.debug("hashing File as output ref without content: {}".format(f))
        print("hashing File as output ref without content: {}".format(f))
        return f.url
    else:
        # logger.debug("hashing File as input with content: {}".format(f))
        print("hashing File as input with content: {}".format(f))
        assert f.scheme == "file"
        filename = f.filepath
        stat_result = os.stat(filename)

