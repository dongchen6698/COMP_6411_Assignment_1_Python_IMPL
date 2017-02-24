import re
import resource
import sys
import time
from operator import itemgetter


class DisjointSet(dict):
    def add(self, item):
        self[item] = item

    def find(self, item):
        parent = self[item]

        while self[parent] != parent:
            parent = self[parent]

        self[item] = parent
        return parent

    def union(self, item1, item2):
        self[item2] = self[item1]


class Edge:
    def __init__(self, startpoint, endpoint, weight):
        self.startPoint = int(startpoint) + 1
        self.endPoint = int(endpoint) + 1
        self.weight = int(weight)

    def __str__(self):
        return "(%d, %d) edge cost: %d \n" % (self.startPoint, self.endPoint, self.weight)


def generateEdgeList(result_mst):
    list = []
    for n in result_mst:
        edge = Edge(n[0], n[1], n[2])
        list.append(edge)

    return list


def kruskal(nodesList, edgesList):
    forest = DisjointSet()
    mst = []
    for n in nodesList:
        forest.add(n)

    for e in sorted(edgesList, key=itemgetter(2)):
        n1, n2, _ = e
        t1 = forest.find(n1)
        t2 = forest.find(n2)
        if t1 != t2:
            mst.append(e)
            forest.union(t1, t2)

    return mst


def getNodesList(nodesCount):
    nodesList = []
    for n in range(nodesCount):
        nodesList.append(str(n))

    return nodesList


def getEdgeList(nodesCount, filePath):
    f = open(filePath, 'r')
    graph = [[0 for i in range(nodesCount)] for j in range(nodesCount)]
    edgesList = []
    for a in range(nodesCount):
        valueList = re.findall('\d+', f.readline())
        for b in range(nodesCount):
            graph[a][b] = valueList.pop(0)

    for x in range(nodesCount):
        for y in range(x, nodesCount):
            if graph[x][y] is 0:
                continue
            else:
                edgesList.append((str(x), str(y), graph[x][y]))

    return edgesList


def fromResultToFile(nodesCount,edgeList, durationTime, memory):
    sumStr = ''
    sumValue = 0
    out = open("Result_of_Graph_G_N_%s.txt" % nodesCount, 'w+')
    out.write("Total number of nodes = %s \n" % nodesCount)
    out.write("Total number of edges in the minimum spanning three = %s \n" % str(len(edgeList)))
    out.write("List of edges & their costs: \n")
    for edge in edgeList:
        out.write(str(edge))
        sumStr += str(edge.weight) + " + "
        sumValue += edge.weight
    out.write("Total cost of minimum spanning tree is = Sum of ( %s ) = %s \n" % (sumStr[0:-3], sumValue))
    out.write("Total execution time is = %s milliseconds \n" % (durationTime*1000))
    out.write("Total memory consumption is = %s bytes \n" % memory)
    out.close()


def main():
    if len(sys.argv) == 3:

        nodesCount = int(sys.argv[1])
        filePath = sys.argv[2]
        nodes = getNodesList(nodesCount)
        edges = getEdgeList(nodesCount, filePath)

        startTime = time.time()
        result_mst = kruskal(nodes, edges)
        endTime = time.time()
        durationTime = endTime - startTime

        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


        edgelist = generateEdgeList(result_mst)

        fromResultToFile(nodesCount, edgelist , durationTime, memory)
        print("Finish calculate")


if __name__ == '__main__':
    main()








