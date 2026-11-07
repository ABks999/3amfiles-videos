import sys, json, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from story import LINES, CAPTIONS
W,H=1080,1920; BW,BH=int(W*1.12),int(H*1.12)
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
M='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def F(p,s): return ImageFont.truetype(p,s)
def base(c1,c2):
    g=np.linspace(0,1,BH)[:,None,None]; a=np.array(c1)*(1-g)+np.array(c2)*g
    return Image.fromarray(np.repeat(a,BW,1).astype('uint8'))
def glow(img,xy,r,col,alpha=0.6):
    l=Image.new('RGB',img.size,(0,0,0)); d=ImageDraw.Draw(l); x,y=xy
    d.ellipse([x-r,y-r,x+r,y+r],fill=col); l=l.filter(ImageFilter.GaussianBlur(r/2))
    return Image.fromarray(np.clip(np.array(img,float)+np.array(l,float)*alpha,0,255).astype('uint8'))
cx=BW//2
def outside():
    im=base((4,6,14),(10,10,16)); d=ImageDraw.Draw(im)
    d.rectangle([0,1500,BW,BH],fill=(14,14,16))
    d.rectangle([150,900,1060,960],fill=(30,30,34))
    for x in (330,605,880): d.rectangle([x-12,960,x+12,1500],fill=(22,22,26))
    for x in (420,790): d.rectangle([x-45,1250,x+45,1500],fill=(28,28,32)); d.rectangle([x-30,1280,x+30,1330],fill=(70,90,80))
    d.rectangle([300,1100,520,1400],fill=(26,26,28))
    im=glow(im,(605,1000),330,(200,170,90),0.55); im=glow(im,(410,1250),150,(200,190,120),0.5)
    d=ImageDraw.Draw(im); d.rectangle([150,955,1060,965],fill=(230,215,160)); d.rectangle([320,1120,500,1380],fill=(150,140,95))
    return im
def phone(red=False):
    im=base((10,8,8),(18,12,10)) if not red else base((25,2,2),(12,0,0)); d=ImageDraw.Draw(im)
    d.rectangle([0,1350,BW,BH],fill=(30,20,14) if not red else (35,6,6))
    d.rounded_rectangle([cx-260,1150,cx+260,1380],40,fill=(20,20,22))
    d.rounded_rectangle([cx-300,1040,cx+300,1160],60,fill=(28,28,30))
    for i in range(3):
        for j in range(4): d.ellipse([cx-120+i*90,1200+j*40,cx-90+i*90,1225+j*40],fill=(60,60,62))
    col=(220,200,170) if not red else (230,40,30)
    for r in (360,460,560): d.arc([cx-r,1100-r,cx+r,1100+r],200,250,fill=col,width=10); d.arc([cx-r,1100-r,cx+r,1100+r],290,340,fill=col,width=10)
    im=glow(im,(cx,1250),400,(120,80,40) if not red else (160,10,10),0.5)
    return im
def cam(man=0):
    im=base((6,6,6),(10,10,10)); d=ImageDraw.Draw(im)
    x0,y0,x1,y1=90,500,BW-90,1700
    d.rounded_rectangle([x0-40,y0-40,x1+40,y1+40],50,fill=(32,32,30))
    s=Image.new('L',(x1-x0,y1-y0),40); sd=ImageDraw.Draw(s); sw,sh=s.size
    sd.rectangle([0,sh*0.62,sw,sh],fill=55); sd.rectangle([0,sh*0.55,sw,sh*0.62],fill=80)
    sd.rectangle([sw*0.05,sh*0.1,sw*0.95,sh*0.3],fill=58)
    px=sw*0.45; sd.ellipse([px-45,sh*0.33,px+45,sh*0.41],fill=18); sd.rectangle([px-70,sh*0.41,px+70,sh*0.56],fill=18)
    if man:
        sc=1.0 if man==1 else 1.25; mx=px+170*sc
        sd.ellipse([mx-50*sc,sh*0.14,mx+50*sc,sh*0.14+110*sc],fill=10)
        sd.rectangle([mx-80*sc,sh*0.14+105*sc,mx+80*sc,sh*0.56],fill=12)
        sd.arc([mx-28*sc,sh*0.14+50*sc,mx+28*sc,sh*0.14+85*sc],20,160,fill=150,width=4)
    for y in range(0,sh,6): sd.line([0,y,sw,y],fill=0)
    s=s.filter(ImageFilter.GaussianBlur(1.6))
    tint=Image.merge('RGB',(s.point(lambda v:v*0.8),s,s.point(lambda v:v*0.85)))
    im.paste(tint,(x0,y0)); d=ImageDraw.Draw(im)
    d.text((x0+40,y0+30),'CAM 02',font=F(M,48),fill=(220,230,220)); d.text((x1-380,y0+30),'03:00:17',font=F(M,48),fill=(220,230,220))
    d.ellipse([x0+40,y0+110,x0+80,y0+150],fill=(220,30,30)); d.text((x0+100,y0+102),'REC',font=F(M,48),fill=(220,230,220))
    return im
