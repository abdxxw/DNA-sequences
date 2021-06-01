
#usage : type  "python adn.py -h" for help 


import argparse, time, datetime


#gestion des parametre du script 
parser = argparse.ArgumentParser()
parser.add_argument("f", type=str, help="the file to use")
parser.add_argument("-distnaif", "--distancenaif", action="count", default=0)
parser.add_argument("-dist1", "--distance1", action="count", default=0)
parser.add_argument("-sol1", "--align1", action="count", default=0)
parser.add_argument("-dist2", "--distance2", action="count", default=0)
parser.add_argument("-progdyn", "--aligndistance", action="count", default=0)
parser.add_argument("-sol2", "--align2", action="count", default=0)
parser.add_argument("-t", "--time", action="count", default=0)
args = parser.parse_args()



name = args.f # recuperation du nom de fichier


file = open(name, "r")  
n=int(file.readline())	#lecture de l'entier de la premiere ligne
m=int(file.readline())
x=file.readline().split(' ')	# couper le string en tableau de char avec ' ' comme delimiteur 
y=file.readline().split(' ')
x=list(x)[0:len(x)-1] # supprimer le \n 
y=list(y)[0:len(y)-1]
file.close()

CDEL=2
CINS=2
T1 = [[0 for i in range(len(y)+1)] for j in range(len(x)+1)]	#tableau de distance pour DIST_1
T2 = [[0 for i in range(len(y)+1)] for j in range(2)]	#tableau de distance pour DIST_2


def sub(x,y):	#cout de substitution
    if x==y:
        return 0
    if ((x == 'A' and y == 'T') or (x == 'T' and y == 'A')) or ((x == 'G' and y == 'C') or (x == 'C' and y == 'G')): #partie concordante 
        return 3
    return 4

	
def DIST_NAIF(x,y):
    d=float('inf') 
    return DIST_NAIF_REC(x,y,0,0,0,d)


def DIST_NAIF_REC(x,y,i,j,c,dist):

    if i == len(x) and j == len(y):
        if c < dist:
            dist = c
    else:
        if i < len(x) and j < len(y):
            dist = DIST_NAIF_REC(x,y,i+1,j+1,c+sub(x[i],y[j]),dist)

        if i < len(x):
            dist = DIST_NAIF_REC(x,y,i+1,j,c+CDEL,dist)

        if j < len(y):
            dist = DIST_NAIF_REC(x,y,i,j+1,c+CINS,dist)

    return dist

	
def DIST_1(x,y,T1):
    n=len(x)
    m=len(y)
    T1[0][0]=0
    # on construit la matrice n*m dont pour construir chaque case du tableau 
    for i in range(1, n+1):
        T1[i][0] = i*CDEL	
    for j in range(1, m+1):
        T1[0][j] = j*CINS
    for i in range(1, n+1):
        for j in range(1, m+1):
            T1[i][j] = min(T1[i-1][j-1]+sub(x[i-1],y[j-1]),T1[i][j-1]+CINS,T1[i-1][j]+CDEL)
    return T1[n][m]


def DIST_2(x,y,T2):
    n=len(x)
    m=len(y)
    T2[0][0]=0
    # dans dist2 on a travaille avec deux ligne car pour avoir la ligne i on a besoi que de la ligne i-1
    for j in range(1, m+1):
        T2[0][j] = j*CINS
    for i in range(1, n+1):
        T2[1][0] = i*CDEL
        for j in range(1, m+1):
            T2[1][j] = min(T2[0][j-1]+sub(x[i-1],y[j-1]),T2[1][j-1]+CINS,T2[0][j]+CDEL)
        for j in range(m+1):
        	# on ecrace la 1ere ligne et on met la 2eme ligne a ca place 
            T2[0][j] = T2[1][j]

    return T2[1][m]


	
def SOL_1(x,y,T1):
    n=len(x)
    m=len(y)
    i=n
    j=m
    x1=[]
    y1=[]
    # on parcour les deux mots y et x pour retriuver le chemai D
    while (j>0) or (i>0):
    	# pour se faire on aura 3 cas a gerer 
    	# si on la case i,j est obtenu a partire d,une sub
        if (j>0) and (i>0) and (T1[i][j] == T1[i-1][j-1]+sub(x[i-1],y[j-1])):
            x1.append(x[i-1])
            y1.append(y[j-1])
            i-=1
            j-=1
        # si elle est obtenu a partir d'une insertion
        if (j>0) and (T1[i][j] == T1[i][j-1]+CINS):
            x1.append('-')
            y1.append(y[j-1])
            j-=1
        # si elle est obtenu a partir d'une supression 
        if (i>0) and (T1[i][j] == T1[i-1][j]+CDEL):
            x1.append(x[i-1])
            y1.append('-')
            i-=1
    return (x1,y1)

	
def PROG_DYN(x,y):
    T = [[0 for i in range(len(y)+1)] for j in range(len(x)+1)]
    d=DIST_1(x,y,T)
    (x1,y1)=SOL_1(x,y,T)
    x1.reverse() #on inverse le tableau a cause des insertion avec append a la fin 
    y1.reverse()
    x1="".join(x1)	#transformation du tableau de char en string
    y1="".join(y1)
    return (d,x1,y1)



