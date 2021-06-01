
import os

files = ["Instances_genome/Inst_0000010_7.adn","Instances_genome/Inst_0000010_8.adn","Instances_genome/Inst_0000010_44.adn","Instances_genome/Inst_0000012_32.adn","Instances_genome/Inst_0000012_56.adn","Instances_genome/Inst_0000100_7.adn","Instances_genome/Inst_0000500_88.adn","Instances_genome/Inst_0002000_44.adn"]


for i in range(0,len(files)):

    print("fichier :",files[i])
    os.system("python adn.py "+files[i]+" -progdyn -t")
	
