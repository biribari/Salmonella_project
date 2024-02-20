doksi=open("genek_test.txt", "r",)
output=open("operon.txt", "w")
#print(genek.read())

#1.remove the text from the gene names
genek=doksi.readlines() #this makes it a list
#print(type(genek))
genek_cut=[""]*len(genek)
#print(genek_cut)
for szamlalo, lista in enumerate(genek):
	#print(szamlalo)
	genek_cut[szamlalo]=genek[szamlalo].replace("SL1344_RS", "").replace("\n", "")
#print(genek_cut)
# this workes with strings: cut_genek_name=genek.replace("SL1344_RS", "")
#print(cut_genek_name)
#2.put into order the gene names
sorted_genek=sorted(genek_cut)
#print(sorted_genek)
#3.find the genes where the difference is only 1
gen_lista=[]
for i in range(len(sorted_genek)-1): #i= szamlalo here also
	if int(sorted_genek[i+1])-int(sorted_genek[i])==1:
		#print(sorted_genek[i+1],sorted_genek[i])
		gen_lista.append("SL1344_RS"+sorted_genek[i])
		gen_lista.append("SL1344_RS"+sorted_genek[i+1])		
print(sorted(set(gen_lista)))		
if len(gen_lista)==0:
	print("no possible operon")	
gen_lista=list(sorted(set(gen_lista)))
for i in gen_lista:
	output.writelines(i+"\n")
doksi.close()
output.close()