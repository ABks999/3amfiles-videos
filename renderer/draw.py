# ===================== SCENE STYLE GUIDE (read before adding scenes) =====================
# Hamza finds simple scenes boring. Every NEW scene must be a rich, cinematic illustration:
# - 3 depth layers: far background (sky/wall with texture, moon, windows, stars, distant shapes),
#   midground (the main object/room, drawn with several parts, edges, highlights and shadows),
#   foreground (dark silhouettes framing the shot: door frame, branches, furniture edge, car pillar).
# - at least 8-12 distinct drawn elements, not one big rectangle. Add small details: cracks, picture
#   frames, wires, leaves, light switches, curtains, reflections, handprints, etc.
# - 1-2 strong coloured light sources (lamp, screen, moon, streetlight, candle) using glow(), with
#   light falling on nearby surfaces (lighter polygons) and long dark shadows.
# - one accent colour per scene (sickly green, blood red, cold cyan, amber) on a dark blue/black base.
# - figures: silhouettes with a clear readable pose (tilted head, long arms, too-tall body),
#   glowing eyes only when the creepy reveal happens.
# - render.py adds colour grade, bloom, fog, dust, camera motion and effects on top automatically.
# - keep the top ~260 px and y 1500-1800 (captions) free of the main subject.
# ==========================================================================================
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
def cabin():
    im=base((4,8,20),(14,16,24)); d=ImageDraw.Draw(im)
    for i in range(120):
        x=(i*97)%BW; y=(i*53)%1100; d.ellipse([x,y,x+5,y+5],fill=(170,175,190))
    d.rectangle([0,1450,BW,BH],fill=(150,155,170))
    for x in (40,170,1000,1120):
        d.polygon([(x,620),(x-130,1500),(x+130,1500)],fill=(8,12,14))
    d.rectangle([330,1000,880,1470],fill=(26,20,18))
    d.polygon([(280,1010),(cx-0,700),(930,1010)],fill=(18,14,14))
    d.polygon([(260,1020),(cx,690),(950,1020),(930,1000),(cx,725),(280,1000)],fill=(200,205,220))
    d.rectangle([420,1160,560,1300],fill=(190,140,60)); d.line([490,1160,490,1300],fill=(40,28,20),width=8); d.line([420,1230,560,1230],fill=(40,28,20),width=8)
    d.rectangle([660,1180,780,1470],fill=(36,26,22))
    im=glow(im,(490,1230),170,(200,140,60),0.45)
    return im
def door():
    im=base((14,10,8),(20,14,10)); d=ImageDraw.Draw(im)
    d.rectangle([0,1600,BW,BH],fill=(26,18,14))
    d.rectangle([300,420,910,1600],fill=(44,30,22))
    for x in (330,600): d.rectangle([x,460,x+250,980],outline=(30,20,14),width=10); d.rectangle([x,1040,x+250,1560],outline=(30,20,14),width=10)
    d.ellipse([820,1020,860,1060],fill=(120,100,60))
    d.rectangle([300,1590,910,1606],fill=(140,170,220))
    im=glow(im,(cx,1600),260,(70,100,160),0.45)
    return im
def prints():
    im=base((10,14,26),(120,126,142)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,700],fill=(6,8,14))
    d.rectangle([380,420,830,720],fill=(22,16,14)); d.polygon([(340,430),(cx,260),(870,430)],fill=(190,195,210))
    d.rectangle([560,560,650,720],fill=(30,22,18))
    d.polygon([(0,700),(BW,700),(BW,BH),(0,BH)],fill=(132,138,156))
    for k in range(12):
        t=k/11; y=BH-120-t*(BH-120-760); s=1-0.8*t
        off=(1 if k%2 else -1)*60*s; x=cx+off
        d.ellipse([x-26*s,y-50*s,x+26*s,y+50*s],fill=(70,76,96))
    im=glow(im,(605,640),120,(150,160,200),0.25)
    return im
def closet(open_=False):
    im=base((6,8,14),(12,12,16)); d=ImageDraw.Draw(im)
    d.rectangle([0,1400,BW,BH],fill=(20,18,18))
    d.rectangle([520,380,1060,1420],fill=(34,30,28))
    if open_:
        d.rectangle([700,410,880,1410],fill=(2,2,3))
        x=790; d.ellipse([x-40,640,x+40,740],fill=(10,10,12)); d.polygon([(x-60,740),(x+60,740),(x+80,1400),(x-80,1400)],fill=(10,10,12))
        d.ellipse([x-22,680,x-10,690],fill=(190,190,170)); d.ellipse([x+10,680,x+22,690],fill=(190,190,170))
        d.polygon([(880,410),(1040,380),(1040,1440),(880,1410)],fill=(44,38,34))
    else:
        d.line([790,400,790,1410],fill=(14,12,12),width=8)
        d.rectangle([700,410,710,1410],fill=(8,8,8))
    d.ellipse([760,880,775,895],fill=(110,95,60)); d.ellipse([805,880,820,895],fill=(110,95,60))
    d.rounded_rectangle([60,1150,600,1520],30,fill=(40,34,40)); d.rounded_rectangle([40,1000,140,1520],30,fill=(46,40,44))
    d.rounded_rectangle([170,1110,380,1200],30,fill=(150,150,165))
    im=glow(im,(260,700),240,(50,70,110),0.3)
    return im
