#!/bin/python

# 1D-FF-BinPacking
# D C Potts 2023
# MIT license

import argparse
import csv
import pathlib
import sys

# Function to total length remaining in a bin
def getRemainingBinLength(bin, stockLength, bladeWidth):
	totalLength = 0
	for length in bin:
		totalLength += (length[1] + bladeWidth)
	return stockLength - totalLength

# Function to printout bins /w items (lengths) to stdout
def printBins(bins):
	for index, bin in enumerate(bins):
		print(f"Bin {index}:")

		for item in bin:
			print(" "*8 + "{}: {:.2f}".format(item[0].ljust(16), item[1]))

if __name__ == "__main__":
	print("1D-FF-BinPacking")
	print("v1.0")
	print("-"*80)

	parser = argparse.ArgumentParser(
		prog="1D-FF-BinPacking",
		description="1-dimensional first fit bin packing tool for cutting lengths of material from a stock of specific length\nOptionally takes a saw blade width to account for material wasted from the cut\nTakes input from a csv file"
		)

	parser.add_argument(
		'inputFile',
		type=argparse.FileType('r', encoding='utf-8'),
		help="Filename of lengths input (.csv)")

	parser.add_argument(
		'stockLength',
		type=float,
		help="Length of stock to pack into")

	parser.add_argument(
		'-b',
		"--bladeWidth",
		type=float,
		help="Width of saw blade to account for material wastage",
		default="0.0")

	args = parser.parse_args()

	print(f"Stock length: {args.stockLength}")
	print(f"Blade width: {args.bladeWidth}\n")

	lengths = []	# List of tuples for desired lengths (description, length)
	bins = []		# List of lists (bins)

	# Get lengths from .csv file
	inputReader = csv.reader(args.inputFile, delimiter=',', quotechar='|')
	next(inputReader) # First row is headers

	for index, row in enumerate(inputReader):
		# Validate row
		try:
			itemDescription = row[0]
			itemLength = float(row[1])
			itemQuantity = int(row[2])
		except BaseException as e:
			print("Error:", row)
			print(e)
			sys.exit(f"Invalid input in row {index}")

		# Append length to lengths list, for all quantities
		for i in range(0, itemQuantity):
			lengths.append( (itemDescription, itemLength) )

	# Lengths are now collected, sort lengths largest to smallest
	lengths.sort(key=lambda lengthTruple: lengthTruple[1], reverse=True)

	# First empty bin
	bins.append( [] )

	# 1D decreasing first fit bin packing
	# For each length, find the first bin it can fit into, if not, create
	# a new bin
	for item in lengths:
		itemBinned = False
		# Loop through bins to see if item will fit, if it fits, append it
		# if not, create a new bin
		# Account for the blade width, if set (defaults to 0)
		for bin in bins:
			if getRemainingBinLength(bin, args.stockLength, args.bladeWidth) >= (item[1] + args.bladeWidth):
				bin.append(item)
				itemBinned = True
				break
			# Item didn't fit, loop goes to nex bin

		if not itemBinned:
			# Item didn't fit in any bin, create a new one and append item
			bins.append( [item] )

	# Print results
	printBins(bins)