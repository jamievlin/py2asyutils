#!/usr/bin/env python3
import sys
import json 
import datetime
import io

def main(args):
    if len(args) == 1:
        graphobj = json.loads(sys.stdin.read())
    else:
        graphfile = io.open(args[1])
        graphdata = graphfile.read()
        graphfile.close()

        graphobj = json.loads(graphdata)
    print('// Generated by graph2asy.')
    print('// Python Script written by Supakorn "Jamie" R. :)')
    print('// Created at {0}'.format(datetime.datetime.now()))
    print('')

    print('// header')
    print(graphobj['options']['header'])

    definededges = {}
    drawnedges = set()
    nodespos = {}
    edgeslist = []
    edgecount = 0

    print('')
    print('// options')
    print('real circrad=', graphobj['options']['circrad'],';')
    print('pen filloptpen=', graphobj['options']['fillbackground'], ';')

    arrowstyle = graphobj['options']['arrowstyle']

    for nodes in graphobj['graph']:
        nodespos[nodes['id']] = nodes['pos']
        for outnodes in nodes['outnodes']:
            edgeslist.append((nodes['id'], outnodes))

    print('// edges')

    # print('picture edgepic;')
    # edges
    for edge in edgeslist:
        print('// processing edge {0}'.format(edge))
        if ordtuple(edge) not in definededges:
            print('path edge_{0}={1}--{2};'.format(edgecount, tuple(nodespos[edge[0]]), tuple(nodespos[edge[1]])))
            curredge = edgecount
            definededges[ordtuple(edge)] = edgecount
            edgecount += 1
            reversedEdge = False
        else:
            curredge = definededges[ordtuple(edge)]
            reversedEdge = True

        if graphobj['options']['directed']:
            lineProp = '1.0 - circrad/arclength(edge_{0})'.format(curredge)
            print('draw({2}(edge_{0}),arrow=Arrow({3}Relative({1})));'.format(curredge, lineProp,
                                                                         'reverse' if reversedEdge else '',
                                                                               arrowstyle + ',' if arrowstyle is not None else ''))
        else:
            if ordtuple(edge) not in drawnedges:
                print('draw(edge_{0});'.format(curredge))
                drawnedges.add(ordtuple(edge))

        print('')

    # vertices
    print('')
    print('// vertices')

    for nodes in graphobj['graph']:
        postuple = str(tuple(nodes['pos']))
        print('// processing node id {0}'.format(nodes['id']))
        print('filldraw(circle({0},circrad),fillpen=filloptpen);'.format(postuple))
        print('label("{0}", {1});'.format(nodes['text'], postuple))
        print('')

def ordtuple(tup: tuple):
    return (min(tup), max(tup));

if __name__ == '__main__':
    sys.exit(main(sys.argv) or 0)
