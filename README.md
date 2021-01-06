All runs are called by running `python3 run.py` on a Gardener login node.

In `runinfo.1_at_a_time_cached_.2_at_once_finds_cache` there are 3 runs.
 * 000
   * This filters* a single file (file part 1), works well, caches the result.
   * 07ad077935bab8ede17ab280b1ebb596
   * Completes ~ 5 minutes.
   * Corresponds to line 29 in `run.py`
 * 001
   * This filters a single file (file part 2), works well, caches the result.
   * 47a423c6e71c58eef057a2d95cb7522a
   * Completes ~ 8 minutes.
   * Corresponds to line 30 in `run.py`
 * 002
   * This attempts to filter both of the files from runs 000 and 001 at once.
   * Since the results from 000 and 001 are cached, this completes successfully.  
     

In `runinfo.2_at_once_without_cache_does_not_work` there is a single run
 * 000
   * This attempts to filter both of the files as in run 002 above, but this
     time without any cached results to fall back on.
   * Corresponds to line  36 in `run.py`
   * Tasks are submitted succesfully and looking at `parsl.log`, workers appear
     to be connected.
   * Memoization hashes are exactly the same as well, but even after ~ 30
     minutes after task submission, neither task completes.


Basically, the above error I'm having is making it difficult for me to scale up
the initial step in my parsl script to work on the ~600 file parts I want to
filter. I can work on 1 file part and have it go through the steps I've created
so far, but anytime I try 2 or more file parts, all tasks for the intial step
hang as described above.

*The "filtering" happening is a call to a python3 command line application that
I've turned into a parsl `bash_app`.
