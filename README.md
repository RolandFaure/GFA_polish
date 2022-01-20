# GFA_polish
Small repository of command lines to polish a GFA assembly. The idea is just to convert to fasta, polish the fasta and reinject in the GFA.

## Step 1: Convert fasta to GFA

```bash
awk '/^S/{printf ">"$2; for (i=4; i<=NF;i++) printf "\t"$i;  printf "\n"$3"\n"}' old_gfa.gfa > unpolished.fasta
```

## Step 2: Polish the fasta

No special instructions for this one, just choose the polisher.

## Step 3: Inject the polished contigs in the GFA

```bash
awk '{if(FNR==NR){if (substr($1,1,1)==">"){a[0]=NF ; a[1]=substr($1, 2); for (i=2; i<=NF;i++) a[i]="\t"$i}else {printf "S\t"a[1]"\t"$1; for (i=2; i<=a[0];i++) printf a[i]; printf("\n")}}else{if(substr($1,1,1)=="L") {print}}}' polished.fasta old_gfa.gfa > new_gfa.gfa
```
