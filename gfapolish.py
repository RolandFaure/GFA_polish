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
    args = sys.argv[1].split()
    #print("argument : " , args)
    for argument in args:
        if ".gfa" in argument and gfaFile == "" :
            gfaFile = argument.split("=")[-1]
            if len(argument.split("=")) > 1 :
                newargs += ['='.join(argument.split("=")[:-1])+"=unpolished.fasta" ]
            else :
                newargs += ["unpolished.fasta"]
            
        else :
            newargs += [argument]
            
    polishedFile = ""
    for arg in range(len(args)-1, -1, -1):
        if ".gfa" in args[arg] and polishedFile == "" :
            polishedFile = args[arg].split("=")[-1]
            if len(args[arg].split("=")) > 1 :
                newargs[arg] = '='.join(args[arg].split("=")[:-1])+"=polished.fasta"
            else :
                newargs[arg] = "polished.fasta"
            
    if gfaFile == "" :
        print("ERROR: did not find the input .gfa file in your command line")
        sys.exit()
        
    if polishedFile == "" or polishedFile == gfaFile :
        print("ERROR: did not find the output .gfa file in your command line")
        sys.exit()
    
    #first convert the GFA to fasta
    commandGFA2fasta = """ awk '/^S/{printf ">"$2; for (i=4; i<=NF;i++) printf "\t"$i;  print ""; print $3;}' """ + gfaFile +""" > unpolished.fasta """
    e = os.system(commandGFA2fasta)
    
    #then polish the fasta
    polishLine = " ".join(newargs)
    # print("command line : ", polishLine)
    f = os.system(polishLine)
    
    if f != 0 :
        print("Polishing crashed, here is the command line I used: ", polishLine)
        sys.exit()
        
    out = "polished.fasta"
    if not os.path.exists("polished.fasta") :
        if os.path.exists("polished.fasta.fasta") :
            out = "polished.fasta.fasta"
        elif os.path.exists("polished.fasta.fa"):
            out = "polished.fasta.fa"
        else :
            print("ERROR: This polisher has an interface too complicated for me. The polished contigs exist somewhere in this directory with a name like 'polished.fasta'. Please switch to manual mode step 3 to finish polishing (see the REAMDE)")
            sys.exit()
    
    #finally, reinject the polished contigs into the GFA
    commandfasta2GFA = """ awk '{if(FNR==NR){if (substr($1,1,1)==">"){a[0]=NF ; a[1]=substr($1, 2); for (i=2; i<=NF;i++) a[i]="\t"$i}else {printf "S\t"a[1]"\t"$1; for (i=2; i<=a[0];i++) printf a[i]; print("");}}else{if(substr($1,1,1)=="L") {print}}}' polished.fasta """+ gfaFile +""" > new_gfa.gfa """
    os.system(commandfasta2GFA)
    
    #remove temporary files
    os.system("rm unpolished.fasta")
    os.system("rm polished.fasta")

if __name__ == '__main__':
    main()