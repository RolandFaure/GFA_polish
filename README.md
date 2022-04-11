# GFA_polish
Very rudimentary script to polish an assembly graph in GFA format. This script does NOT exploit the extra information contained in the GFA relative to the fasta. The idea is just to convert to fasta, polish the fasta and reinject in the GFA.

## All-in-one script

### Dependancies and installation
You'll need a working python 3 installation. The script runs "awk", which you'll also need in the path (default on Linux distributions). 
The script also runs a 'rm' at the end: if you do not have the permissions, you can comment out this line or just let it crash, the result won't be affected
It is a python script thus needs no installation

### Usage
Give to the script the command you would have used to polish a fasta, replacing the '.fasta' files by '.gfa'. For example, instead of running
```
racon reads.fasta alignments.paf assembly.fasta > polished.fasta
```
run :
```
python gfapolish.py "racon reads.fasta alignments.paf assembly.gfa > polished.gfa "

```
The script identifies the first GFA of the line as the input file and the last GFA of the line as the output file. 
If the interface of the polisher is a little complicated (e.g. you do not explicitely give the output file but an output prefix), you'll probably be better off using the manual override below.

## Manual override
If the above script does not work for one reason or another, here are the two important command lines encapsulated in the script:
### Step 1: Convert GFA to fasta

```bash
awk '/^S/{printf ">"$2; for (i=4; i<=NF;i++) printf "\t"$i;  printf "\n"$3"\n"}' old_gfa.gfa > unpolished.fasta
```

### Step 2: Polish the fasta

No special instructions for this one, just choose the polisher.

### Step 3: Inject the polished contigs in the GFA

```bash
awk '{if(FNR==NR){if (substr($1,1,1)==">"){a[0]=NF ; a[1]=substr($1, 2); for (i=2; i<=NF;i++) a[i]="\t"$i}else {printf "S\t"a[1]"\t"$1; for (i=2; i<=a[0];i++) printf a[i]; printf("\n")}}else{if(substr($1,1,1)=="L") {print}}}' polished.fasta old_gfa.gfa > new_gfa.gfa
```
