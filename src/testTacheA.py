
import os

files = ["Instances_genome/Inst_0000010_7.adn","Instances_genome/Inst_0000010_8.adn","Instances_genome/Inst_0000010_44.adn","Instances_genome/Inst_0000012_32.adn","Instances_genome/Inst_0000012_56.adn"]


for i in range(0,len(files)-2):

    print("fichier :",files[i])
    os.system("python adn.py "+files[i]+" -distnaif -t")
	
