import pandas as pd
#import numpy as np

#put the colums values in decresing order and find the first 10 highest gene
dok=pd.read_excel (r'C:/Users/Bari/Desktop/python/GB.xlsx', sheet_name = 0, header = 0) 
#print(dok)

#dok2 = dok.sort_values(by=['CE_C1m1','CE_C1m2','CE_C1m3','CE_C6m4sum','CE_C7m1sum','CE_C7m2sum','CE_A7m3','CE_A10m1','CE_A10m3','CE_A10m4','CC_A6m1','CC_A6m2','CC_C1m1','CC_C1m2','CC_C1m3','CC_C6m1','CC_C6m2','CC_C6m3','LG_A7m3','LG_A10m1','LG_A10m3','LG_A10m4','GB_C6m3','GB_C6m4','GB_C7m1','GB_C7m2'], ascending=False)
#print(dok2) 
#select rows
#print(dok.iloc[[2,3,4,5,6,7,8,9,10]])
#writer.save() #How to save?

dic = {}
for i,x in enumerate(dok.columns): #x= head of columns, i= counter
	#print(x)
	#break
	if i >= 3:
		#dok = dok.astype({x: float})
		doksorted=dok.sort_values(by=x,ascending=False)
		#print(list(dok.iloc[range(1,50), 0]))
		#break	
		dic[x] = list(doksorted.iloc[range(0,200), 0]) #key:column head=value:List(50 gene name)	
#print(dic)	
z = []
torlendo=[]
for n,t in enumerate(dic.values()): # n= counter t= dictionary value
	if n == 0: 
		z = t	
	for elem in z:
		if elem in t:
			#print(elem)
			pass
		else:
			torlendo.append(elem)
			#print("barmi")
	for torles in torlendo:
		z.remove(torles)
	torlendo=[]

#print(len(z))
print(z)
out=open("genek.txt", 'w')
for gen in z:
	gen=gen+'\n'
	out.writelines(gen)
out.close()
