#encoding=utf-8
from tkinter import*
from sys import*

def Diviseur(g):
    R1,C=[],[]
    for j in range(len(g)):
        b=ord(g[j:j+1])
        while (b!=0):
            C.append(b%2)
            b=b//2
        C.reverse()
        for i in C:R1.append(i)
        C=[]
    return R1

def Compression(A):
    A0,k,let=[],0,""
    A.append(2)
    for i in range(len(A)-1):      #compte les 0 et les 1 par fragment
        if (A[i]==A[i+1]):k+=1
        elif (A[i]!=A[i+1]):
            if (k==0):
                A0.append(A[i])
            else:
                A0.append(k+1)
                A0.append(A[i])
            k=0
    for i in range(len(A0)):#convertis chaque chiffre en charactère
        let+=chr(A0[i]+48)  #sans changer de valeur numérique.
    return let

def Cryptage(B1,n1,g):
    n1=n1+1
    d1=len(g)
    B1.append(g)      #Insert le mot de passe dans le meme vecteur
    R1=[]      #que celui du texte et de la clé
    for i in Diviseur(g):R1.append(i)
    A2,H,i1=[],[],0
    while(i1<=n1-1):
        let=B1[i1]
        d=len(let)
        if(i1!=n1-1):d=len(let)-1
        if(ord(let[0:1])==10):d+=1
        R=[]
        for i in range(d):R.append(ord(let[i:i+1]))
        C,A3=[],[]
        lett=""
        for j in range(d):
            b=R[j]
            while(b!=0):
                C.append(b%2)
                b//=2
            lett+=chr(len(C)+48)
            C.reverse()
            for i in C:A3.append(i)
            C=[]
        A2.append(lett)
        A=[]
        if (i1<n1-1):
            if (len(R1)<=len(A3)):
                k=0
                while (k<=len(A3)):
                    for j in range(len(R1)):
                        if((j+k)!=len(A3)):
                            if(A3[j+k]!=R1[j]):A.append(A3[j+k]+R1[j]) #représente la somme des 2
                            elif(A3[j+k]==R1[j]):A.append(A3[j+k]-R1[j])   #codes binaires(texte et clé)
                        else:break
                    k+=len(R1)
            else:
                for j in range(len(A3)):
                    if(A3[j]!=R1[j]):A.append(A3[j]+R1[j])  #représente la somme des 2
                    elif(A3[j]==R1[j]):A.append(A3[j]-R1[j])  #codes binaires(texte et clé)
        else:
            for j in range(len(R1)):A.append(1-R1[j])
        H.append(Compression(A))
        i1+=1
    for i in range(i1):
        A=[]
        for j in Diviseur(A2[i]):A.append(j)
        A2[i]=Compression(A)
    B2,j=[],0
    for i in range(i1-1):
        B2.append(H[i])
        B2.append(A2[i])
    B2.append(H[i1-1]+" "+A2[i1-1])
    return B2

def Decryptage1(F,H,g,n1):
    A1,B1=[],[]
    for i in Diviseur(g):A1.append(i)
    i1=0
    while(i1<n1):
        g=H[i1]
        d=len(g)       #décompresse chaque code binaire
        g1,let=g[d-1:d],""      #du texte
        if("0"<=g[0:1] and g[0:1]<="9" and "0"<=g[d-1:d] and g[d-1:d]<="9"):
            let+=g[0:d]
        elif("0"<=g[0:1] and g[0:1]<="9" and (g[d-1:d]=="*" or g[d-1:d]=="\n")):
            let+=g[0:d-1]
        elif(g[0:1]<="9" or "0"<=g[0:1] and g[d-1:d]!='*'):let+=g[1:d]
        else:let+=g[1:d-1]
        d=len(let)
        if("0"<=let[d-1:d] and let[d-1:d]<="9"):d=d
        else:d-=1
        A=[]
        for i in range(d):
            A.append(ord(let[i:i+1])-48)
        g,k="",0
        for i in range(d):
            if(A[i]<=1):
                g+=chr(A[i]+48)
                k+=1
            elif(A[i]>1):
                for j in range(A[i]-1):
                    g+=chr(A[i+1]+48)
                k+=j-2
            k=k
        d=len(g)
        R1=[]
        for i in range(d):R1.append(ord(g[i:i+1])-48)
        A4=[]
        if(g1=="*"):
            if(len(A1)<d):d=len(R1)
            else:d=d
            for j in range(d):A4.append(1-R1[j])
        else:
            k=0
            while(k<=d):
                for j in range(len(A1)):
                    if(j+k<d):
                        if(R1[j+k]!=A1[j]):A4.append(R1[j+k]+A1[j])   #représente la somme des 2 codes binaeires
                        elif(R1[j+k]==A1[j]):A4.append(R1[j+k]-A1[j])   #(texte et clé)
                    else:break
                k+=len(A1)
        i2=d            #représente la dimension du diviseur R1
        g,let="",""
        g=F[i1]
        d=len(g)       #décompresse chaque code binaire
        if("0"<=g[0:1] and g[0:1]<="9"):let+=g[0:d]       #du diviseur
        else:let+=g[1:d]
        d=len(let)
        A,g=[],""
        for i in range(d):A.append(ord(let[i:i+1])-48)
        k=0
        for i in range(d):
            if(A[i]<=1):
                g+=chr(A[i]+48)
                k=k+1
            elif(A[i]>1):
                for j in range(A[i]-1):g+=chr(A[i+1]+48)
                k+=j-2
            k=k
        A3=[]
        for i in range(len(g)):
            if(g[i:i+1]=="1" or g[i:i+1]=="0"):A3.append(ord(g[i:i+1])-48)
        R1,i=[],0
        while(i<len(A3)):
            K=0
            for j in range(6):K+=A3[i+j]*(2**(5-j))
            R1.append(K-48)           #represente les puissance de 2
            i=i+j+1
        j1,g=0,""
        for i in R1:      #convertis chaque code binaire en ASCII
            k=0
            for j in range(1,i+1):k+=A4[j+j1-1]*(2**(i-j))
            g+=chr(k)          #convertis le code ASCII en charactère
            j1+=i
        B1.append(g)
        i1+=1
    return B1

