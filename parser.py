#!/usr/bin/env python3

import json
import argparse
import sys 
from kmatch import K

listOfVars=['operator', 'distance']

parser = argparse.ArgumentParser(description='Parse JSON formatted cell_log informations')
parser.add_argument('-f', dest='file',help='The JSON formatted input file ', required=True)
parser.add_argument('-m', '--mode', help="Define the action mode. Sort mode allows to sort results using -s option.", choices=["sort", "print", "filter"], type=str,  dest='mode')
parser.add_argument('-s', '--sortBy', help="In sort mode: define the variable to sort-by.", type=str, choices=listOfVars, dest="sort") 
parser.add_argument('-r','--reverse', help="In sort mode: reverse the output.", default=False, dest="reverse", action='store_true')


parser.add_argument('-l','--limit', help="In sort mode: Limit the size of the output.", default=None, dest="limit", type=int)

parser.add_argument('--no-duplicate', help="In filter mode: remove the duplicated entries.", default=False, dest="no_duplicates", action='store_true')

parser.add_argument('-F','--filter', help="In filter mode: specify the filter to use, in JSON format.", default=None, dest="filter", type=str)


args = parser.parse_args()



if args.file is None:
    sys.exit()
else:
    inFile = open(args.file, "r")
    data = json.load(inFile)

if args.mode == "sort":
    assert(args.sort in listOfVars)
    if args.sort == "operator":
        sortedOutput = sorted(data, key=lambda x: (x['mnc'] == 'n/a', x['mnc']['code']), reverse=args.reverse)[:args.limit]
    elif args.sort == "distance":
        sortedOutput = sorted(data, key=lambda x: (x['ta'] == 'n/a', x['ta']), reverse=args.reverse)[:args.limit]
    
    print(json.dumps(sortedOutput, indent=4, sort_keys=True))

elif args.mode == "filter":
    if args.filter is not None:
        #myfilter = json.loads(args.filter)
        myfilter = args.filter
        
        output=[]
        typeDict = False # flag permettant de dedupliquer les elements etant des listes de listes
        for field in data: # pour chaque element (cellule) trouvé
            if myfilter in field.keys(): # on check si notre filtre correspond à un des elements decrivant la cellule (keys)
                if type(field[myfilter]) is not type(dict()): # si l'entree n'est pas un dictionnaire
                    output.append(field[myfilter])
                else:
                    typeDict = True
                    output.append([j for i,j in field[myfilter].items()]) # on append chaque element du dictionnaire 

        if args.no_duplicates: # si l'option no-duplicate est activee 
             # si l'element voulu n'est pas de type dict/toutpourri on transforme en set pour virer les doublons, et on le repasse en list pour faciliter le traitement futur de la sortie
            if not typeDict:
                print(list(set(output)))
            else: # si c'est un type toutpourri/dict on transforme ca en sous liste, et même manip qu'au dessus avec list(set(...))
                print(list(set(tuple(i) for i in output))) # 
        else: # sinon on affiche juste la sortie
            print(output)

    

elif args.mode == "print":
    print(json.dumps(data, indent=4, sort_keys=True))

