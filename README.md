In `runinfo/` there are runs 000 and 001 these runs were called with `python3 dose_to_bbf.py` after `module load gcc/6.2.0; module load python/3.8.1` on CRI.

In 000 I was using the single node launcher and in 001 I was using the aprun launcher (default) and in the respective stderr files I was seeing that process_worker_pool.py and the command aprun were not found.

In config.py I tried different ways to specify the address in the HighThoroughputExecutor but wasn't having any luck connecting the workers (or at least I would always see "0 connected workers" in the logs. In runs 000 and 001 however I only used address_by_route().

