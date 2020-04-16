import random
sbox = [9, 0xb, 0xc, 4, 0xa, 1, 2, 6, 0xd, 7, 3, 8, 0xf, 0xe, 0, 5]
invsbox=[0xe, 5, 6, 0xa, 3, 0xf, 7, 9, 0xb, 0, 4, 1, 2, 8, 0xd, 0xc]
mask=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
clef=[random.randint(0,15),random.randint(0,15)]

#Fonction tour 
def round(state, key):
    return sbox[state ^ key]

#Algorithme de chiffrement avec deux tours 
def enc(msg, key):
    t0=round(msg,key[0])
    t1=round(t0,key[1])
    return t1

def ToyCipher(msg, msg_crypt):
    for k0 in range(0, 16):
        for k1 in range(0, 16):
            t=enc(msg,[k0,k1])
            if t == msg_crypt:
                return [k0,k1]

              
#Fonction qui génère tous les messages possibles avec 4 bits donc 16 messages possibles .
def generate_all_msg(size, key):
    return [(i,enc(i, key)) for i in range(0, 16)]

#fonction qui fait de la force brute en esssayant toutes les clés possibles avec deux tour de chiffrement associés à tous les messages possibles
def bruteforce():
    list_all_msg = generate_all_msg(5, clef)
    for k1 in range(0, 16):
        for k2 in range(0,16):
            contr= 0
            for(msg,cry) in list_all_msg:
                if cry != enc(msg, (k1,k2)):
                    contr = 1
                    break
            if contr ==0:
              k = (k1, k2)
              print("(%x, %x)" % k)
              return k

forcing=bruteforce()
print('la force brute :')
print(forcing)

#fonction qui étant donné une clef et un nombre𝑛de paire à générer, renvoie une liste de𝑛pairesde message aléatoirement choisi et du chiffré correspondant avec la clef donnée.
def kPA(key,numbre):
    tab = []
    for i in range(0,numbre):
        p0= random.randint(0,15)
        t=enc(p0,key)
        tab.append([p0,t])
    return tab
print('execution de la fonction kPA avec un exemple de 6 messages à générer')
print(kPA(clef,6))   
#focntion qui converti un chiffre en binaire et qui compte le nombre de 1 figurant     
def count_nb_1(nombre):
    return bin(nombre).count('1')

#fonction qui calcule pour chaque couple de masques (𝑚𝑎𝑠𝑘𝑖, 𝑚𝑎𝑠𝑘𝑜),pour combien des 16 paires entrée/sortie de la boîte S on a une égalité de parité
def calcul_mask (mask0, mask1):
    nb=0
    for i in range(0, 16):
        parite_entre = count_nb_1(i & mask1) % 2
        parite_sortie = count_nb_1(sbox[i] & mask0) % 2
        if parite_sortie == parite_entre:
            nb=nb+1
    return nb

def generate_all_mask ():
    for mask1 in range(0,16):
        for mask0 in range(0,16):
            i = calcul_mask(mask1,mask0)
            print("mask1 : ",mask1," mask0 : ",mask0," ==> ",i)

print("génération de tous les masque possibles ")
generate_all_mask()            

#Écrire une fonction qui trouve la meilleure paire(𝑚𝑎𝑠𝑘𝑖, 𝑚𝑎𝑠𝑘𝑜)de masques 
def meilleur_score():
 max = 0
 tab = []
 c=0
 maxx=0
 maxtab=[]
 for i in range(1, 16):
    for j in range(1, 16):
        if calcul_mask(i, j) >= max:
            max = calcul_mask(i, j)
 for i in range(1, 16):
    for j in range(1, 16):
        if calcul_mask(i, j) == max:
            tab.append([i, j, max])
 for m in range(0, len(tab)):
    for i in range(0, 1):
        c = c+count_nb_1(tab[m][i])
    if c>maxx:
        maxx=c
        maxtab=[tab[m][0],tab[m][1]]
    c=0
 print("le meilleur score est :", maxtab)
 return maxtab



#fonction qui fait de l'encodage mais avec un seul tour uniquement
def encode2(msg, key):
    t0=round(msg,key[0])
    return t0

#générer 16 paires de message/chiffré connues
print("génération de 16 paires de message et chiffrés connus")
kpa = kPA(clef, 16)
print(kpa)
masks = meilleur_score()

print("Clefs aleatoires générés = ",clef)

# fonction de sélection de candidats pour𝑘0. Cette fonction prend en entrée la liste des pairesmessage/chiffré connues, et les𝑚𝑎𝑠𝑘𝑖et𝑚𝑎𝑠𝑘𝑜sélectionnés précédemment.
def selection (kpa, masks):
    score = 0
    score1 = 0
    score2 = 0
    tab_t = []
    score_key = []
    for key in range(0,16):
        for mes in range(1,len(kpa)):
            t = encode2(kpa[mes][0], [key, key])

            parite_t = count_nb_1(t & masks[0]) % 2
            parite_c = count_nb_1(kpa[mes][1] & masks[1]) % 2
            
            if parite_t == parite_c:
                score1 = score1 + 1
            else:
                score2 = score2 - 1
            if abs(score1) > abs(score2):
                score = score1
            else:
                score = score2
        score_key.append(abs(score))
        score1 = 0
        score2 = 0

    # Le score de la clé 1 est dans la case 1 du tableau score_key
    # Il faut parcourir le tableau score_key et selectionner ceux qui ont le meilleur score
    max_score = 0
    for x in range(0,16):
        if max_score < score_key[x]:
            max_score = score_key[x]

    # On selectionne les clefs qui ont le meilleur score
    clefs_with_max_score = []
    for key in range(0,16):
        if score_key[key] == max_score:
            clefs_with_max_score.append(key)

    print(" Les clefs K0 avec meilleurs scores : ",clefs_with_max_score)
    return clefs_with_max_score

print("------------------------------------------")

def test_unicite(tab, tab1):
    for x in range(0,len(tab)):
        if tab[x]==tab1:
            return 1
    return 0

#Fonction qui, étant donné les𝑘0candidats, trouve la clef (si possible)
def recherch_k1 ():
    clefs_with_max_score = selection(kpa, masks)
    tab_k0_k1 = []
    for k0 in range(0,len(clefs_with_max_score)):
        for k1 in range(0,16):
            message_crypte = enc(kpa[k0][0], [clefs_with_max_score[k0],k1])
            if message_crypte == kpa[k0][1] :
                if test_unicite(tab_k0_k1, [clefs_with_max_score[k0],k1])==0:
                    tab_k0_k1.append([clefs_with_max_score[k0],k1])
        
    print("Les couples de clefs [K0, K1] possibles => ", tab_k0_k1)
    for x in range(0,len(tab_k0_k1)):
        crypt_tab = []
        for z in range(0,len(kpa)):
            c = enc(kpa[z][0], tab_k0_k1[x])
            crypt_tab.append([kpa[z][0],c])
        if crypt_tab == kpa:
            print("La bonne clef est =>",tab_k0_k1[x])
            return tab_k0_k1[x]
    print("Aucune correspondance trouvée")
    



recherch_k1 ()