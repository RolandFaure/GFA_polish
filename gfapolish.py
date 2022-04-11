#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 08:31:48 2022

@author: rfaure
"""

import os
import sys

def main():
    
    gfaFile = ""
    newargs = []
    for argument in sys.argv[1:]:
        
        if ".gfa" in argument and gfaFile == "" :
            gfaFile = argument.split("=")[-1]
            if len(argument.split("=")) > 1 :
                newargs += ['='.join(argument.split("=")[:-1])+"=unpolished.fasta" ]
            else :
                newargs += ["unpolished.fasta"]
            
        else :
            newargs += [argument]
            
    if gfaFile == "" :
        print("ERROR: did not find the .gfa file of your command line")
        sys.exit()
    
    #first convert the GFA to fasta
    commandGFA2fasta = """ awk '/^S/{printf ">"$2; for (i=4; i<=NF;i++) printf "\t"$i;  print ""; print $3;}' """ + gfaFile +""" > unpolished.fasta """
    os.system(commandGFA2fasta)
    
    #then polish the fasta
    polishLine = " ".join(newargs)
    print("command line : ", polishLine)
    
    #finally, reinject the polished contigs into the GFA
    commandfasta2GFA = """ awk '{if(FNR==NR){if (substr($1,1,1)==">"){a[0]=NF ; a[1]=substr($1, 2); for (i=2; i<=NF;i++) a[i]="\t"$i}else {printf "S\t"a[1]"\t"$1; for (i=2; i<=a[0];i++) printf a[i]; print("");}}else{if(substr($1,1,1)=="L") {print}}}' unpolished.fasta """+ gfaFile +""" > new_gfa.gfa """
    os.system(commandfasta2GFA)
    
    #remove temporary files

if __name__ == '__main__':
    main()