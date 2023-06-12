#!/bin/sh

python create_db_susceptibility.py
python create_db_microorganism.py
python create_db_antimicrobial.py

$SHELL