import getTopo
import json

class Node:
    """
    type: host/switch

    """
    type = -1
    def __init__(self,type):
        self.type = type
        self.link = []
class Arc:
    def __init__(self,src,dst):
        self.src = src
        self.dst = dst   
