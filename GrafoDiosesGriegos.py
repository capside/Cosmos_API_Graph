import time, datetime, os
from gremlin_python.driver import client

lista=[]

with open('DiosesGriegos.txt','r') as file:
    lines=file.readlines()
    for line in lines:
            linea2=line.strip().split(sep=',')
            #lista.append("g.addV('"+linea2[2]+"').property('tipo','"+linea2[2]+"').property('id','"+linea2[0]+"').property('genero','"+linea2[1]+"').property('tribu','"+linea2[3]+"')")
            lista.append("g.addV('"+linea2[2]+"').property('id','"+linea2[0]+"').property('genero','"+linea2[1]+"').property('tribu','"+linea2[3]+"')")


#for item in lista:
#   print('item: '+item)

lista_rel=[]
with open('DiosesGriegosRelaciones.txt','r') as file:
    lines=file.readlines()
    for line in lines:
            linea2=line.strip().split(sep=',')
            lista_rel.append("g.V('" + linea2[0] + "').addE('" + linea2[1] +"').to(g.V('" + linea2[2] + "'))")



COSMOS_KEY=os.environ.get('COSMOS_KEY')
cliente = client.Client('wss://cosmos-graph.gremlin.cosmosdb.azure.com:443/', "g", username="/dbs/graph-db/colls/graph-coll",password=COSMOS_KEY)

drop=cliente.submitAsync("g.V().drop()")
print('Resultado del drop: {0}'.format(drop.result().one()))
print('===========')

i=0
for item in lista:
    #time.sleep(0.2)
    res=cliente.submitAsync(item)
    if res.result() is not None:
            i+=1
            print("\tMetemos este vertice, "+str(i)+":\n\t{0}\n".format(res.result().one()))
print('===========')
k=0
time.sleep(2)
for item in lista_rel:
    #time.sleep(1)
    res=cliente.submitAsync(item)
    if res.result() is not None:
            k+=1
            print("\tMetemmos esta arista, "+str(k)+":\n\t{0}\n".format(res.result().one()))
print('===========')

