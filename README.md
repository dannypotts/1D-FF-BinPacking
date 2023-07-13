# 1D-FF-BinPacking
1-dimensional first fit bin packing tool for cutting lengths of material from a stock of specific length

## Usage
<b>python src/main.py</b> inputFile stockLength [options]
### Options
<b>-b, --bladeWidth</b>, Width of buffer/saw blade to take into account

## Input File
- Comma seperated variable (.csv) format:
description, length, quantity
- First row is a header and is ignored
- Example input file given in "lengths.csv.example"
- The script will ignore lines that start with a #