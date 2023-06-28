```
sage: a = running(500*10**6)
0.089007
sage: a['path'].execute(405980010) 
etape 0
balance CMST(CRESCENT) ::: 1000000
IBC transfer comdex ===> crescent
gas estimate: 97737
query crescent
query crescent
transfer received
etape 1
balance AXLUSDC(CRESCENT) ::: 2233798
swap CMST for USDC in crescent
gas estimate: 167776
balance AXLUSDC(CRESCENT) ::: 407735036
etape 2
balance IST(CRESCENT) ::: 0
swap USDC for IST in crescent
gas estimate: 167769
balance IST(CRESCENT) ::: 405675178
etape 3
balance GUSDC(CRESCENT) ::: 1560919
swap IST for USDC in crescent
gas estimate: 161130
balance GUSDC(CRESCENT) ::: 407224529
etape 4
balance AXLUSDC(CRESCENT) ::: 2310303
swap USDC for USDC in crescent
gas estimate: 167860
balance AXLUSDC(CRESCENT) ::: 407825317
etape 5
balance CMST(CRESCENT) ::: 1000000
swap USDC for CMST in crescent
gas estimate: 167769
balance CMST(CRESCENT) ::: 406738847
etape 6
balance CMST(COMDEX) ::: 160038072
IBC transfer crescent ===> comdex
gas estimate: 122860
query comdex
transfer received
False```
