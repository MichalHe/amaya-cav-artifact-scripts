# Structure and content of this artifact
The artifact is a Debian 12 VM with a working installation of all tools
necessary to reproduce results presented in the section _8. Experimental
evaluation_.

The implementation of the tool presented in the paper consists of two source
trees:
 - `/home/amaya/amaya` - Python source code of the presented tool. The code
   implements a SMTLIB parser, preprocessing and orchestrates the decision
   procedure.
 - `/home/amaya/amaya-mtbdd` - C++ source code of the backend of the presented
   tool. Implements automata operations and the derivative-based construction
   presented in the paper.

# How to set up this artifact
Login into the account `amaya` using the password `amaya`.

# How to replicate the experiments
The artifact contains a script located at `/home/amaya/run_experiments.sh`
that will execute benchmarks and print two tables --- one for the Frobenius coin
problem benchmark, one for the SMLIB benchmark --- presenting the results. The
structure of these tables matches the tables presented in the section _8.
Experimental evaluation_. Except for the printed tables, the script creates
the following files:
- `/home/amaya/results/smt-frobenius.csv` - results and runtimes of all tools
 that support the SMTLIB input format on the Frobenius coin problem benchmark.
- `/home/amaya/results/lash-frobenius.csv` - results and runtimes of the LASH
 tool on the Frobenius coin problem benchmark.
- `/home/amaya/results/smt-smt_formulae.csv` - results and runtimes of all tools
 that support the SMTLIB input format on the SMTLIB benchmarks.
- `/home/amaya/results/lash-smt_formulae.csv` - results and runtimes of the LASH
 tool on the SMTLIB benchmarks.

Note that depending on the CPU/RAM configuration of the machine, the automata
tools (amaya, LASH) might terminate with an error. We have investigated these
errors and they are caused by the OS forcefully terminating the solver due to
the solver consuming all available memory. Also, the LASH tool might terminate
with a segmentation fault on a very small number (~3) formulae some time  in
the process of solving the input formula. As these formulae are syntactically
correct, there is nothing that can be done from our side to fix these errors.

To perform a smoke test --- run the experiments with only a tiny fraction
of formulae --- please run:
\`\`\`
bash /home/amaya/run_experiments.sh smoke-test
\`\`\`

To run the entire benchmark, run:
\`\`\`
bash /home/amaya/run_experiments.sh
\`\`\`


## System requirements
- 10GB of RAM, 2 core CPU

## Runtime estimates
For a smoke test, the estimated time is <10min.
For the entire benchmark, the upper bound on the overall runtime is 35h, the
expected runtime is <8h.

The experiments were performed on Intel(R) Xeon(R) CPU E5-2620 v3 @ 2.40 GHz
with 32GBs of RAM. The entire job took 5.71h.

# How was the tool tested
The result returned by the tool has been compared to all other tools that finished
in the given time frame.