#----definition de la fonction coupure 
def coupure(x,y):
	n=len(x)
	m=len(y)
	# on cree deux tableau: D pour le calcule de distance d'edition et I pour la coupure 
	I = [[0] * (m+1) for i in range(2)]
	D =	[[0] * (m+1) for i in range(2)]
	#initialisation de la 1ere ligne du tableau D
	for k in range(m+1):
		I[0][k]=k
		D[0][k]=CDEL*k
	#on commence le parcour des mots x et y pour cree la matrice permetant de calculer coupure
	for i in range(1,n+1):
		#inialisation de le 1ere colone pour chaque tour de boucle 
		I[1][0]=0
		D[1][0]=CINS*i

		for j in range(1,m+1):
			# pour chaque case du tableau on calcul le meilleur chemain qui mennet a elle 
			# parmis les 3 possible puis dans un tableau I on enregistre le chemain 
			dell=D[1][j-1] +CDEL
			ins =D[0][j] +CINS
			subs=D[0][j-1] + sub(x[i-1],y[j-1])
			D[1][j]=min(dell,ins,subs)
			# le process commence a partir de la ligne n/2 car on a besoins de l'intersection 
			# entre le chemin et la ligne n/2
			if(i>n/2):
				# donc pour chaque case on verfie quelle chemin de D mene a cette case et on garde
				# valeur dans I
				if(D[1][j]==dell):
					I[1][j]=I[1][j-1]
				elif(D[1][j]==ins):
					I[1][j]=I[0][j]
				else:
					I[1][j]=I[0][j-1]
		# pour chaque fin de ligne on remente la ligne 1 pour s'enservir pour ligne suivante
		D[0]=[k for k in D[1]]
		if(i>n/2):
			I[0]=[k for k in I[1]]
	
	print(D[1][m])
	return I[1][len(y)]

# definition de mo gpas 
def  mot_gaps(k):
	#on cree une liste vide et on lui ajoute k gaps
	out=[]
	for x in range(1,k+1):
		out.append('-')
	return out




def align_lettre_mot(x,y):
	#cree un indice pour que a la fin de la boucle on a x=une lettre t tq sub(x,t)=3
	indice=-1
	m=len(y)
	# on parcour tout le mot y et pour chaque lettre t de ce dernier on verfie 3 cas:
	for i in range(0,m):
		# si x=t on retourne directement i*gapr+x+m-i-1 gaps
		if y[i]==x[0] :
			return(mot_gaps(i)+x+mot_gaps(m-i-1),y)
		else:
			# si non on essye de trouver une lettre tq 
			if (sub(x[0],y[i]) == 3):
				if indice!=-1:
					indice=indice
				else:
					indice=i				
	if(indice!=-1):
		return(mot_gaps(indice)+x+mot_gaps(m-indice-1),y)
	return(x+mot_gaps(len(y)-1),y)



	
def SOL_2_REC(x,y):
    m=len(y)
    n=len(x)
    # on gere ici les cas de base qui sont 3 :
    if (len(y)==0):
        return(x,mot_gaps(n))
    if (len(x)==0):
        return(mot_gaps(m),y)
    if (n==1):
        return align_lettre_mot(x,y)
        # ici on gere la recursivite 
    else:
    	#pour chaque x different de 0 on le divise par deux et on trouve la coupure de y 
        index_i= n//2
        index_j=coupure(x,y)
        (ali_x1,ali_y1) =SOL_2(x[0:index_i],y[0:index_j])
        (ali_x2,ali_y2) =SOL_2(x[index_i : n],y[index_j : m])
        return(ali_x1+ali_x2, ali_y1+ali_y2) 
		
		
def SOL_2(x,y):
    (x1,y1) = SOL_2_REC(x,y)
    x1="".join(x1)
    y1="".join(y1)
    return(x1,y1) 



#gestion des parametre du script 
if args.distancenaif:
    t0 = time.time()
    print("Distance naif : "+str(DIST_NAIF(x,y)))
    t1 = time.time()
    tDist_naif = t1-t0
    if args.time:
        print("time used is %f s" %(tDist_naif))
		
if args.distance1:
    t0 = time.time()
    print("Distance methode 1 : "+str(DIST_1(x,y,T1)))
    t1 = time.time()
    tDist1 = t1-t0
    if args.time:
        print("time used is %f s" %(tDist1))
		
if args.align1:
    t0 = time.time()
    print("Alignement methode 1 : "+str.join(SOL_1(x,y,T1)))
    t1 = time.time()
    tSol1 = t1-t0
    if args.time:
        print("time used is %f s" %(tSol1))
		
if args.distance2:
    t0 = time.time()
    print("Distance methode 2 : "+str(DIST_2(x,y,T2)))
    t1= time.time()
    tDist2 = t1-t0
    if args.time:
        print("time used is %f s" %(tDist2))
		
if args.aligndistance:
    t0 = time.time()
    print("Distance1 + Align 1 : "+str(PROG_DYN(x,y)))
    t1 = time.time()
    tProgDyn = t1-t0
    if args.time:
        print("time used is %f s" %(tProgDyn))

if args.align2:
    t0 = time.time()
    print("Alignement methode 2 : "+str(SOL_2(x,y)))
    t1 = time.time()
    tSol2 = t1-t0
    if args.time:
        print("time used is %f s" %(tSol2))


