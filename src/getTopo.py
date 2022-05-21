import imp
from operator import truediv
from pickle import FALSE
from tracemalloc import start
import requests
import json
import heapq
def link(ip):
    url  = 'http://localhost:8181/restconf/operational/network-topology:network-topology'.format(ip)
    headers = {
        'connection':'close',
        'content-encoding':'gzip',
        'content-type':'application/yang.data+json'
    }
    r = requests.get(url,headers=headers,auth=('admin','admin'))
    return r.text
def node(ip):
    url  = 'http://localhost:8181/restconf/operational/opendaylight-inventory:nodes'.format(ip)
    headers = {
        'connection':'close',
        'content-encoding':'gzip',
        'content-type':'application/yang.data+json'
    }
    r = requests.get(url,headers=headers,auth=('admin','admin'))
    return r.text
# class link:
class Edge:
    def __init__(self,dst,value ):
        self.dst=dst
        self.value=value
class Node:
    def __init__(self):
        self.link=[]
        self.dst=[]
    def setId(self,str):
        self.id = str
class Graph:
    
    
    def __init__(self):
        self.way=[]
        self.predict=[]
        self.numadj=0
        self.numnode=0
        self.node=[]
        self.path={}
    def addNode(self):
        node=Node()
        self.node.append(node)
        self.numnode+=1
    def addonelink(self,src,dst,value):
        link=Edge(dst,value)
        self.node[src].link.append(link)
    def addLink(self,type="UDG",src=0,dst=0,value=0):
        if(type=="UDG"):
            self.addonelink(src,dst,value)
            self.addonelink(dst,src,value)
        if(type=="DG") :
            self.addonelink(src,dst,value)
        return
    def ShortPath(self,start):
        dis = []
        book = []
        pre  = []
        heap = []
        INF = 999999999
        i = 0
        while i < self.numnode:
            dis.append( INF)
            book.append(False)
            pre.append(-1)
            i+=1
        pre[start]= -1
        dis[start]=0
        v = 0
        heapq.heappush(heap,(0,start))
        while len(heap) > 0:
            v_dis,v=heapq.heappop(heap)
            # print(v_dis,v)
            if(book[v]==True):
                continue
            book[v]=True
            if(self.node[v].id[0]=='h'):
                continue
            for edge in self.node[v].link:
                dst = edge.dst
                val = edge.value
                # print(dst,val,book[dst])
                new_dis = v_dis+val
                if new_dis < dis[dst] and ( not book[dst]):
                    
                    dis[dst] = new_dis
                    pre[dst] = v
                    heapq.heappush(heap,(new_dis,dst))
        i = 0
        path_start={}
        path_start["src_id"]=self.node[start].id
        while i < self.numnode:
            path_to_i={}
            path_to_i["dest_node"]=self.node[i].id
            path_to_i["Path"]=[self.node[i].id]
            if(i==start):
                path_to_i["Connected"]=True
            else:
                if(pre[i]==-1):
                    path_to_i['Connected']=False
                else:
                    path_to_i['Connected']=True
                    j = pre[i]
                    while j!=-1:
                        path_to_i['Path'].append(self.node[j].id)
                        j = pre[j]
            path_to_i['Path'].reverse()
            path_start[self.node[i].id]=path_to_i
            # print(path_to_i)
            i+=1
        self.path[self.node[start].id]=path_start
        # print(path_start)
    def ShortPathAll(self):
        for i in range(0,self.numnode):
            self.ShortPath(i)
def save_data(filename,content):
    with open(filename,'w',encoding='utf-8') as f:
            f.write(content)
                
