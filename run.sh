#!/bin/bash

# Run program for all puzzle files in current directory
for puzzle in puzzle*.txt; do
  solution="solution"$(echo $puzzle | tr -dc "0-9")".txt"
  python3 driver.py $puzzle > $solution
done
