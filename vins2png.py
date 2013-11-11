#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, Image, ImageDraw, re
from xml.dom.minidom import parse

def parse_color(attr):
    mo = re.search('rgb\(([0-9]*),([0-9]*),([0-9]*)\)',attr)
    if mo==None:
        return (0,0,0)
    return tuple(map(int,[mo.group(1),mo.group(2),mo.group(3)]))

def rasterize(f, draw, X1, Y1, W, H, max_level=100):
    dom = parse(f)
    w,h = int(dom.documentElement.getAttribute('width')),int(dom.documentElement.getAttribute('height'))
    def trans((x,y)):
       X,Y = W*x/w,H*y/h
       return (X+X1,Y+Y1)
    for l in dom.getElementsByTagName('line'):
        x1,y1,x2,y2 = map(float,[l.getAttribute('x1'),l.getAttribute('y1'),l.getAttribute('x2'),l.getAttribute('y2')])
        draw.line([trans((x1,y1)),trans((x2,y2))],fill=parse_color(l.getAttribute('stroke')))
    for r in dom.getElementsByTagName('rect'):
        x,y,ww,hh = map(float,[r.getAttribute('x'),r.getAttribute('y'),r.getAttribute('width'),r.getAttribute('height')])
        draw.rectangle([trans((x,y)),trans((x+ww,y+hh))],fill=parse_color(r.getAttribute('fill')))
    for p in dom.getElementsByTagName('polygon'):
        pts = map(lambda xy:tuple(map(float,xy.split(','))),p.getAttribute('points').split())
        draw.polygon(map(trans,pts),fill=parse_color(p.getAttribute('fill')))
    #for c in dom.getElementsByTagName('call'):
        # Bob : ce cas va être difficile !

def main():
    global w,h
    w,h = int(sys.argv[2]), int(sys.argv[3])
    img = Image.new('RGB',(w,h))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(w,h)],fill=(255,255,255))
    rasterize(sys.argv[1],draw,0,0,w-1,h-1)
    img.save(sys.argv[4])

main()
