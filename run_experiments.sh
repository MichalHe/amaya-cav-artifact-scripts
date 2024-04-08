#!/usr/bin/bash

PYTHON=/home/amaya/amaya/venv/bin/python3

TIMEOUT=60  # seconds
JOBS=1
RESULTS_DIR=/home/amaya/results
BENCH_DIR=/home/amaya/amaya/benchmarks/bench
TINY_MODE_FORMULAE_AMOUNT=3

SMT_TOOLS_CONFIG=$BENCH_DIR/smt.yaml
LASH_TOOLS_CONFIG=$BENCH_DIR/lash.yaml

function run_benchmark {
    input_list_file="$1";
    config="$2";
    dest_csv_file="$3";
    run_mode="$4";
    dest_raw_file="$dest_csv_file".raw;
    
    pushd /home/amaya/amaya/benchmarks/bench; 
    if [[ "$run_mode" == "smoke-test" ]]; then
        cat $input_list_file | head -$TINY_MODE_FORMULAE_AMOUNT | $PYTHON ./pycobench -c "$config" -t $TIMEOUT -j $JOBS -o "$dest_raw_file" 
    else
        cat $input_list_file | $PYTHON ./pycobench -c "$config" -t $TIMEOUT -j $JOBS -o "$dest_raw_file" 
    fi
    cat $dest_raw_file | $PYTHON ./pyco_proc --csv > $dest_csv_file 
    popd
}

function run_frobenius {
    mode="$1"
    echo "Benchmarking on frobenius formulae."
    echo "Executing tools that support SMTLIB format."
    run_benchmark "${BENCH_DIR}/inputs/cav/frobenius.inputs"      "$SMT_TOOLS_CONFIG" $RESULTS_DIR/smt-frobenius.csv   "$mode"
    echo "Executing LASH."
    run_benchmark "${BENCH_DIR}/inputs/cav/lash-frobenius.inputs" "$LASH_TOOLS_CONFIG" $RESULTS_DIR/lash-frobenius.csv "$mode" 
}

function run_smt_formulae {
    mode="$1"
    echo "Benchmarking on SMTLIB formulae."
    echo "Executing tools that support SMTLIB format."
    run_benchmark "${BENCH_DIR}/inputs/cav/smt_formulae.inputs"      "$SMT_TOOLS_CONFIG"  $RESULTS_DIR/smt-smt_formulae.csv  "$mode" 
    echo "Executing LASH."
    run_benchmark "${BENCH_DIR}/inputs/cav/lash-smt_formulae.inputs" "$LASH_TOOLS_CONFIG" $RESULTS_DIR/lash-smt_formulae.csv "$mode" 
}

run_mode="$1"
run_frobenius    $run_mode
run_smt_formulae $run_mode

echo ""
echo ""
echo "########## FROBENIUS RESULTS ##########"
$PYTHON /home/amaya/merge_csvs.py $RESULTS_DIR/smt-frobenius.csv $RESULTS_DIR/lash-frobenius.csv
echo ""
echo "########## SMTLIB RESULTS ##########"
$PYTHON /home/amaya/merge_csvs.py $RESULTS_DIR/smt-smt_formulae.csv $RESULTS_DIR/lash-smt_formulae.csv

