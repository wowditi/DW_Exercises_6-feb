from basicgraphs import graph

def createPath(N):
    G=graph(N)
    for i in range (N-1):
        G.addedge(G[i], G[i+1])
    return G

def createCycle(N):
    G=createPath(N)
    G.addedge(G[0],G[N-1])
    return G

def createGraph(N):
    G=graph(N)
    for i in range (N-1):
        for j in range (i+1,N):
            G.addedge(G[i], G[j])
    return G


def disjointUnion(G, H):
    vmap={}
    K=graph()
    for v in G.V() + H.V():
        vmap[v] = K.addvertex()
    for e in G.E()+H.E():
        K.addedge(vmap[e.tail()], vmap[e.head()])
    return K


print(disjointUnion(createPath(4),createCycle(10)))