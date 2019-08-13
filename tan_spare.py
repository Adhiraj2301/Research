import math, sys, pygame, random
from math import *
from pygame import display,draw,event
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK= (  0,   0,  0)
box = (1200, 650)
running = True
ar=[]
wp=[]
di={}
n=0
m=0
ch=-1

def drawCirc(x0,x1,x2,col):
    pygame.draw.circle(screen,col,(x0,x1),x2)
def boundary(st,s,cr1,cr2,cr3,cr4):
    flag=0
    k1=(cr1[1]-st[1])/(s[1]-st[1])
    if(k1>0 and k1<1):
        flag=1
        return flag
    k2=(cr2[0]-st[0])/(s[0]-st[0])
    if(k2>0 and k2<1):
        flag=1
        return flag
    k3=(cr4[1]-st[1])/(s[1]-st[1])
    if(k3>0 and k3<1):
        flag=1
        return flag
    k4=(cr3[0]-st[0])/(s[0]-st[0])
    if(k4>0 and k4<1):
        flag=1
        return flag
    return flag
        
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
    if yc==0:
        yc=0.1
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
        sdx1=ar[pos][0]+1.1*(solx1-ar[pos][0])
        sdx2=ar[pos][0]+1.1*(solx2-ar[pos][0])
        sdy1=ar[pos][1]+1.1*(soly1-ar[pos][1])
        sdy2=ar[pos][1]+1.1*(soly2-ar[pos][1])
        d1=root((st[0]-sdx1)*(st[0]-sdx1)+(st[1]-sdy1)*(st[1]-sdy1))
        d2=root((st[0]-sdx2)*(st[0]-sdx2)+(st[1]-sdy2)*(st[1]-sdy2))
        sx1=st[0]+((ar[pos][2]+d1)/d1)*(sdx1-st[0])
        sx2=st[0]+((ar[pos][2]+d2)/d2)*(sdx2-st[0])
        sy1=st[1]+((ar[pos][2]+d1)/d1)*(sdy1-st[1])
        sy2=st[1]+((ar[pos][2]+d2)/d2)*(sdy2-st[1])
        pygame.draw.line(screen,BLACK,st,(sx1,sy1),1)
        pygame.draw.line(screen,BLACK,st,(sx2,sy2),1)
        pygame.draw.line(screen,BLACK,(sx1,sy1),ed,1)
        pygame.draw.line(screen,BLACK,(sx2,sy2),ed,1)
        pygame.display.update()
        return sx1,sx2,sy1,sy2
