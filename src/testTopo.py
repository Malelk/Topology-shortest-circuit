import random
import getTopo
import json
import heapq
ip='127.0.0.1'
def printType(a):
    print(type(a))
topo = json.loads(getTopo.link(ip))["network-topology"]["topology"][0]
links = topo['link']
nodes = topo['node']
projectpath="/home/anti/TopoPath"
# printType(node)
# print(len(node))
i=0
g = getTopo.Graph()
nodeTable={}
while i<len(nodes):
    nodes[i]['link'] = []
    nodeTable[nodes[i]["node-id"]]=i
    g.addNode()
    g.node[g.numnode-1].setId(nodes[i]["node-id"])
    i+=1
i=0
while i<len(links):
    src_str = links[i]["source"]["source-node"]
    dst_str = links[i]["destination"]["dest-node"]
    g.addLink("DG",nodeTable[src_str],nodeTable[dst_str],random.randint(100,500))
    i+=1
cnt = 0
# g.ShortPath(0)
g.ShortPathAll()
json_str = json.dumps(g.path,indent=1)
getTopo.save_data(projectpath+"/test/Path.json",json_str)