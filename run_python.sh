#!/bin/bash

for i in {15..19}; do
  python main.py -t -cn -l  > logs/ausgabe_cn_$i.txt
  python main.py -r "Q_table${i}_Z10L1G0.npy" -m1 > logs/ausgabe_cn_m1_$i.txt
  python main.py -r "Q_table${i}_Z10L1G0.npy" -m2 > logs/ausgabe_cn_m2_$i.txt
  python main.py -r "Q_table${i}_Z10L1G0.npy" -m3 > logs/ausgabe_cn_m3_$i.txt

  python main.py -t -cc -l > logs/ausgabe_cc_$i.txt
  python main.py -r "Q_table${i}_Z01L1G0.npy" -m1 > logs/ausgabe_cc_m1_$i.txt
  python main.py -r "Q_table${i}_Z01L1G0.npy" -m2 > logs/ausgabe_cc_m2_$i.txt
  python main.py -r "Q_table${i}_Z01L1G0.npy" -m3 > logs/ausgabe_cc_m3_$i.txt

  python main.py -t -l  > logs/ausgabe_l_$i.txt
  python main.py -r "Q_table${i}_Z00L1G0.npy" -m1 > logs/ausgabe_l_m1_$i.txt
  python main.py -r "Q_table${i}_Z00L1G0.npy" -m2 > logs/ausgabe_l_m2_$i.txt
  python main.py -r "Q_table${i}_Z00L1G0.npy" -m3 > logs/ausgabe_l_m3_$i.txt

  python main.py -t -g  > logs/ausgabe_g_$i.txt
  python main.py -r "Q_table${i}_Z00L0G1.npy" -m1 > logs/ausgabe_g_m1_$i.txt
  python main.py -r "Q_table${i}_Z00L0G1.npy" -m2 > logs/ausgabe_g_m2_$i.txt
  python main.py -r "Q_table${i}_Z00L0G1.npy" -m3 > logs/ausgabe_g_m3_$i.txt

  python main.py -t -g -cc > logs/ausgabe_gcc_$i.txt
  python main.py -r "Q_table${i}_Z01L0G1.npy" -m1 > logs/ausgabe_gcc_m1_$i.txt
  python main.py -r "Q_table${i}_Z01L0G1.npy" -m2 > logs/ausgabe_gcc_m2_$i.txt
  python main.py -r "Q_table${i}_Z01L0G1.npy" -m3 > logs/ausgabe_gcc_m3_$i.txt

  python main.py -t -g -cn > logs/ausgabe_gcn_$i.txt
  python main.py -r "Q_table${i}_Z10L0G1.npy" -m1 > logs/ausgabe_gcn_m1_$i.txt
  python main.py -r "Q_table${i}_Z10L0G1.npy" -m2 > logs/ausgabe_gcn_m2_$i.txt
  python main.py -r "Q_table${i}_Z10L0G1.npy" -m3 > logs/ausgabe_gcn_m3_$i.txt
done