def sub(st,ed,ar,cor1,cor2,cor3,cor4):
    while(1):
                pygame.draw.line(screen,BLACK,st,ed,1)
                pygame.display.update()
                pos,count=closest_circ(st,ed)
                if count==0:
                    pygame.draw.line(screen,RED,st,ed,2)
                    pygame.display.update()
                    break
                sx1,sx2,sy1,sy2=draw_tan(st,ed,pos)
                s1=(sx1,sy1)
                s2=(sx2,sy2)
                flag1=boundary(st,s1,cor1,cor2,cor3,cor4)
                flag2=boundary(st,s2,cor1,cor2,cor3,cor4)
                if(flag1==1):
                    pygame.draw.line(screen,RED,st,s2,2)
                    st=s2
                    continue
                elif(flag2==1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    st=s1
                    continue
                pos1,count1=closest_circ(st,s1)
                pos2,count2=closest_circ(st,s2)
                tsel=0
                if(count1!=0 and count2!=0):
                    if(count1>count2):
                        sub(st,s2,ar)
                        break
                    elif(count2>count1):
                        sub(st,s1,ar)
                        break
                    else:
                        pos3,count3=closest_circ(s1,ed)
                        pos4,count4=closest_circ(s2,ed)
                        if(count3>count4):
                            sub(st,s2,ar)
                            break
                        elif(count4>count3):
                            sub(st,s1,ar)
                            break
                        else:
                            d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                            d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                            if(d1>d2):
                                sub(st,s2,ar)
                                break
                            else:
                                sub(st,s1,ar)
                                break
                elif(count1>count2):
                    pygame.draw.line(screen,RED,st,s2,2)
                    tsel=1
                    pygame.display.update()
                elif(count2>count1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    pygame.display.update()
                else:
                    pos3,count3=closest_circ(s1,ed)
                    pos4,count4=closest_circ(s2,ed)
                    if(count3>count4):
                        pygame.draw.line(screen,RED,st,s2,2)
                        tsel=1
                        pygame.display.update()
                    elif(count4>count3):
                        pygame.draw.line(screen,RED,st,s1,2)
                        pygame.display.update()
                    else:
                        d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                        d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                        if(d1>d2):
                            pygame.draw.line(screen,RED,st,s2,2)
                            tsel=1
                            pygame.display.update()
                        else:
                            pygame.draw.line(screen,RED,st,s1,2)
                            pygame.display.update()
                if(tsel==0):
                    pos,count3=closest_circ(s1,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s1,ed,2)
                        pygame.display.update()
                        break
                    else:
                        tsel=2
                else:
                    pos,count3=closest_circ(s2,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s2,ed,2)
                        pygame.display.update()
                        break
                    else:
                        tsel=3
                if(tsel==2):
                    st=s1
                if(tsel==3):
                    st=s2                
def main():
    flag=0
    global running, screen
    global n,m
    pygame.init()
    screen = pygame.display.set_mode(box)
    pygame.display.set_caption("TANGENT_TEST_MOD")
    screen.fill(WHITE)
    cor1=(20,20)
    cor2=(1180,20)
    cor3=(20,630)
    cor4=(1180,630)
    pygame.draw.line(screen,GREEN,cor1,cor2,2)
    pygame.draw.line(screen,GREEN,cor1,cor3,2)
    pygame.draw.line(screen,GREEN,cor3,cor4,2)
    pygame.draw.line(screen,GREEN,cor4,cor2,2)
    pygame.display.update()
    file=open("C:/Users/Adhiraj/tan_input.txt","r")
    m=int(file.readline())
    for i in range(0,m):
        p=file.readline()
        imp=tuple(int(x.strip()) for x in p.split(','))
        wp.append(imp)
        drawCirc(wp[i][0],wp[i][1],8,BLUE)
    
    n=int(file.readline())   
    for i in range(0,n):
        p=file.readline()
        inp=tuple(int(x.strip()) for x in p.split(','))
        ar.append(inp)
        drawCirc(ar[i][0],ar[i][1],ar[i][2],BLACK)
    
    pygame.display.update()
    count=0
    st_count=0
    ed_count=1
    while running:
        while ed_count<m:
            st=(wp[st_count][0],wp[st_count][1])
            ed=(wp[ed_count][0],wp[ed_count][1])
            while(1):
                pygame.draw.line(screen,BLACK,st,ed,1)
                pygame.display.update()
                pos,count=closest_circ(st,ed)
                if count==0:
                    pygame.draw.line(screen,RED,st,ed,2)
                    pygame.display.update()
                    break
                sx1,sx2,sy1,sy2=draw_tan(st,ed,pos)
                s1=(sx1,sy1)
                s2=(sx2,sy2)
                flag1=boundary(st,s1,cor1,cor2,cor3,cor4)
                flag2=boundary(st,s2,cor1,cor2,cor3,cor4)
                if(flag1==1):
                    pygame.draw.line(screen,RED,st,s2,2)
                    st=s2
                    continue
                elif(flag2==1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    st=s1
                    continue
                pos1,count1=closest_circ(st,s1)
                pos2,count2=closest_circ(st,s2)
                tsel=0
                if(count1!=0 and count2!=0):
                    if(count1>count2):
                        sub(st,s2,ar,cor1,cor2,cor3,cor4)
                        st=s2
                        continue
                    elif(count2>count1):
                        sub(st,s1,ar,cor1,cor2,cor3,cor4)
                        st=s1
                        continue
                    else:
                        pos3,count3=closest_circ(s1,ed)
                        pos4,count4=closest_circ(s2,ed)
                        if(count3>count4):
                            sub(st,s2,ar,cor1,cor2,cor3,cor4)
                            st=s2
                            continue
                        elif(count4>count3):
                            sub(st,s1,ar,cor1,cor2,cor3,cor4)
                            st=s1
                            continue
                        else:
                            d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                            d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                            if(d1>d2):
                                sub(st,s2,ar,cor1,cor2,cor3,cor4)
                                st=s2
                                continue
                            else:
                                sub(st,s1,ar,cor1,cor2,cor3,cor4)
                                st=s1
                                continue
                elif(count1>count2):
                    pygame.draw.line(screen,RED,st,s2,2)
                    tsel=1
                    pygame.display.update()
                elif(count2>count1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    pygame.display.update()
                else:
                    pos3,count3=closest_circ(s1,ed)
                    pos4,count4=closest_circ(s2,ed)
                    if(count3>count4):
                        pygame.draw.line(screen,RED,st,s2,2)
                        tsel=1
                        pygame.display.update()
                    elif(count4>count3):
                        pygame.draw.line(screen,RED,st,s1,2)
                        pygame.display.update()
                    else:
                        d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                        d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                        if(d1>d2):
                            pygame.draw.line(screen,RED,st,s2,2)
                            tsel=1
                            pygame.display.update()
                        else:
                            pygame.draw.line(screen,RED,st,s1,2)
                            pygame.display.update()
                if(tsel==0):
                    pos,count3=closest_circ(s1,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s1,ed,2)
                        pygame.display.update()
                        break
                    else:
                        tsel=2
                else:
                    pos,count3=closest_circ(s2,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s2,ed,2)
                        pygame.display.update()
                        break
                    else:
                        tsel=3
                if(tsel==2):
                    st=s1
                if(tsel==3):
                    st=s2
            st_count=st_count+1
            ed_count=ed_count+1
        ev = pygame.event.get()
        for event in ev:            
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                
if __name__ == '__main__':
    main()
    
        

