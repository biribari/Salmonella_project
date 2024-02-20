file = open("SL1344-merge-good1412.gtf", "r")
#file2 = open("hianyzo_f.txt", "r") read as a list
file3 = open("Salmonella_CLC_CDSs.gtf", "r")
out = open("Sl1344-all.gtf", "w")

lista351=[]
szamrendezettlista=[]
nevrendezettlista=[]
rossz_jo={
"NC_016810":"gi|378697983|ref|NC_016810.1|",
"NC_017718":"NC_017718.1",
"NC_017719":"gi|386730646|ref|NC_017719.1|",
"NC_017719.1":"gi|386730646|ref|NC_017719.1|",
"NC_017720":"NC_017720.1"}

list_open = open ("hianyzo_f.txt", "r")
lines = list_open.readlines()
clclista=file3.readlines()
for i, sor in enumerate(lines):
	lines[i]=sor[:-1]

for sor2 in lines:
	for sor3 in clclista:
		if sor3.split('"')[1]==sor2:
			"""sor3split=sor3.split("\t")
			#print(sor3split[0])
			if sor3split[0]==rosszgenomnev:
				sor3split[0]=jogenomnev
				sor3="\t".join(sor3split)
			"""
			lista351.append(sor3)
			break
eredetifilelist=file.readlines()
eredetifilelist[0]=eredetifilelist[0][3:]
#print(eredetifilelist[0])
eredetifilelist=eredetifilelist+lista351
#print(rossz_jo.values())

for z, sor4 in enumerate(eredetifilelist):
	if sor4.split("\t")[0] in rossz_jo:
		#print(sor4)
		eredetifilelist[z]="\t".join([rossz_jo[eredetifilelist[z].split("\t")[0]]]+eredetifilelist[z].split("\t")[1:])
		#print("\t".join(eredetifilelist[z]))
		#break
szamrendezettlista.append(eredetifilelist[0])
#print(szamrendezettlista)
for x, sor5 in enumerate(eredetifilelist):
	if x==0:
		print("0")
	else:
		for n, sor6 in enumerate(szamrendezettlista):
			#print(sor5.split("\t")[3])
			if int(sor5.split("\t")[3])<int(sor6.split("\t")[3]):
				szamrendezettlista.insert(n,sor5)
				break
		if szamrendezettlista[n]!=sor5:
			szamrendezettlista.append(sor5)
	#print("utána:")
kulonlista=list(rossz_jo.values())
kulonlista=kulonlista[:2]+kulonlista[3:]
print(kulonlista)

for nev in kulonlista:
	for sor7 in szamrendezettlista:
		if sor7.split("\t")[0]==nev:
			nevrendezettlista.append(sor7)
'''for nev in kulonlista:
	for kaki, sor8 in enumerate(nevrendezettlista):
		if sor8.split("\t")[0]==nev:
			for valami in range(5):
				print(nevrendezettlista[kaki+valami])
			break'''
for outsor in nevrendezettlista:
	out.writelines(outsor)
'''
	if x==2:
		break

for elem in szamrendezettlista:
	print(elem.split["\t"][3])


'''
file.close()
file3.close()
out.close()