def road():
    im=base((3,5,12),(8,8,12)); d=ImageDraw.Draw(im)
    vx,vy=cx,880
    d.rectangle([0,vy,BW,BH],fill=(10,12,10))
    for x in range(-40,BW+80,90):
        h=260+(x*37)%220; d.polygon([(x,vy-h),(x-70,vy+10),(x+70,vy+10)],fill=(4,7,6))
    d.polygon([(vx-30,vy),(vx+30,vy),(BW+200,BH),(-200,BH)],fill=(28,28,30))
    for k in range(7):
        t=k/6; y0=vy+20+(BH-vy)*t**1.7; y1=y0+30+120*t**1.5; w=3+14*t
        d.polygon([(vx-w/2,y0),(vx+w/2,y0),(vx+w,y1),(vx-w,y1)],fill=(200,180,90))
    im=glow(im,(vx,1500),520,(150,140,110),0.35)
    d=ImageDraw.Draw(im); d.polygon([(0,1650),(BW,1650),(BW,BH),(0,BH)],fill=(6,6,7))
    d.arc([cx-520,1560,cx+520,2500],200,340,fill=(14,14,16),width=60)
    return im
def gps(red=False):
    im=base((4,4,8),(10,9,10)); d=ImageDraw.Draw(im)
    d.polygon([(0,520),(BW,520),(BW,380),(0,380)],fill=(6,8,14))
    d.rectangle([0,1050,BW,BH],fill=(16,15,16))
    d.rounded_rectangle([230,600,980,1100],40,fill=(20,20,22))
    sc=(150,20,15) if red else (20,70,110)
    d.rounded_rectangle([270,640,940,1060],24,fill=sc)
    lc=(255,120,100) if red else (120,210,255)
    d.line([605,1020,605,860,470,760],fill=lc,width=44,joint='curve')
    d.polygon([(470,700),(430,800),(530,790)],fill=lc)
    d.ellipse([585,990,625,1030],fill=(255,255,255))
    im=glow(im,(605,850),330,sc,0.7); d=ImageDraw.Draw(im)
    d.arc([cx-560,1250,cx+560,2350],180,360,fill=(8,8,9),width=90)
    d.rectangle([cx-70,1300,cx+70,1700],fill=(8,8,9))
    return im
def mirror(eyes=False):
    im=base((6,6,10),(12,10,12)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,330],fill=(10,10,14)); d.rectangle([cx-20,330,cx+20,560],fill=(16,16,18))
    d.rounded_rectangle([110,540,1100,1120],90,fill=(24,24,26))
    d.rounded_rectangle([150,580,1060,1080],70,fill=(14,16,22))
    d.rounded_rectangle([200,860,1010,1080],40,fill=(30,26,28))
    d.rectangle([260,700,380,880],fill=(24,22,24)); d.rectangle([830,700,950,880],fill=(24,22,24))
    d.rectangle([150,620,1060,700],fill=(26,30,42))
    if eyes:
        x=cx; d.ellipse([x-80,640,x+80,820],fill=(3,3,4)); d.polygon([(x-150,800),(x+150,800),(x+200,1080),(x-200,1080)],fill=(3,3,4))
        d.ellipse([x-46,712,x-22,726],fill=(230,220,200)); d.ellipse([x+22,712,x+46,726],fill=(230,220,200))
    im=glow(im,(cx,660),300,(60,70,100),0.3)
    d=ImageDraw.Draw(im); d.rectangle([0,1250,BW,BH],fill=(14,12,12))
    return im
# Scene library. Add new scene functions above and register them here.
SC={'title':title,'outside':outside,'phone':phone,'phone_red':lambda:phone(True),'cam_empty':lambda:cam(0),'cam_man':lambda:cam(1),'cam_man_close':lambda:cam(2),'dark':dark,'dark_red':lambda:dark(True),
    'building':building,'elev9':lambda:elevator(9),'elev13':lambda:elevator(13),'hall':lambda:hall(False),'hall_woman':lambda:hall(True),'room_woman':room,
    'cabin':cabin,'door':door,'prints':prints,'closet':lambda:closet(False),'closet_woman':lambda:closet(True),
    'road':road,'gps':gps,'gps_red':lambda:gps(True),'mirror':mirror,'mirror_eyes':lambda:mirror(True)}
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