def dark(red=False):
    im=base((2,2,3),(6,5,6)) if not red else base((18,0,0),(4,0,0))
    return glow(im,(cx,BH//2),300,(40,40,50) if not red else (90,0,0),0.4)
def title():
    im=dark(); d=ImageDraw.Draw(im)
    f=F(B,300); d.text((cx,820),'3:00',font=f,fill=(225,40,30),anchor='mm')
    d.text((cx,1020),'AM',font=F(B,120),fill=(235,230,220),anchor='mm')
    return im
def building():
    im=base((4,6,14),(8,8,14)); d=ImageDraw.Draw(im)
    d.rectangle([260,500,950,BH],fill=(22,22,26))
    for r in range(11):
        for c in range(5):
            x=310+c*125; y=560+r*130
            lit=(r==2 and c==3)
            d.rectangle([x,y,x+70,y+85],fill=(170,150,90) if lit else (32,32,38))
    im=glow(im,(690,860),160,(180,150,80),0.5)
    return im
def elevator(num):
    im=base((22,20,16),(14,12,10)); d=ImageDraw.Draw(im)
    d.rectangle([140,350,BW-140,BH-200],fill=(48,46,42))
    d.rectangle([200,560,BW//2-6,BH-200],fill=(70,68,64)); d.rectangle([BW//2+6,560,BW-200,BH-200],fill=(70,68,64))
    d.rounded_rectangle([cx-170,400,cx+170,520],16,fill=(10,10,10))
    col=(230,60,40) if num==13 else (240,170,60)
    d.text((cx,460),str(num),font=F(M,96),fill=col,anchor='mm')
    im=glow(im,(cx,460),150,col,0.35 if num==13 else 0.2)
    return im
def hall(woman=False):
    im=base((5,6,8),(8,8,10)); d=ImageDraw.Draw(im)
    vx,vy=cx,1050
    d.polygon([(0,300),(vx-70,vy-120),(vx-70,vy+120),(0,BH)],fill=(18,18,20))
    d.polygon([(BW,300),(vx+70,vy-120),(vx+70,vy+120),(BW,BH)],fill=(16,16,18))
    d.polygon([(0,BH),(vx-70,vy+120),(vx+70,vy+120),(BW,BH)],fill=(24,22,20))
    d.rectangle([vx-70,vy-120,vx+70,vy+120],fill=(30,30,32))
    for k in range(4):
        y=300+k*180; d.line([0+k*120,y+k*20,0+k*120,y+400-k*60],fill=(28,28,30),width=8)
    im=glow(im,(vx,vy-200),120,(90,95,90),0.35); d=ImageDraw.Draw(im)
    if woman:
        d.ellipse([vx-16,vy-95,vx+16,vy-60],fill=(6,6,6)); d.polygon([(vx-26,vy-60),(vx+26,vy-60),(vx+34,vy+118),(vx-34,vy+118)],fill=(6,6,6))
        d.polygon([(vx-18,vy-85),(vx+18,vy-85),(vx+22,vy-20),(vx-22,vy-20)],fill=(4,4,4))
    return im
def room():
    im=base((10,10,14),(14,12,12)); d=ImageDraw.Draw(im)
    d.rectangle([0,1350,BW,BH],fill=(24,20,18))
    d.rectangle([80,300,520,700],fill=(18,22,30)); d.line([300,300,300,700],fill=(10,10,12),width=10); d.line([80,500,520,500],fill=(10,10,12),width=10)
    d.rounded_rectangle([90,1150,560,1420],30,fill=(30,26,26)); d.rounded_rectangle([70,1080,170,1420],30,fill=(34,30,30))
    x=840; d.ellipse([x-60,700,x+60,840],fill=(5,5,5)); d.polygon([(x-90,840),(x+90,840),(x+130,1480),(x-130,1480)],fill=(5,5,5))
    d.polygon([(x-70,740),(x+70,740),(x+85,1000),(x-85,1000)],fill=(3,3,3))
    im=glow(im,(300,500),220,(60,70,95),0.3)
    return im
# Scene library. Add new scene functions above and register them here.
SC={'title':title,'outside':outside,'phone':phone,'phone_red':lambda:phone(True),'cam_empty':lambda:cam(0),'cam_man':lambda:cam(1),'cam_man_close':lambda:cam(2),'dark':dark,'dark_red':lambda:dark(True),
    'building':building,'elev9':lambda:elevator(9),'elev13':lambda:elevator(13),'hall':lambda:hall(False),'hall_woman':lambda:hall(True),'room_woman':room}
def caption(text):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); f=F(B,70)
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>900 and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); y=1660-len(lines)*45
    for ln in lines:
        d.text((W//2,y),ln,font=f,fill=(255,255,255),anchor='mm',stroke_width=8,stroke_fill=(0,0,0)); y+=92
    return lay
def endcard():
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((W//2,1640),'FOLLOW FOR A NEW',font=F(B,70),fill=(255,255,255),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    d.text((W//2,1735),'STORY EVERY DAY',font=F(B,70),fill=(225,40,30),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    return lay
