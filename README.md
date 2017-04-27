# First of all 

Made for and using [osmocom-bb](https://github.com/osmocom/osmocom-bb.git) repository, and [francoip/thesis](https://gitlab.com/francoip/thesis.git) patchs.

Set-up process:

	git clone https://github.com/osmocom/osmocom-bb.git
	git clone https://gitlab.com/francoip/thesis.git
	cd ./osmocom-bb/
	git pull --rebase
	patch -p1 < ../thesis/patch/thesis.patch
	patch -p1 < ../thesis/patch/aftenposten.patch
 	cd ./src/
	make -e CROSS_TOOL_PREFIX=arm-none-eabi-

# Apply the patch

Just replace the *osmocom-bb/src/host/layer23/src/misc/cell_log.c* file with the one provided here (can also be done using the patch, frome the osmocom-bb root directory:
	
	git clone https://github.com/razaborg/osmocom_cell-log_parser.git
	cd osmocom-bb/cd src/host/layer23/src/misc/
	patch -p0 --dry-run < ../../../../../../cell_log-parser/cell_log.json.patch
	make
	./cell_log -l ...

# Use the parser

1. Edit the logfile from teh new cell_log binary :

	sed -i '1s/^/[/' logfile.txt && head -c -2 logfile.txt && echo ']' >> logfile.txt

2. And RTFM:

	./parser.py -h 


# How the does the parser works ? 

## Intro

The ''''parser.py'''' works with modes :

Mode **sort** :

	parser.py -m sort -s <sortBy>

Mode **filter** : 

	parser.py -m filter - F <filterBy>

Mode **print** : 

	parser.py -m print

## Examples

### To sort per operator with max 2 entries:

	./parser.py -f logfile.txt -m sort -s operator -l 2

### To get the 10 nearer cells:

	./parser.py -f logfile.txt -m sort -s distance -l 10

### To get only the mnc scanned, without duplicates :

	./parser.py -f logfile.txt -m filter -F mnc --no-duplicate

### To get only the ARFCN of all the scanned cells, without duplicates:

	./parser.py -f logfile.txt -m filter -F arfcn --no-duplicate


