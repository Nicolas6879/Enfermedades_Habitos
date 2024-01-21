import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import os

sumaD=0
sumaH=0
sumaCP=0
sumaC=0
contador=0
pesoACC=0
pesoACAL=0
pesoACA=0
pesoACL=0
pesoS=0
pesoF=0

def pesoHabitos(habito):
    if habito=="Alto consumo de carbohidratos":
        global pesoACC
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoACC = int(input())*20
    elif habito=="Alto consumo de alcohol":
        global pesoACAL
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoACAL = int(input())*20
    elif habito=="Alto consumo de azucar":
        global pesoACA
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoACA = int(input())*20
    elif habito=="Alto consumo de lipidos":
        global pesoACL
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoACL = int(input())*20
    elif habito=="Sedentarismo":
        global pesoS
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoS = (5-int(input()))*20
    elif habito=="Fumar":
        global pesoF
        print ("Ingrese la frecuenca con la que", habitos(habito), "(0=Nunca//5=Muy frecuentemente)")
        pesoF = int(input())*20

def suma(enfermedad, habito):
    if enfermedad=="Diabetes":
        global sumaD
        sumaD+=getPeso(habito)
    if enfermedad=="Hipertension":
        global sumaH
        sumaH+=getPeso(habito)
    if enfermedad=="Cancer de pulmon":
        global sumaCP
        sumaCP+=getPeso(habito)
    if enfermedad=="Cirrosis":
        global sumaC
        sumaC+=getPeso(habito)

def getPeso(habito):
    if habito=="Alto consumo de carbohidratos":
        return pesoACC
    elif habito=="Alto consumo de alcohol":
        return pesoACAL
    elif habito=="Alto consumo de azucar":
        return pesoACA
    elif habito=="Alto consumo de lipidos":
        return pesoACL
    elif habito=="Sedentarismo":
        return pesoS
    elif habito=="Fumar":
        return pesoF

def habitos(habito):
    if habito=="Alto consumo de carbohidratos":
        return "consume carbohidratos"
    elif habito=="Alto consumo de alcohol":
        return "consume bebidas alcoholicas"
    elif habito=="Alto consumo de azucar":
        return "consume azucares"
    elif habito=="Alto consumo de lipidos":
        return "consume alimentos altos en grasas o lipdos"
    elif habito=="Sedentarismo":
        return "realiza actividad fisica"
    elif habito=="Fumar":
        return "fuma"

def getSuma(enfermedad):
    if enfermedad=="Diabetes":
        return sumaD/numeroDeHabitos(enfermedad)
    if enfermedad=="Hipertension":
        return sumaH/numeroDeHabitos(enfermedad)
    if enfermedad=="Cancer de pulmon":
        return sumaCP/numeroDeHabitos(enfermedad)
    if enfermedad=="Cirrosis":
        return sumaC/numeroDeHabitos(enfermedad)

def numeroDeHabitos(enfermedad):
    global contador
    for i in E.neighbors(enfermedad):
        contador+=1
    return contador

def imprimirPorcentajes(enfermedad):
    print ("La probabilidad que tenga ",enfermedad," es de ",getSuma(enfermedad),"%, si sigue con esos mismos habitos.")



E = nx.DiGraph() # crear un grafo

#Añadir nodos
E.add_node("Persona")
enfermedades_E = ["Diabetes","Hipertension" , "Cancer de pulmon" , "Cirrosis"]
E.add_nodes_from(enfermedades_E)
habitos_E = ["Alto consumo de carbohidratos" , "Alto consumo de alcohol" , "Alto consumo de azucar" , "Alto consumo de lipidos" , "Sedentarismo" , "Fumar"]
E.add_nodes_from(habitos_E)

#Añadir aristas
E.add_edges_from([("Persona", "Diabetes") , ("Persona", "Hipertension") , ("Persona", "Cancer de pulmon") , ("Persona", "Cirrosis")])
E.add_edges_from([("Diabetes", "Alto consumo de carbohidratos") , ("Diabetes", "Alto consumo de azucar") , ("Diabetes", "Sedentarismo")])
E.add_edges_from([("Hipertension", "Alto consumo de azucar") , ("Hipertension", "Alto consumo de alcohol") , ("Hipertension", "Sedentarismo") , ("Hipertension", "Alto consumo de lipidos")])
E.add_edges_from([("Cancer de pulmon", "Fumar")])
E.add_edges_from([("Cirrosis", "Alto consumo de alcohol") , ("Cirrosis", "Alto consumo de lipidos")])

#Darles valor a los peso de los habitos
for i in habitos_E:
    pesoHabitos(i)

#Asignar peso a los habitos
for i in E.neighbors("Persona"):
    #print(i)
    for j in E.neighbors(i):
        E.edges[i, j]["label"] = getPeso(j)
        suma(i,j)
    print("\n")

#Asignar peso a las enfermedades
for i in E.neighbors("Persona"):
    E.edges["Persona", i]["label"] = getSuma(i)
    contador=0

for i in E.neighbors("Persona"):
    imprimirPorcentajes(i)
    contador=0
#Imprimir grafica del grafo
pos = nx.layout.planar_layout(E)
nx.draw_networkx(E, pos)
labels = nx.get_edge_attributes(E, "Probabilidad")
nx.draw_networkx_edge_labels(E, pos, edge_labels=labels)
plt.rcParams['figure.figsize'] = (12, 8)
plt.title("Grafo de posibles enfermedades")
plt.show()

A = nx.nx_agraph.to_agraph(E)
A.layout('dot')
graphviz.Source(A.to_string())