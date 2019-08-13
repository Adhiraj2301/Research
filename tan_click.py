# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 19:12:45 2019

@author: Adhiraj
"""

import math, sys, pygame, random
from math import *
from pygame import display,draw,event
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK= (  0,   0,  0)
box = (1200, 700)
running = True
ar=[]
di={}
n=0
ch=-1
def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)
def drawCircle(z):
    (x,y)=getPos()
    pygame.draw.circle(screen,z,(x,y),10)

def drawObs(x0,x1,x2):
    pygame.draw.circle(screen,BLACK,(x0,x1),x2)

def root(num):
    return math.sqrt(num)
def closest_circ(st,ed):
    ex=st[0]
    ey=st[1]
    dx=ed[0]-st[0]
    dy=ed[1]-st[1]
    a=(dx*dx)+(dy*dy)
    for i in range(0,n):
        zerone=0
        p=ar[i][0]
        q=ar[i][1]
        r=ar[i][2]
        
        b=2*((ex*dx)+(ey*dy)-(dx*p)-(dy*q))
        c=(ex*ex)+(ey*ey)-(2*ex*p)-(2*ey*q)+(p*p)+(q*q)-(r*r)
        dis=(b*b)-(4*a*c)
        if(dis>0):
            s1=(-b + root(dis))/(2*a)
            s2=(-b - root(dis))/(2*a)
            if(0<=s1<=1 and 0<=s2<=1):
                if(s1<s2):
                    sol=s1
                    zerone=1
                else:
                    sol=s2
                    zerone=1
            elif(0<=s1<=1):
                sol=s1
                zerone=1
            elif(0<=s2<=1):
                sol=s2
                zerone=1
        if(zerone==1):
            di[i]=sol
        else:
            di[i]=9999
    val=9999
    pos=0
    count=0
    for i in range(n):
        if(di[i]<val):
            count+=1
    for i in range(0,n):
        if(di[i]<val):
            val=di[i]
            pos=i
    return pos,count
def draw_tan(st,ed,pos):
    xc=st[0]-ar[pos][0]
    yc=st[1]-ar[pos][1]
    co=(ar[pos][0]*ar[pos][0])+(ar[pos][1]*ar[pos][1])-(ar[pos][2]*ar[pos][2])-(ar[pos][0]*st[0])-(ar[pos][1]*st[1])
    at=1+((xc/yc)*(xc/yc))
    bt=((2*co*xc)/(yc*yc))-(2*ar[pos][0])+((2*ar[pos][1]*xc)/yc)
    ct=((co*co)/(yc*yc))+((2*ar[pos][1]*co)/yc)+(ar[pos][0]*ar[pos][0])+(ar[pos][1]*ar[pos][1])-(ar[pos][2]*ar[pos][2])
    dist=(bt*bt)-(4*at*ct)
    if(dist>0):
        solx1=(-bt+root(dist))/(2*at)
        solx2=(-bt-root(dist))/(2*at)
        soly1=-(co+(xc*solx1))/yc
        soly2=-(co+(xc*solx2))/yc
        d=root((st[0]-solx1)*(st[0]-solx1)+(st[1]-soly1)*(st[1]-soly1))
        sx1=st[0]+((ar[pos][2]+d)/d)*(solx1-st[0])
        sx2=st[0]+((ar[pos][2]+d)/d)*(solx2-st[0])
        sy1=st[1]+((ar[pos][2]+d)/d)*(soly1-st[1])
        sy2=st[1]+((ar[pos][2]+d)/d)*(soly2-st[1])
        pygame.draw.line(screen,BLACK,st,(sx1,sy1),1)
        pygame.draw.line(screen,BLACK,st,(sx2,sy2),1)
        pygame.draw.line(screen,BLACK,(sx1,sy1),ed,1)
        pygame.draw.line(screen,BLACK,(sx2,sy2),ed,1)
        pygame.display.update()
        return sx1,sx2,sy1,sy2
def main():
    flag=0
    global running, screen
    global n
    pygame.init()
    screen = pygame.display.set_mode(box)
    pygame.display.set_caption("TANGENT_TEST_MOD")
    screen.fill(WHITE)
    pygame.display.update()
    n=int(input("no. of nodes "))
    
    for i in range(0,n):
        inp=tuple(int(x.strip()) for x in input().split(','))
        ar.append(inp)
        drawObs(ar[i][0],ar[i][1],ar[i][2])
        pygame.display.update()
    
    while running:
        ev = pygame.event.get()

        for event in ev:
            
            if flag==0 and event.type == pygame.MOUSEBUTTONUP:
                screen.fill(WHITE)
                count=0
                for i in range(0,n):
                    drawObs(ar[i][0],ar[i][1],ar[i][2])
                    pygame.display.update()
                flag=1
                drawCircle(BLUE)
                pygame.display.update()
                st=getPos()
                print("Start:")
                print(st)
                
            elif flag==1 and event.type == pygame.MOUSEBUTTONUP:
                flag=0
                drawCircle(RED)
                pygame.display.update()
                ed=getPos()
                print("End:")
                print(ed)
                while(1):
                    pygame.draw.line(screen,BLACK,st,ed,1)
                    pygame.display.update()
                    pos,count=closest_circ(st,ed)
                    if count==0:
                        pygame.draw.line(screen,RED,st,ed,5)
                        pygame.display.update()
                        break
                    sx1,sx2,sy1,sy2=draw_tan(st,ed,pos)
                    s1=(sx1,sy1)
                    s2=(sx2,sy2)
                    pos1,count1=closest_circ(st,s1)
                    pos2,count2=closest_circ(st,s2)
                    tsel=0
                    if(count1>count2):
                        pygame.draw.line(screen,RED,st,s2,5)
                        tsel=1
                        pygame.display.update()
                    elif(count2>count1):
                        pygame.draw.line(screen,RED,st,s1,5)
                        pygame.display.update()
                    else:
                        d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                        d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                        if(d1>d2):
                            pygame.draw.line(screen,RED,st,s2,5)
                            tsel=1
                            pygame.display.update()
                        else:
                            pygame.draw.line(screen,RED,st,s1,5)
                            pygame.display.update()
                    if(tsel==0):
                        pos,count3=closest_circ(s1,ed)
                        if(count3==0):
                            pygame.draw.line(screen,RED,s1,ed,5)
                            pygame.display.update()
                            break
                        else:
                            tsel=2
                    else:
                        pos,count3=closest_circ(s2,ed)
                        if(count3==0):
                            pygame.draw.line(screen,RED,s2,ed,5)
                            pygame.display.update()
                            break
                        else:
                            tsel=3
                    if(tsel==2):
                        st=s1
                    if(tsel==3):
                        st=s2
                
                
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                
            
                
                
if __name__ == '__main__':
    main()
    
        