def file_name(event):
    File2=str(enter1.get())
    Password=str(enter2.get())
    open_file(File2,Password)
    fen.destroy()

def out(File2):
    fen1=Tk()
    can1=Frame(fen1,width=150,height=15)
    chaine=Label(fen1)
    if(File2=="py"):chaine.configure(text="Your Password is Wrong, Try Again")
    elif(File2=="vide"):chaine.configure(text="This File is Empty")
    elif(File2=="existe"):chaine.configure(text="This File isn't exist")
    else:chaine.configure(text="Impossible To Open The File "+File2)
    chaine.grid(padx=10,pady=10)
    can1.grid()
    
def verify(B2,File2):
    try:
        filout=open(File2,'w',encoding="utf-8")
        for i in B2:filout.write(i+'\n')
    except:
        out(File2)
        filout.close()

def open_file(File2,Password):
    n1=0
    try:
        filin=open(File2,"r",encoding="utf-8")
        T=filin.readlines()
        if(len(T)==0):out("vide")
        n1,B3=0,[]
        for u in T:
            B3.append(u)
            n1+=1
    except:
        if(n1==0):out("existe")
        else:out(File2)
    t,i,k=[],0,-1
    for i in range(n1-1):
        P=B3[i]
        if(len(P)<20):K=len(P)
        else:K=20
        for k in range(1,K):t.append(ord(P[k:k+1]))
    if(k!=-1):
        L1,L2=0,0
        for i in range(len(t)):
            if(48<=t[i] and t[i]<=57):L1+=1
            else:L2+=1
        filin.close()
        if(L2<L1):
            F,H,B1,g,g1=[],[],[]*2,"",""
            g+=B3[n1-1]
            for j in range(len(g)):
                if(g[j:j+1]==" "):break
                g1+=g[j:j+1]
            g1+='*'
            H.append(g1)
            k=len(g1)
            F.append(g[k:])
            for i in Decryptage1(F,H,Password,1):B1.append(i)    #Decrypte la clé
            if(B1[0]==Password):
                F1,H1,B1=[],[],[]
                for i in range(0,n1-1,2):
                    H1.append(B3[i])
                    F1.append(B3[i+1])
                for i in Decryptage1(F1,H1,Password,len(H1)):B1.append(i)    #Decrypte le fichier
                for i in range(len(B1)):print("i=",i,B1[i])
                verify(B1,File2)
            else:out("py")
        elif(L1<L2):
            B1,B2=[],[]
            for i in range(n1):B1.append(B3[i])
            for i in Cryptage(B1,len(B1),Password):B2.append(i)        #Crypte le fichier
            for i in range(len(B2)):print("i=",i,B2[i])
            verify(B2,File2)
fen=Tk()
can=Frame(fen,width=150,height=15)
text=Label(fen,text="Remplissez les cases ci-dessous").grid(row=1,sticky=E)
text1=Label(fen,text="Enter a File's name").grid(row=2,sticky=W,pady=10)
text2=Label(fen,text="Enter your Password").grid(row=3,sticky=W,pady=10)
enter1=Entry(fen)
enter1.bind("<Return>",file_name)
enter1.grid(row=2,column=2)
enter2=Entry(fen)
enter2.bind("<Return>",file_name)
enter2.grid(row=3,column=2)
Button(fen,text="Quitter",command=fen.destroy).grid(row=5,column=3,padx=10)
can.grid()
fen.mainloop()
