#!/bin/bash

set -e

PLANS_DIR="plans"
RESULTS_DIR="results"
RUNS=1

# Backup dos resultados anteriores, se existirem
if [ -d "$RESULTS_DIR" ]; then
  TS=$(date +%Y%m%d_%H%M%S)
  mv "$RESULTS_DIR" "${RESULTS_DIR}_bkp_$TS"
  echo "[BACKUP] Resultados anteriores movidos para ${RESULTS_DIR}_bkp_$TS"
fi

mkdir -p "$RESULTS_DIR"

for plan in "$PLANS_DIR"/sas_full_flow_*.jmx; do
    plan_name=$(basename "$plan" .jmx)
    plan_result_dir="$RESULTS_DIR/$plan_name"
    mkdir -p "$plan_result_dir"
    for i in $(seq 1 $RUNS); do
        ts=$(date +%Y%m%d_%H%M%S)
        result_file="$plan_result_dir/run_${i}_$ts.jtl"
        echo "[RUN] Executando $plan_name (run $i/$RUNS) -> $result_file"
        jmeter -n -t "$plan" -l "$result_file" -e -o "$plan_result_dir/html_report_${i}_$ts"
    done
    echo "[OK] $plan_name finalizado. Resultados em $plan_result_dir/"
done

echo -e "\n🎉 Todas as execuções dos planos full flow foram concluídas!" 
