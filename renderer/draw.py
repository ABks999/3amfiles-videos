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
# - helpers ready to use: noise_tex(), cone() light beams, vgrad(), moon(), stars(), pine(), figure() creepy silhouette.
# - render.py adds colour grade, bloom, fog, dust, camera motion and effects on top automatically.
# - keep the top ~260 px and y 1500-1800 (captions) free of the main subject.
# ==========================================================================================
import sys, json, random, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from story import LINES, CAPTIONS
W,H=1080,1920; BW,BH=int(W*1.12),int(H*1.12)
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
M='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
SERIFD='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def F(p,s): return ImageFont.truetype(p,s)
def base(c1,c2):
    g=np.linspace(0,1,BH)[:,None,None]; a=np.array(c1)*(1-g)+np.array(c2)*g
    return Image.fromarray(np.repeat(a,BW,1).astype('uint8'))
def glow(img,xy,r,col,alpha=0.6):
    l=Image.new('RGB',img.size,(0,0,0)); d=ImageDraw.Draw(l); x,y=xy
    d.ellipse([x-r,y-r,x+r,y+r],fill=col); l=l.filter(ImageFilter.GaussianBlur(r/2))
    return Image.fromarray(np.clip(np.array(img,float)+np.array(l,float)*alpha,0,255).astype('uint8'))
cx=BW//2
# ---------- drawing helpers ----------
_R=np.random.default_rng(11)
def noise_tex(im,amt=10,scale=3):
    n=_R.normal(0,1,(BH//scale,BW//scale)).astype(np.float32)
    n=np.asarray(Image.fromarray(((n*40)+128).clip(0,255).astype(np.uint8)).resize((BW,BH),Image.BICUBIC),dtype=np.float32)-128
    return Image.fromarray(np.clip(np.asarray(im,dtype=np.float32)+n[...,None]*amt/40,0,255).astype(np.uint8))
def cone(im,apex,p1,p2,col,alpha=0.35,blur=40):
    l=Image.new('RGB',im.size,(0,0,0)); ImageDraw.Draw(l).polygon([apex,p1,p2],fill=col)
    l=l.filter(ImageFilter.GaussianBlur(blur))
    return Image.fromarray(np.clip(np.asarray(im,float)+np.asarray(l,float)*alpha,0,255).astype('uint8'))
def vgrad(d,box,c1,c2,steps=40):
    x0,y0,x1,y1=box
    for i in range(steps):
        t=i/(steps-1); c=tuple(int(c1[k]*(1-t)+c2[k]*t) for k in range(3))
        d.rectangle([x0,y0+(y1-y0)*i/steps,x1,y0+(y1-y0)*(i+1)/steps+1],fill=c)
def moon(im,x,y,r=70,col=(215,220,235)):
    im=glow(im,(x,y),r*3,(60,75,110),0.5); d=ImageDraw.Draw(im)
    d.ellipse([x-r,y-r,x+r,y+r],fill=col)
    for (dx,dy,rr) in ((-20,-15,14),(25,10,10),(-5,30,8)): d.ellipse([x+dx-rr,y+dy-rr,x+dx+rr,y+dy+rr],fill=tuple(c-25 for c in col))
    return im
def stars(d,n=90,ymax=900,seed=1):
    r=np.random.default_rng(seed)
    for _ in range(n):
        x,y=r.random()*BW,r.random()*ymax; s=r.random()*2.2+0.6; v=int(120+r.random()*110)
        d.ellipse([x-s,y-s,x+s,y+s],fill=(v,v,min(255,v+20)))
def pine(d,x,base_y,h,w,col):
    for k in range(5):
        t=k/5; yy=base_y-h*t; ww=w*(1-t*0.8)
        d.polygon([(x,yy-h*0.32),(x-ww,yy),(x+ww,yy)],fill=col)
    d.rectangle([x-w*0.06,base_y-10,x+w*0.06,base_y+30],fill=col)
def figure(d,x,y,h,col=(4,4,6),tilt=0,eyes=None,long_arms=True):
    """thin, too-tall silhouette. (x,y)=feet centre, h=height."""
    hw=h*0.11; head=h*0.09
    hx=x+tilt*head; hy=y-h+head
    d.ellipse([hx-head*0.8,hy-head,hx+head*0.8,hy+head],fill=col)
    d.polygon([(x-hw*0.6,y-h+head*1.8),(x+hw*0.6,y-h+head*1.8),(x+hw,y-h*0.45),(x+hw*0.7,y),(x-hw*0.7,y),(x-hw,y-h*0.45)],fill=col)
    arm=h*(0.55 if long_arms else 0.4)
    for s in (-1,1):
        d.polygon([(x+s*hw*0.6,y-h+head*2),(x+s*hw*1.05,y-h+head*2.2),(x+s*hw*1.25,y-h+head*2+arm),(x+s*hw*0.95,y-h+head*2+arm)],fill=col)
        for f in range(3): d.line([x+s*hw*1.1,y-h+head*2+arm,x+s*hw*(1.0+0.15*f),y-h+head*2+arm+h*0.04],fill=col,width=4)
    if eyes:
        e=head*0.18
        for s in (-1,1): d.ellipse([hx+s*head*0.35-e,hy-e*0.6,hx+s*head*0.35+e,hy+e*0.6],fill=eyes)

# ---------- scenes ----------
def outside():  # gas station at night
    im=base((5,8,20),(12,12,22)); d=ImageDraw.Draw(im); stars(d,70,700,3)
    for x,h in ((0,520),(140,380),(990,460),(1110,600)): pine(d,x+40,1260,h,140,(6,10,12))
    d.rectangle([0,1260,BW,BH],fill=(16,16,19)); vgrad(d,(0,1260,BW,1500),(22,22,26),(14,14,16))
    for k in range(9): d.line([k*160-200,BH,cx+(k-4)*40,1300],fill=(24,24,27),width=4)
    d.rectangle([140,860,1070,940],fill=(36,36,40)); d.rectangle([140,935,1070,950],fill=(240,225,170))
    d.text((cx,900),'OPEN 24H',font=F(B,46),fill=(200,40,30),anchor='mm')
    for x in (300,605,910): d.rectangle([x-16,950,x+16,1300],fill=(28,28,32))
    for x in (450,760):
        d.rounded_rectangle([x-55,1110,x+55,1300],10,fill=(34,34,38)); d.rectangle([x-38,1135,x+38,1190],fill=(80,140,110))
        d.line([x+55,1160,x+85,1160,x+85,1250],fill=(20,20,22),width=8)
    d.rectangle([880,1020,1180,1300],fill=(30,28,26)); d.rectangle([905,1050,1155,1290],fill=(120,112,76))
    for y in (1100,1160,1220): d.line([905,y,1155,y],fill=(110,100,70),width=8)
    d.rectangle([1080,1130,1110,1290],fill=(20,18,16))  # someone standing inside
    d.ellipse([1083,1100,1107,1132],fill=(20,18,16))
    im=glow(im,(605,960),300,(170,150,90),0.3); im=glow(im,(1030,1160),180,(170,160,100),0.25)
    im=cone(im,(605,950),(250,1400),(960,1400),(200,185,130),0.15,50)
    d=ImageDraw.Draw(im); d.polygon([(0,BH),(0,1700),(180,1620),(260,BH)],fill=(5,5,6))  # foreground car edge
    return noise_tex(im,8)
def phone(red=False):  # smartphone ringing on a nightstand
    bg1,bg2=((8,10,18),(16,12,12)) if not red else ((24,3,3),(10,0,0))
    im=base(bg1,bg2); d=ImageDraw.Draw(im)
    d.rectangle([60,330,520,820],fill=(14,18,30) if not red else (30,8,8))  # window
    d.line([290,330,290,820],fill=(6,6,8),width=12); d.line([60,575,520,575],fill=(6,6,8),width=12)
    for x in (40,540): d.polygon([(x-20,300),(x+40,300),(x+60,1000),(x-30,1000)],fill=(10,8,10))  # curtains
    vgrad(d,(0,1180,BW,BH),(40,28,22) if not red else (40,8,8),(16,12,10) if not red else (12,2,2))
    d.polygon([(0,1180),(BW,1180),(BW,1215),(0,1215)],fill=(58,42,32) if not red else (60,12,12))
    d.rounded_rectangle([780,860,900,1180],10,fill=(30,26,24)); d.polygon([(700,860),(980,860),(930,720),(750,720)],fill=(60,50,40))  # lamp (off)
    d.rounded_rectangle([90,1090,300,1180],12,fill=(26,24,26)); d.text((195,1135),'3:07',font=F(M,60),fill=(220,40,30),anchor='mm')  # clock
    px,py=cx,1290
    d.polygon([(px-190,py-40),(px+190,py-40),(px+230,py+70),(px-230,py+70)],fill=(12,12,14))
    scr=(30,120,90) if not red else (200,30,25)
    d.polygon([(px-165,py-30),(px+165,py-30),(px+200,py+60),(px-200,py+60)],fill=scr)
    im=glow(im,(px,py),330,scr,0.75); d=ImageDraw.Draw(im)
    d.text((px,py+5),'UNKNOWN' if not red else 'NO CALLER ID',font=F(B,42),fill=(240,255,245),anchor='mm')
    col=(150,240,200) if not red else (255,90,70)
    for r in (230,320,410): d.arc([px-r,py-r*0.75,px+r,py+r*0.55],205,335,fill=col,width=9)
    im=cone(im,(290,575),(500,1180),(900,1180),(70,90,140) if not red else (120,20,20),0.18,40)
    return noise_tex(im,8)
def cam(man=0):  # CCTV monitor showing a store aisle
    im=base((6,6,8),(12,11,10)); d=ImageDraw.Draw(im)
    d.rectangle([0,1700,BW,BH],fill=(22,18,14)); d.rectangle([0,1690,BW,1712],fill=(44,34,26))
    x0,y0,x1,y1=90,480,BW-90,1560
    d.rounded_rectangle([x0-50,y0-50,x1+50,y1+60],40,fill=(30,30,30)); d.rounded_rectangle([x0-30,y0-30,x1+30,y1+30],30,fill=(10,10,10))
    d.ellipse([cx-10,y1+30,cx+10,y1+50],fill=(40,200,60))
    s=Image.new('L',(x1-x0,y1-y0),30); sd=ImageDraw.Draw(s); sw,sh=s.size
    vx,vy=sw*0.5,sh*0.42
    sd.polygon([(0,sh),(vx-60,vy+60),(vx+60,vy+60),(sw,sh)],fill=60)  # floor
    sd.polygon([(0,0),(vx-60,vy-80),(vx-60,vy+60),(0,sh)],fill=42); sd.polygon([(sw,0),(vx+60,vy-80),(vx+60,vy+60),(sw,sh)],fill=40)
    for k in range(6):  # shelves
        t=k/6; xl=vx-60-(vx-60)*(1-t)**1.6; xr=sw-(xl)
        for yy in (0.25,0.45,0.65):
            sd.line([xl,vy-80+(sh*yy)*(1-t),xl+20,vy-80+(sh*yy)*(1-t)],fill=80,width=3)
        sd.line([xl,vy-80*(t)-sh*0.1*(1-t),xl,sh*(1-0.4*t)],fill=25,width=6); sd.line([xr,vy-80*(t)-sh*0.1*(1-t),xr,sh*(1-0.4*t)],fill=25,width=6)
    for k in range(4): sd.rectangle([vx-200+k*120,20,vx-140+k*120,40],fill=140)  # ceiling lights
    if man:
        sc=1.0 if man==1 else 1.7; mx=vx+30; base_y=vy+60+sh*0.12*sc
        hgt=sh*0.36*sc; sd.ellipse([mx-hgt*0.07,base_y-hgt,mx+hgt*0.07,base_y-hgt+hgt*0.16],fill=8)
        sd.polygon([(mx-hgt*0.12,base_y-hgt*0.84),(mx+hgt*0.12,base_y-hgt*0.84),(mx+hgt*0.1,base_y),(mx-hgt*0.1,base_y)],fill=8)
        sd.ellipse([mx-hgt*0.035,base_y-hgt*0.93,mx-hgt*0.015,base_y-hgt*0.91],fill=200); sd.ellipse([mx+hgt*0.015,base_y-hgt*0.93,mx+hgt*0.035,base_y-hgt*0.91],fill=200)
        sd.arc([mx-hgt*0.04,base_y-hgt*0.9,mx+hgt*0.04,base_y-hgt*0.87],10,170,fill=170,width=3)
    for y in range(0,sh,5): sd.line([0,y,sw,y],fill=0)
    s=s.filter(ImageFilter.GaussianBlur(1.4))
    tint=Image.merge('RGB',(s.point(lambda v:v*0.75),s,s.point(lambda v:v*0.8)))
    im.paste(tint,(x0,y0)); im=glow(im,(cx,(y0+y1)//2),520,(40,70,50),0.35); d=ImageDraw.Draw(im)
    d.text((x0+40,y0+30),'CAM 02',font=F(M,48),fill=(220,230,220)); d.text((x1-380,y0+30),'03:00:17',font=F(M,48),fill=(220,230,220))
    d.ellipse([x0+40,y0+110,x0+80,y0+150],fill=(220,30,30)); d.text((x0+100,y0+102),'REC',font=F(M,48),fill=(220,230,220))
    d.rounded_rectangle([140,1740,420,1800],8,fill=(30,30,32)); d.ellipse([900,1720,1010,1790],fill=(40,30,24))  # keyboard, mug
    return noise_tex(im,7)
def dark(red=False):  # near-black room, faint shapes
    im=base((3,3,6),(8,7,9)) if not red else base((22,0,0),(5,0,0)); d=ImageDraw.Draw(im)
    c=(10,10,13) if not red else (32,4,4)
    d.rectangle([140,520,470,1000],fill=c); d.line([305,520,305,1000],fill=(4,4,5),width=10)  # faint window
    d.polygon([(700,1650),(1150,1650),(1209,BH),(640,BH)],fill=(12,11,13) if not red else (28,2,2))
    d.rectangle([0,1640,BW,1660],fill=(14,13,15) if not red else (34,4,4))
    im=glow(im,(cx,BH//2),340,(40,42,60) if not red else (110,0,0),0.45)
    im=cone(im,(305,700),(160,1700),(700,1700),(40,50,80) if not red else (90,10,10),0.12,60)
    if red:
        d=ImageDraw.Draw(im)
        for k in range(14): x=_R.random()*BW; d.line([x,320,x+_R.normal(0,6),320+_R.random()*200],fill=(70,0,0),width=3)  # drips
    return noise_tex(im,9)
def title():
    im=dark(); d=ImageDraw.Draw(im)
    f=F(B,300); d.text((cx,820),'3:00',font=f,fill=(225,40,30),anchor='mm')
    d.text((cx,1020),'AM',font=F(B,120),fill=(235,230,220),anchor='mm')
    return im
def building():  # apartment block, one lit window
    im=base((6,10,26),(14,14,24)); d=ImageDraw.Draw(im); stars(d,80,600,5)
    im=moon(im,960,420,65); d=ImageDraw.Draw(im)
    for x,w,h in ((-20,200,900),(1000,260,1050)): d.rectangle([x,BH-h,x+w,BH],fill=(10,12,18))
    d.rectangle([250,520,960,BH],fill=(24,24,30)); d.rectangle([230,500,980,540],fill=(34,34,40))
    for r in range(11):
        for c in range(5):
            x=300+c*130; y=580+r*125; lit=(r==2 and c==3); dim=((r*7+c*3)%9==0)
            d.rectangle([x-6,y-6,x+76,y+96],fill=(30,30,36))
            d.rectangle([x,y,x+70,y+90],fill=(200,170,90) if lit else ((60,55,40) if dim else (16,18,24)))
            d.line([x+35,y,x+35,y+90],fill=(28,28,32),width=4)
            if lit: d.rectangle([x+44,y+20,x+60,y+90],fill=(30,22,16)); d.ellipse([x+44,y+4,x+60,y+22],fill=(30,22,16))
            if r%3==0: d.rectangle([x-10,y+96,x+80,y+104],fill=(38,38,44))
    for x in (120,1100):
        d.rectangle([x-6,1300,x+6,1900],fill=(18,18,22)); d.line([x,1300,x+(60 if x<600 else -60),1290],fill=(18,18,22),width=8)
        im=glow(im,(x+(60 if x<600 else -60),1300),140,(200,160,80),0.4); d=ImageDraw.Draw(im)
    im=glow(im,(725,885),170,(200,160,80),0.6)
    d=ImageDraw.Draw(im); d.rectangle([0,1900,BW,BH],fill=(10,10,12))
    pine(d,60,1950,600,170,(4,6,6)); pine(d,1170,1980,520,150,(4,6,6))
    return noise_tex(im,8)
def elevator(num):
    im=base((16,15,12),(8,7,6)); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(BW,0),(BW-150,330),(150,330)],fill=(14,13,11))  # ceiling
    for k in range(3): d.rectangle([cx-260+k*190,140,cx-130+k*190,200],fill=(230,220,180))
    d.polygon([(0,0),(150,330),(150,BH-220),(0,BH)],fill=(26,25,22)); d.polygon([(BW,0),(BW-150,330),(BW-150,BH-220),(BW,BH)],fill=(23,22,20))
    d.rectangle([150,330,BW-150,BH-220],fill=(34,33,30))
    d.rectangle([200,560,cx-6,BH-220],fill=(50,49,46)); d.rectangle([cx+6,560,BW-200,BH-220],fill=(47,46,43))
    for x in (260,cx+70): d.line([x,600,x+180,BH-300],fill=(64,63,60),width=3)  # brushed metal reflections
    d.polygon([(0,BH),(150,BH-220),(BW-150,BH-220),(BW,BH)],fill=(30,26,22))
    for k in range(6): d.line([150+k*(BW-300)/5,BH-220,k*BW/5,BH],fill=(40,36,30),width=3)
    d.rectangle([60,600,110,1500],fill=(70,68,62)); d.rectangle([66,620,104,1480],fill=(52,50,46))  # panel
    for k in range(10): d.ellipse([72,650+k*80,98,676+k*80],fill=(200,160,60) if k==(2 if num==13 else 4) else (90,88,80))
    d.rounded_rectangle([cx-170,380,cx+170,510],16,fill=(8,8,8))
    col=(230,60,40) if num==13 else (240,170,60)
    d.text((cx,445),str(num),font=F(M,96),fill=col,anchor='mm')
    d.polygon([(cx+120,420),(cx+150,470),(cx+90,470)] if num!=13 else [(cx+120,470),(cx+150,420),(cx+90,420)],fill=col)
    im=glow(im,(cx,445),160,col,0.35 if num==13 else 0.22); im=glow(im,(cx,170),260,(200,180,130),0.2)
    if num==13:
        d=ImageDraw.Draw(im)
        for k in range(5): d.line([cx-8+k*4,560,cx-10+k*5,700+k*30],fill=(20,18,16),width=3)  # fingers in the door gap
    return noise_tex(im,7)
def hall(woman=False):
    im=base((6,7,9),(10,9,10)); d=ImageDraw.Draw(im)
    vx,vy=cx,1050
    d.polygon([(0,300),(vx-80,vy-140),(vx-80,vy+130),(0,BH)],fill=(30,28,26))
    d.polygon([(BW,300),(vx+80,vy-140),(vx+80,vy+130),(BW,BH)],fill=(26,24,23))
    d.polygon([(0,300),(BW,300),(vx+80,vy-140),(vx-80,vy-140)],fill=(18,17,16))
    d.polygon([(0,BH),(vx-80,vy+130),(vx+80,vy+130),(BW,BH)],fill=(44,20,18))  # red carpet
    for k in range(10):
        t=(k/10)**1.8; y=vy+130+(BH-vy-130)*t; w=80+(cx-80)*t
        d.line([vx-w,y,vx+w,y],fill=(56,28,24),width=max(2,int(10*t)))
    d.rectangle([vx-80,vy-140,vx+80,vy+130],fill=(14,14,15))
    for s in (-1,1):  # doors on both walls
        for k in range(3):
            t=0.15+k*0.25; x=vx+s*(80+(cx-80)*(1-t)**1.3)*(1 if s>0 else 1)
            xa=vx+s*80+s*(cx-80)*(1-t)**1.6; xb=vx+s*80+s*(cx-80)*(1-(t+0.12))**1.6
            ya0=300+(vy-140-300)*(1-(1-t)**1.6); ya1=BH-(BH-vy-130)*(1-(1-t)**1.6)*1.0
            d.polygon([(xa,ya0+ (ya1-ya0)*0.15),(xb,ya0+(ya1-ya0)*0.22),(xb,ya1-(ya1-ya0)*0.1),(xa,ya1-(ya1-ya0)*0.02)],fill=(52,38,30))
    for k in range(4):  # ceiling lights, the far one flickering off
        t=k/4; y=300+(vy-140-300)*(t**0.7); w=60*(1-t)+12
        d.rectangle([vx-w,y+10,vx+w,y+10+16*(1-t)+4],fill=(220,225,210) if k!=2 else (60,60,58))
        im=glow(im,(vx,y+40),int(170*(1-t)+40),(140,150,130),0.35 if k!=2 else 0.05); d=ImageDraw.Draw(im)
    if woman: figure(d,vx,vy+128,260,(5,5,6),tilt=0.4)
    d.polygon([(0,0),(140,0),(140,BH),(0,BH)],fill=(8,8,9)); d.polygon([(BW,0),(BW-110,0),(BW-110,BH),(BW,BH)],fill=(7,7,8))  # door frame foreground
    return noise_tex(im,8)
def room():  # living room, woman standing in the corner
    im=base((10,12,18),(14,12,12)); d=ImageDraw.Draw(im)
    d.rectangle([0,1350,BW,BH],fill=(30,24,20)); d.rectangle([0,1340,BW,1360],fill=(46,36,30))
    for k in range(12): d.line([k*110,1360,k*110-150,BH],fill=(36,28,24),width=3)
    d.rectangle([70,300,540,760],fill=(20,30,48)); im=moon(im,420,420,40); d=ImageDraw.Draw(im)
    d.line([305,300,305,760],fill=(8,8,10),width=12); d.line([70,530,540,530],fill=(8,8,10),width=12)
    for x in (40,560): d.polygon([(x-30,260),(x+40,260),(x+55,1100),(x-40,1100)],fill=(22,16,20))
    d.rectangle([640,380,880,560],fill=(40,34,28)); d.rectangle([660,400,860,540],fill=(60,58,54))  # picture frame
    d.ellipse([720,430,800,510],fill=(30,28,26))
    d.rounded_rectangle([60,1130,600,1420],34,fill=(44,36,40)); d.rounded_rectangle([40,1040,170,1430],30,fill=(50,42,46)); d.rounded_rectangle([490,1040,620,1430],30,fill=(50,42,46))
    d.rounded_rectangle([120,1060,290,1160],26,fill=(70,60,66))
    d.line([620,1420,700,980],fill=(30,26,24),width=8); d.polygon([(640,980),(760,980),(730,880),(670,880)],fill=(80,64,44))  # lamp (off)
    im=cone(im,(305,530),(200,1700),(760,1700),(70,90,140),0.22,50); d=ImageDraw.Draw(im)
    figure(d,950,1480,820,(4,4,5),tilt=0.6)
    d.ellipse([1080,330,1209,470],fill=(0,0,0))  # dark corner
    return noise_tex(im,8)
def cabin():
    im=base((6,10,26),(16,18,30)); d=ImageDraw.Draw(im); stars(d,140,1000,7)
    im=moon(im,900,420,75); d=ImageDraw.Draw(im)
    for x,h in ((60,800),(200,620),(330,480),(880,520),(1010,700),(1140,880)): pine(d,x,1470,h,150,(8,12,16))
    d.rectangle([0,1450,BW,BH],fill=(92,98,120)); vgrad(d,(0,1450,BW,1560),(70,76,98),(96,102,124))
    d.rectangle([330,1000,880,1470],fill=(42,30,24))
    for y in range(1020,1470,38): d.line([330,y,880,y],fill=(30,22,18),width=6)  # logs
    d.polygon([(280,1010),(cx,700),(930,1010)],fill=(22,16,14))
    d.polygon([(260,1020),(cx,690),(950,1020),(930,1000),(cx,725),(280,1000)],fill=(210,215,230))
    d.rectangle([760,760,820,900],fill=(30,22,18))  # chimney
    for k in range(6): d.ellipse([770+k*14-20+k*k*3,700-k*55-30,770+k*14+20+k*k*3+k*6,700-k*55+10],fill=(70,74,90))
    d.rectangle([410,1150,570,1310],fill=(220,160,70)); d.line([490,1150,490,1310],fill=(40,28,20),width=10); d.line([410,1230,570,1230],fill=(40,28,20),width=10)
    d.rectangle([520,1180,545,1300],fill=(30,20,14)); d.ellipse([517,1158,548,1186],fill=(30,20,14))  # someone at the window
    d.rectangle([660,1170,790,1470],fill=(50,36,28)); d.ellipse([765,1310,778,1323],fill=(160,140,90))
    im=glow(im,(490,1230),190,(220,150,60),0.5); im=cone(im,(490,1310),(330,1700),(700,1700),(200,150,80),0.25,30)
    d=ImageDraw.Draw(im)
    for k in range(9):  # footprints to the door
        t=k/8; y=BH-60-t*(BH-60-1490); s=1-0.75*t; x=725+(1 if k%2 else -1)*30*s+(1-t)*120
        d.ellipse([x-18*s,y-34*s,x+18*s,y+34*s],fill=(56,62,84))
    pine(d,-20,BH,900,210,(3,5,7))
    return noise_tex(im,7)
def door():  # front door from inside
    im=base((16,12,10),(22,16,12)); d=ImageDraw.Draw(im)
    for x in range(0,BW,70): d.line([x,0,x,1600],fill=(20,15,12),width=3)  # wallpaper stripes
    d.rectangle([0,1600,BW,BH],fill=(30,22,16))
    for k in range(10): d.line([0,1600+k*55,BW,1600+k*55],fill=(38,28,20),width=4)
    d.rectangle([270,390,940,1610],fill=(30,22,16)); d.rectangle([300,420,910,1600],fill=(58,40,28))
    for x in (330,615):
        d.rectangle([x,460,x+265,980],outline=(38,26,18),width=12); d.rectangle([x+12,472,x+253,968],outline=(72,52,36),width=4)
        d.rectangle([x,1040,x+265,1560],outline=(38,26,18),width=12); d.rectangle([x+12,1052,x+253,1548],outline=(72,52,36),width=4)
    d.ellipse([588,700,622,734],fill=(20,16,12)); d.ellipse([596,708,614,726],fill=(200,190,150))  # peephole (lit)
    d.ellipse([820,1020,868,1068],fill=(150,125,70)); d.rectangle([835,1060,852,1130],fill=(120,100,60))
    d.line([820,860,700,900,860,960],fill=(150,140,110),width=6)  # chain lock
    d.rectangle([300,1590,910,1606],fill=(160,190,240))
    for k in range(2): d.rectangle([450+k*200,1588,520+k*200,1608],fill=(8,8,10))  # shadows of feet under the door
    d.line([1060,500,1060,1600],fill=(20,16,12),width=10); d.ellipse([1020,450,1100,530],fill=(24,18,14))  # coat rack
    d.polygon([(1030,560),(1120,560),(1150,1100),(1000,1100)],fill=(26,20,24))
    d.rectangle([60,900,200,1200],fill=(36,28,22)); d.rectangle([75,920,185,1060],fill=(48,46,40))  # mirror
    im=glow(im,(cx,1600),300,(80,110,170),0.5); im=glow(im,(605,717),60,(200,190,150),0.5)
    return noise_tex(im,8)
def prints():  # footprints in snow leading to the cabin
    im=base((8,12,26),(30,34,50)); d=ImageDraw.Draw(im); stars(d,60,600,9)
    im=moon(im,250,380,55); d=ImageDraw.Draw(im)
    for x,h in ((60,420),(200,330),(1000,380),(1140,460)): pine(d,x,760,h,110,(10,14,20))
    d.polygon([(0,700),(BW,700),(BW,BH),(0,BH)],fill=(88,94,116)); vgrad(d,(0,700,BW,1000),(64,70,92),(90,96,118))
    d.rectangle([400,460,820,720],fill=(34,24,20)); d.polygon([(360,470),(cx+10,300),(860,470)],fill=(200,205,222))
    d.rectangle([570,580,650,720],fill=(44,32,26)); d.rectangle([440,540,530,620],fill=(200,150,70))
    im=glow(im,(485,580),90,(200,150,70),0.45); d=ImageDraw.Draw(im)
    for k in range(14):
        t=k/13; y=BH-120-t*(BH-120-740); s=1-0.82*t; x=cx+(1 if k%2 else -1)*70*s+math.sin(t*3)*40
        d.ellipse([x-30*s,y-58*s,x+30*s,y+58*s],fill=(44,50,72)); d.ellipse([x-22*s,y-52*s,x+22*s,y-10*s],fill=(36,42,62))
        for tt in range(3): d.ellipse([x-20*s+tt*14*s,y-70*s,x-12*s+tt*14*s,y-60*s],fill=(40,46,66))
    for k in range(40):  # snow sparkle
        x,y=_R.random()*BW,700+_R.random()*(BH-700); d.ellipse([x-2,y-2,x+2,y+2],fill=(170,175,195))
    d.polygon([(0,BH),(0,1500),(130,1560),(220,BH)],fill=(10,12,18))
    return noise_tex(im,6)
def closet(open_=False):  # bedroom closet
    im=base((8,10,18),(12,12,16)); d=ImageDraw.Draw(im)
    for x in range(0,BW,90): d.line([x,0,x,1400],fill=(12,14,22),width=3)
    d.rectangle([0,1400,BW,BH],fill=(24,20,20)); d.rectangle([0,1390,BW,1410],fill=(36,30,28))
    d.rectangle([500,360,1080,1420],fill=(26,22,22)); d.rectangle([520,380,1060,1420],fill=(42,36,32))
    if open_:
        d.rectangle([700,410,880,1410],fill=(2,2,3))
        for k in range(4): d.line([720+k*45,420,720+k*45,520],fill=(30,28,26),width=4); d.polygon([(700+k*45,520),(740+k*45,520),(735+k*45,820),(705+k*45,820)],fill=(14,12,14))
        figure(d,790,1405,820,(10,10,12),tilt=-0.3,eyes=(225,225,200))
        d.polygon([(880,410),(1040,380),(1040,1440),(880,1410)],fill=(52,44,38))
        d.polygon([(700,1410),(880,1410),(980,1700),(620,1700)],fill=(10,9,10))
    else:
        for x0 in (540,800):
            d.rectangle([x0,400,x0+240,1400],outline=(30,26,24),width=8)
            for y in range(440,1380,40): d.line([x0+20,y,x0+220,y],fill=(34,30,28),width=6)  # louvres
        d.rectangle([785,410,800,1410],fill=(4,4,5)); im=glow(im,(792,900),120,(40,40,60),0.25); d=ImageDraw.Draw(im)
    d.ellipse([760,880,778,898],fill=(130,110,70)); d.ellipse([805,880,823,898],fill=(130,110,70))
    d.rounded_rectangle([40,1120,620,1540],30,fill=(46,38,48)); d.rounded_rectangle([20,980,150,1540],30,fill=(52,44,52))
    d.rounded_rectangle([170,1080,400,1180],30,fill=(165,165,180)); d.polygon([(150,1250),(620,1200),(620,1540),(150,1540)],fill=(60,54,72))  # pillow, blanket
    d.rectangle([90,560,380,820],fill=(18,28,46)); d.line([235,560,235,820],fill=(6,6,8),width=10)
    im=cone(im,(235,690),(200,1500),(700,1500),(60,80,130),0.2,40)
    return noise_tex(im,8)
def road():
    im=base((4,8,20),(10,10,16)); d=ImageDraw.Draw(im); stars(d,70,700,13)
    vx,vy=cx,880
    for x in range(-40,BW+80,80):
        h=300+(x*37)%260; pine(d,x,vy+10,h,70,(5,8,8))
    d.rectangle([0,vy,BW,BH],fill=(10,12,10))
    d.polygon([(vx-30,vy),(vx+30,vy),(BW+260,BH),(-260,BH)],fill=(30,30,33))
    d.line([vx-30,vy,-260,BH],fill=(150,150,140),width=5); d.line([vx+30,vy,BW+260,BH],fill=(150,150,140),width=5)
    for k in range(8):
        t=k/7; y0=vy+20+(BH-vy)*t**1.7; y1=y0+30+140*t**1.5; w=3+16*t
        d.polygon([(vx-w/2,y0),(vx+w/2,y0),(vx+w,y1),(vx-w,y1)],fill=(220,190,80))
    d.line([vx+90,vy-10,vx+130,vy+60],fill=(60,60,60),width=4); d.rectangle([vx+110,vy-60,vx+170,vy-20],fill=(30,90,40))  # sign
    figure(d,vx-120,vy+40,90,(3,3,4))  # someone standing by the road far away
    im=cone(im,(vx-200,BH),(vx-60,vy),(vx+60,vy),(200,190,150),0.3,30); im=cone(im,(vx+200,BH),(vx-60,vy),(vx+60,vy),(200,190,150),0.3,30)
    d=ImageDraw.Draw(im)
    d.polygon([(0,1600),(BW,1600),(BW,BH),(0,BH)],fill=(8,8,9)); d.polygon([(0,1600),(160,0),(0,0)],fill=(6,6,7)); d.polygon([(BW,1600),(BW-160,0),(BW,0)],fill=(6,6,7))  # dashboard + pillars
    d.arc([cx-540,1540,cx+540,2520],200,340,fill=(16,16,18),width=64)
    d.rounded_rectangle([cx-60,1640,cx+60,1700],10,fill=(20,60,80))
    return noise_tex(im,7)
def gps(red=False):
    im=base((4,5,10),(10,9,10)); d=ImageDraw.Draw(im)
    d.polygon([(0,330),(BW,330),(BW,560),(0,560)],fill=(8,12,22))  # windshield view
    for x in range(0,BW,70): pine(d,x,560,140+(x*13)%90,40,(4,6,8))
    d.polygon([(0,560),(BW,560),(BW,640),(0,640)],fill=(14,14,16))
    d.polygon([(0,330),(140,330),(0,1000)],fill=(6,6,7)); d.polygon([(BW,330),(BW-140,330),(BW,1000)],fill=(6,6,7))
    d.rectangle([0,1050,BW,BH],fill=(18,17,18)); d.polygon([(0,1000),(BW,1000),(BW,1080),(0,1080)],fill=(24,23,24))
    for k in range(3): d.rounded_rectangle([60+k*60,1120,100+k*60,1160],8,fill=(40,40,44))
    for x in (100,1060): d.rounded_rectangle([x-50,1150,x+50,1250],14,fill=(12,12,14))  # vents
    d.rounded_rectangle([230,600,980,1100],40,fill=(22,22,24))
    sc=(150,20,15) if red else (20,70,110)
    d.rounded_rectangle([270,640,940,1060],24,fill=sc)
    lc=(255,120,100) if red else (120,210,255)
    for k in range(5): d.line([300,700+k*80,900,690+k*85],fill=tuple(int(c*0.7) for c in sc),width=6)  # map lines
    d.line([605,1020,605,860,470,760],fill=lc,width=44,joint='curve')
    d.polygon([(470,700),(430,800),(530,790)],fill=lc)
    d.ellipse([585,990,625,1030],fill=(255,255,255))
    d.text((605,670),'TURN LEFT' if not red else 'REROUTING...',font=F(B,40),fill=(255,255,255),anchor='mm')
    im=glow(im,(605,850),340,sc,0.7); d=ImageDraw.Draw(im)
    d.arc([cx-560,1250,cx+560,2350],180,360,fill=(8,8,9),width=90)
    d.rectangle([cx-70,1300,cx+70,1700],fill=(8,8,9)); d.ellipse([cx-90,1700,cx+90,1860],fill=(10,10,11))
    d.polygon([(860,1500),(1000,1420),(1080,1520),(950,1600)],fill=(14,12,12))  # hand on the wheel
    return noise_tex(im,7)
def mirror(eyes=False):  # rear-view mirror showing the back seat
    im=base((6,8,14),(12,10,12)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,340],fill=(12,12,16)); d.polygon([(0,340),(BW,340),(BW,1300),(0,1300)],fill=(10,14,24))
    for x in range(0,BW,60): pine(d,x,1300,200+(x*17)%120,40,(5,7,9))  # trees through windshield
    d.rectangle([cx-20,330,cx+20,560],fill=(18,18,20))
    d.rounded_rectangle([100,530,1110,1130],100,fill=(26,26,28))
    d.rounded_rectangle([140,570,1070,1090],80,fill=(16,18,26))
    d.rectangle([160,620,1050,700],fill=(30,36,52))  # rear window
    for x in range(180,1050,90): pine(d,x,700,60,20,(14,18,26))
    d.rounded_rectangle([200,850,1010,1090],40,fill=(36,30,32)); d.rounded_rectangle([210,860,600,960],30,fill=(44,38,40)); d.rounded_rectangle([610,860,1000,960],30,fill=(44,38,40))
    d.rectangle([250,700,390,880],fill=(30,26,28)); d.rectangle([820,700,960,880],fill=(30,26,28))  # headrests
    if eyes:
        x=cx; d.ellipse([x-85,640,x+85,830],fill=(3,3,4)); d.polygon([(x-160,810),(x+160,810),(x+210,1090),(x-210,1090)],fill=(3,3,4))
        d.polygon([(x-80,700),(x-110,1000),(x-70,1000)],fill=(3,3,4)); d.polygon([(x+80,700),(x+110,1000),(x+70,1000)],fill=(3,3,4))  # long hair
        d.ellipse([x-48,712,x-20,728],fill=(235,225,205)); d.ellipse([x+20,712,x+48,728],fill=(235,225,205))
        d.arc([x-40,750,x+40,800],15,165,fill=(150,140,130),width=4)
    im=glow(im,(cx,660),320,(60,75,110),0.32)
    d=ImageDraw.Draw(im); d.line([180,600,330,1050],fill=(50,54,68),width=6)  # glare streak
    d.rectangle([0,1250,BW,BH],fill=(14,12,12)); d.polygon([(0,1250),(BW,1250),(BW,1300),(0,1300)],fill=(22,20,20))
    return noise_tex(im,7)
def farmhouse(woman=False):  # dead end: old farmhouse in headlights, one lit window
    im=base((5,8,20),(14,14,20)); d=ImageDraw.Draw(im); stars(d,110,800,21)
    im=moon(im,860,360,58); d=ImageDraw.Draw(im)
    for x in range(-40,BW+80,95): pine(d,x,1010,260+(x*29)%240,80,(6,9,10))
    d.rectangle([0,1000,BW,BH],fill=(16,16,14))
    d.polygon([(cx-60,1260),(cx+60,1260),(BW+200,BH),(-200,BH)],fill=(44,40,34))  # gravel road
    for k in range(60):
        x,y=_R.random()*BW,1270+_R.random()*(BH-1270); d.ellipse([x-3,y-2,x+3,y+2],fill=(70,64,54))
    # farmhouse
    d.rectangle([250,820,960,1260],fill=(46,44,42))
    for y in range(840,1260,30): d.line([250,y,960,y],fill=(36,34,32),width=4)  # clapboard
    d.polygon([(210,830),(cx,560),(1000,830)],fill=(24,22,22)); d.line([210,830,cx,560,1000,830],fill=(70,68,66),width=8)
    d.rectangle([820,600,880,740],fill=(30,26,24))  # chimney
    d.polygon([(560,700),(640,700),(620,760),(580,770)],fill=(18,16,16))  # broken attic window
    for x in (330,770):  # dark boarded windows
        d.rectangle([x,920,x+110,1060],fill=(14,14,16))
        d.line([x-10,950,x+120,1020],fill=(60,48,36),width=14); d.line([x-10,1030,x+120,980],fill=(60,48,36),width=14)
    d.rectangle([520,900,690,1080],fill=(170,110,50))  # the lit window
    d.line([605,900,605,1080],fill=(50,36,24),width=10); d.line([520,990,690,990],fill=(50,36,24),width=10)
    d.rectangle([505,885,705,900],fill=(60,56,52)); d.rectangle([505,1080,705,1094],fill=(60,56,52))
    if woman:
        d.ellipse([590,920,640,975],fill=(8,6,6)); d.polygon([(570,975),(660,975),(675,1080),(555,1080)],fill=(8,6,6))
        d.polygon([(586,940),(574,1040),(594,1040)],fill=(8,6,6)); d.polygon([(644,940),(656,1040),(636,1040)],fill=(8,6,6))  # long hair
        d.polygon([(655,990),(700,905),(712,912),(668,995)],fill=(8,6,6))  # waving arm
        for f in range(4): d.line([706,906,700+f*7,885],fill=(8,6,6),width=5)
        d.ellipse([601,940,611,946],fill=(240,230,210)); d.ellipse([619,940,629,946],fill=(240,230,210))
    d.rectangle([250,1150,960,1170],fill=(34,30,28)); d.rectangle([240,1140,970,1152],fill=(60,56,52))  # porch
    for x in (270,450,760,940): d.rectangle([x-8,1150,x+8,1260],fill=(56,52,48))
    d.rectangle([380,1180,470,1260],fill=(20,18,18))  # front door ajar
    d.line([300,1260,240,1300],fill=(30,28,26),width=6); d.line([860,1260,950,1310],fill=(30,28,26),width=6)
    for x in range(40,250,40): d.line([x,1240,x,1300],fill=(40,36,30),width=6)  # broken fence
    d.line([30,1255,250,1250],fill=(40,36,30),width=5)
    d.line([1000,1250,1010,1110],fill=(40,36,30),width=6); d.rectangle([965,1110,1060,1150],fill=(60,50,40))  # mailbox
    im=glow(im,(605,990),200,(200,130,60),0.28)
    im=cone(im,(cx-260,BH),(220,1000),(700,1000),(200,190,150),0.13,40); im=cone(im,(cx+260,BH),(500,1000),(1000,1000),(200,190,150),0.13,40)
    d=ImageDraw.Draw(im)
    d.polygon([(0,1640),(BW,1640),(BW,BH),(0,BH)],fill=(8,8,9)); d.polygon([(0,1640),(170,0),(0,0)],fill=(6,6,7)); d.polygon([(BW,1640),(BW-170,0),(BW,0)],fill=(6,6,7))  # dashboard + pillars
    d.arc([cx-540,1580,cx+540,2560],200,340,fill=(16,16,18),width=64)
    pine(d,-30,1400,900,200,(3,4,5))
    return noise_tex(im,7)
def clipping():  # old newspaper clipping under a desk lamp
    im=base((10,9,8),(16,13,10)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,BH],fill=(30,22,16))
    for y in range(0,BH,90): d.line([0,y+((y*7)%30),BW,y+((y*13)%30)],fill=(24,18,13),width=5)  # wood grain
    d.rounded_rectangle([60,330,420,560],10,fill=(20,20,24)); d.rounded_rectangle([80,350,400,540],6,fill=(30,60,80))  # laptop corner
    d.text((100,380),'COUNTY RECORDS',font=F(M,24),fill=(150,210,230))
    for k in range(4): d.line([100,430+k*26,360-k*30,430+k*26],fill=(90,150,170),width=6)
    d.polygon([(230,620),(930,580),(980,1440),(250,1480)],fill=(112,102,80))  # clipping
    d.polygon([(930,580),(980,1440),(960,1450),(905,600)],fill=(84,76,58))
    d.text((290,650),'FARMHOUSE FIRE',font=F(SERIFD,54),fill=(14,12,10))
    d.text((300,730),'ON ROUTE 9',font=F(SERIFD,54),fill=(14,12,10))
    d.text((305,815),'OCTOBER 31, 1987',font=F(M,28),fill=(36,30,24))
    d.rectangle([310,870,890,1170],fill=(60,56,48))  # photo of burned house
    d.rectangle([310,1050,890,1170],fill=(40,38,34))
    d.polygon([(380,1050),(380,950),(470,890),(560,960),(560,1050)],fill=(20,18,16)); d.polygon([(620,1050),(640,930),(700,980),(760,920),(820,1050)],fill=(22,20,18))
    for k in range(5): d.ellipse([480+k*40,890-k*8,540+k*48,930-k*8],fill=(90,86,78))
    for k in range(8): d.line([320,1200+k*30,880-(k%3)*60,1196+k*30],fill=(60,54,42),width=8)
    d.ellipse([300,1300,420,1420],outline=(170,30,25),width=6)  # red ink circle
    d.text((316,1340),'1 MISSING',font=F(B,18),fill=(170,30,25))
    d.line([150,1500,500,1580],fill=(170,30,25),width=10); d.polygon([(500,1580),(470,1560),(475,1595)],fill=(170,30,25))  # red pen
    d.ellipse([880,1500,1060,1600],fill=(46,34,26)); d.ellipse([900,1515,1040,1585],fill=(24,14,10))  # coffee cup
    d.rectangle([780,300,900,380],fill=(20,18,16)); d.polygon([(700,380),(980,380),(1050,520),(630,520)],fill=(36,32,28))  # lamp shade
    im=glow(im,(600,1000),480,(170,110,50),0.22); im=cone(im,(840,500),(200,1500),(1100,1450),(200,150,80),0.12,50)
    d=ImageDraw.Draw(im)
    d.polygon([(0,BH),(0,1560),(200,1620),(320,BH)],fill=(8,6,5))  # foreground shadow
    return noise_tex(im,7)
# Scene library. Add new scene functions above and register them here.

def _crib(d,x,y,w,h,col,bar):  # crib seen from the side; (x,y)=top-left
    d.rectangle([x,y+h*0.55,x+w,y+h*0.62],fill=col)          # mattress rail
    d.rectangle([x,y,x+w,y+h*0.07],fill=col)                 # top rail
    d.rectangle([x-w*0.04,y-h*0.12,x+w*0.03,y+h],fill=col); d.rectangle([x+w*0.97,y-h*0.12,x+w*1.04,y+h],fill=col)  # posts
    for k in range(1,12): xx=x+w*k/12; d.line([xx,y+h*0.07,xx,y+h*0.55],fill=bar,width=max(2,int(w/90)))
def _nv(mode):  # night-vision camera picture (green), returns an image of size 600x420
    sw,sh=600,420; im=Image.new('RGB',(sw,sh),(8,30,14)); d=ImageDraw.Draw(im)
    if mode=='me':  # living room seen from a ceiling corner: sofa, girl on it, figure behind
        d.polygon([(0,0),(sw,0),(sw,sh*0.55),(0,sh*0.62)],fill=(14,48,22)); d.polygon([(0,sh*0.62),(sw,sh*0.55),(sw,sh),(0,sh)],fill=(10,38,18))
        d.rectangle([60,60,190,170],fill=(40,110,55)); d.line([125,60,125,170],fill=(14,48,22),width=5)  # window
        d.rounded_rectangle([150,250,470,360],20,fill=(24,72,34)); d.rounded_rectangle([140,215,480,275],18,fill=(30,86,40))  # sofa
        d.ellipse([285,195,325,240],fill=(70,150,80)); d.rounded_rectangle([272,236,338,300],14,fill=(58,130,68))  # girl
        d.rectangle([292,262,318,280],fill=(140,230,140))  # monitor glow in her hands
        d.ellipse([382,40,428,96],fill=(4,14,6)); d.polygon([(372,95),(438,95),(450,250),(360,250)],fill=(4,14,6))  # figure behind sofa
        d.polygon([(372,100),(330,230),(345,236),(385,120)],fill=(4,14,6))  # arm reaching toward her
        d.ellipse([393,60,403,68],fill=(210,255,210)); d.ellipse([408,60,418,68],fill=(210,255,210))
    else:  # nursery from above the crib
        d.polygon([(0,sh*0.6),(sw,sh*0.6),(sw,sh),(0,sh)],fill=(10,40,18))
        d.rectangle([420,50,540,170],fill=(34,96,48)); d.line([480,50,480,170],fill=(10,36,16),width=5)
        d.line([200,0,200,70],fill=(60,140,70),width=3)
        for k in range(4): a=k*1.57; d.ellipse([200+50*math.cos(a)-12,90+10*math.sin(a)-12,200+50*math.cos(a)+12,90+10*math.sin(a)+12],fill=(60,140,70))  # mobile
        _crib(d,110,150,300,190,(40,110,55),(34,96,48))
        d.ellipse([220,215,300,250],fill=(90,180,100)); d.ellipse([290,212,322,244],fill=(110,200,115))  # sleeping baby
        if mode=='man':
            d.ellipse([430,60,480,118],fill=(3,12,5)); d.polygon([(420,116),(492,116),(505,sh),(410,sh)],fill=(3,12,5))
            d.polygon([(425,140),(380,170),(392,184),(440,160)],fill=(3,12,5))  # long arm resting on the crib rail
            d.polygon([(380,170),(350,158),(354,170),(392,184)],fill=(3,12,5))
            d.ellipse([440,80,451,88],fill=(220,255,220)); d.ellipse([459,80,470,88],fill=(220,255,220))
    a=np.asarray(im,dtype=np.float32)
    a[::4]*=0.72                                              # scanlines
    a+=np.random.default_rng(5).normal(0,10,a.shape[:2])[...,None]*np.array([0.4,1,0.5])
    im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im)
    d.text((18,14),'CAM 1' if mode!='me' else 'CAM 2',font=F(M,28),fill=(170,255,170)); d.ellipse([sw-44,18,sw-22,40],fill=(230,40,30))
    d.text((18,sh-44),'02:47 AM',font=F(M,28),fill=(170,255,170))
    return im
def monitor(mode='empty'):  # handheld baby monitor glowing on a sofa armrest in a dark living room
    im=base((6,8,14),(12,10,12)); d=ImageDraw.Draw(im)
    d.rectangle([700,300,1060,820],fill=(16,22,38)); d.line([880,300,880,820],fill=(6,6,9),width=14); d.line([700,560,1060,560],fill=(6,6,9),width=14)  # window
    for x in (680,1080): d.polygon([(x-30,260),(x+30,260),(x+50,1000),(x-40,1000)],fill=(10,9,12))  # curtains
    d.rectangle([110,360,330,560],fill=(22,20,22)); d.rectangle([125,375,315,545],fill=(30,30,38))  # picture frame
    d.ellipse([170,410,270,500],fill=(40,40,50))
    d.rectangle([0,1000,BW,1012],fill=(26,22,22))  # baseboard
    vgrad(d,(0,1012,BW,BH),(22,18,18),(10,8,8))
    d.rounded_rectangle([-60,1120,BW+60,1520],80,fill=(30,24,26)); d.rounded_rectangle([-60,1060,360,1200],60,fill=(38,30,32))  # sofa + armrest
    d.line([0,1300,BW,1300],fill=(22,18,20),width=6)
    px,py=cx,840
    d.rounded_rectangle([px-360,py-300,px+360,py+330],50,fill=(20,20,24)); d.rounded_rectangle([px-345,py-285,px+345,py+315],44,fill=(34,34,40))
    d.rectangle([px+230,py-420,px+262,py-300],fill=(22,22,26)); d.ellipse([px+226,py-436,px+266,py-404],fill=(28,28,32))  # antenna
    for k in range(3): d.ellipse([px-60+k*50,py+250,px-30+k*50,py+280],fill=(60,60,70))
    d.ellipse([px+220,py+250,px+250,py+280],fill=(60,220,90) if mode!='me' else (230,50,40))
    scr=_nv(mode); im.paste(scr,(px-300,py-250))
    im=glow(im,(px,py-40),420,(40,150,70) if mode!='me' else (60,150,60),0.5); im.paste(scr.point(lambda v:min(255,int(v*1.15))),(px-300,py-250))
    im=cone(im,(px,py+330),(px-600,1500),(px+600,1500),(40,120,60),0.22,50)
    d=ImageDraw.Draw(im); d.line([px-280,py-240,px-120,py+150],fill=(90,140,100),width=4)  # glare
    return noise_tex(im,7)
def nursery():  # dark nursery, crib under the window, star night light
    im=base((8,10,20),(14,12,16)); d=ImageDraw.Draw(im)
    for y in range(300,1150,70):
        for x in range(30 if (y//70)%2 else 70,BW,80): d.ellipse([x-5,y-5,x+5,y+5],fill=(20,22,34))  # wallpaper dots
    d.rectangle([380,330,840,860],fill=(26,34,58)); im=moon(im,700,460,55); d=ImageDraw.Draw(im)
    d.line([610,330,610,860],fill=(8,8,12),width=14); d.line([380,595,840,595],fill=(8,8,12),width=14)
    for x in (360,860): d.polygon([(x-40,300),(x+40,300),(x+60,1000),(x-50,1000)],fill=(30,22,34))
    d.rectangle([0,1150,BW,1162],fill=(30,26,30)); vgrad(d,(0,1162,BW,BH),(30,24,24),(12,10,10))
    im=cone(im,(610,600),(330,1500),(950,1500),(80,100,150),0.25,40); d=ImageDraw.Draw(im)
    _crib(d,250,940,700,480,(48,40,44),(38,32,36))
    d.ellipse([480,1160,700,1250],fill=(70,64,80)); d.ellipse([680,1150,760,1230],fill=(90,80,90))  # sleeping baby
    d.line([600,700,600,840],fill=(50,46,56),width=4)
    for k in range(5): a=k*1.26; d.ellipse([600+90*math.cos(a)-18,870+16*math.sin(a)-18,600+90*math.cos(a)+18,870+16*math.sin(a)+18],fill=(60,54,70))  # mobile
    d.rounded_rectangle([60,1250,220,1500],12,fill=(24,20,22))  # dresser
    im=glow(im,(140,1220),110,(200,150,60),0.7); d=ImageDraw.Draw(im)
    st=[(140+44*math.cos(math.pi/2+k*math.pi/5)*(1 if k%2==0 else 0.45),1220-44*math.sin(math.pi/2+k*math.pi/5)*(1 if k%2==0 else 0.45)) for k in range(10)]
    d.polygon(st,fill=(255,210,120))  # star night light
    d.polygon([(BW-130,250),(BW,250),(BW,BH),(BW-190,BH)],fill=(5,5,7))  # door frame foreground
    return noise_tex(im,7)
def _rain(d,n=160,seed=7,col=(70,80,100)):
    r=np.random.default_rng(seed)
    for _ in range(n):
        x,y=r.random()*BW,r.random()*BH; l=r.random()*40+25; d.line([x,y,x-l*0.25,y+l],fill=col,width=2)
def lighthouse():  # lighthouse on a rocky island in a storm, lamp burning, beams sweeping the sea
    im=base((6,9,18),(12,16,24)); d=ImageDraw.Draw(im); stars(d,40,500,31)
    im=moon(im,230,420,50,(190,196,210)); d=ImageDraw.Draw(im)
    for k,(x,y,w,h) in enumerate(((-100,380,700,170),(420,300,900,200),(150,560,800,150),(700,520,700,180))):  # storm clouds
        d.ellipse([x,y,x+w,y+h],fill=(16+k*2,20+k*2,30+k*2))
    d.rectangle([0,1180,BW,BH],fill=(10,16,22)); vgrad(d,(0,1180,BW,1700),(18,26,34),(8,12,18))  # sea
    for k in range(40):  # waves
        y=1200+(k*37)%480; x=(k*173)%BW; w=60+(k*31)%120; d.arc([x-w,y-14,x+w,y+14],200,340,fill=(46,60,72),width=4)
    d.polygon([(120,1260),(260,1110),(420,1080),(620,1050),(860,1090),(1010,1180),(1110,1290),(60,1300)],fill=(22,22,24))  # island rock
    d.polygon([(260,1110),(420,1080),(520,1100),(380,1160)],fill=(34,34,36)); d.polygon([(860,1090),(1010,1180),(900,1170)],fill=(30,30,32))
    for x in (180,1060): d.ellipse([x-90,1260,x+90,1310],fill=(120,135,145))  # surf foam
    tx,tb,tt=640,1100,690  # tower centre x, base y, top y
    d.polygon([(tx-110,tb),(tx+110,tb),(tx+70,tt),(tx-70,tt)],fill=(150,148,142))
    d.polygon([(tx+20,tb),(tx+110,tb),(tx+70,tt),(tx+15,tt)],fill=(96,96,96))  # shaded side
    for y0 in (700,900):  # red bands
        f0=(y0-tt)/(tb-tt); f1=(y0+80-tt)/(tb-tt); w0=70+40*f0; w1=70+40*f1
        d.polygon([(tx-w0,y0),(tx+w0,y0),(tx+w1,y0+80),(tx-w1,y0+80)],fill=(120,30,26))
    for y in (760,960): d.rectangle([tx-12,y,tx+12,y+34],fill=(30,28,26))  # small tower windows
    d.rectangle([tx-95,tt-14,tx+95,tt+6],fill=(26,26,28)); d.line([tx-100,tt-30,tx+100,tt-30],fill=(30,30,32),width=5)  # gallery + rail
    for x in range(tx-96,tx+100,24): d.line([x,tt-30,x,tt-12],fill=(30,30,32),width=3)
    d.rectangle([tx-58,tt-120,tx+58,tt-14],fill=(240,200,120))  # lantern room glass
    for x in (tx-30,tx,tx+30): d.line([x,tt-120,x,tt-14],fill=(40,34,28),width=5)
    d.polygon([(tx-70,tt-120),(tx+70,tt-120),(tx,tt-185)],fill=(30,30,32)); d.ellipse([tx-10,tt-200,tx+10,tt-180],fill=(30,30,32))  # roof
    d.rectangle([800,1000,1000,1100],fill=(70,66,60)); d.polygon([(785,1005),(900,930),(1015,1005)],fill=(40,36,34))  # keeper's cottage
    d.rectangle([840,1030,880,1070],fill=(14,14,16)); d.rectangle([930,1035,970,1100],fill=(26,22,20))  # dark window, door
    im=glow(im,(tx,tt-70),260,(230,170,80),0.55)
    im=cone(im,(tx,tt-70),(-200,tt-260),(-200,tt+160),(230,200,140),0.32,30)  # beam to the left
    im=cone(im,(tx,tt-70),(BW+250,tt-40),(BW+250,tt+220),(230,200,140),0.18,40)
    im=cone(im,(tx,tt-70),(200,1300),(700,1300),(200,170,110),0.06,60)
    d=ImageDraw.Draw(im); _rain(d)
    d.polygon([(0,BH),(0,1480),(160,1430),(330,1520),(520,1600),(560,BH)],fill=(5,6,7))  # foreground rocks
    d.polygon([(BW,BH),(BW,1520),(1050,1500),(900,1620),(820,BH)],fill=(4,5,6))
    for k in range(18): x=20+k*28; d.line([x,1500,x+((k%3)-1)*30,1380+(k*13)%60],fill=(8,10,9),width=4)  # dune grass
    return noise_tex(im,8)
def lh_stairs(mode=0):  # looking DOWN the spiral staircase of the lighthouse; mode 1/2 = figure far/close
    im=base((10,10,12),(4,4,6)); d=ImageDraw.Draw(im)
    ccx,ccy=cx+30,1080; n=13
    for k in range(n):
        r=640*0.80**k; s=1.0-k/n
        wall=tuple(int(v*s) for v in (38,36,34)); step=tuple(int(v*s) for v in (66,60,52))
        d.ellipse([ccx-r,ccy-r*0.92,ccx+r,ccy+r*0.92],fill=wall)
        ri=r*0.86; d.ellipse([ccx-ri,ccy-ri*0.92,ccx+ri,ccy+ri*0.92],fill=step)  # stone step ring
        for j in range(16):  # step edges
            a=j*math.pi/8+k*0.35; d.line([ccx+ri*math.cos(a),ccy+ri*0.92*math.sin(a),ccx+r*0.80*math.cos(a)*0.8,ccy+r*0.80*0.92*math.sin(a)*0.8],fill=tuple(int(v*s) for v in (40,36,32)),width=max(1,int(5*s)))
        rr=r*0.66; d.ellipse([ccx-rr,ccy-rr*0.92,ccx+rr,ccy+rr*0.92],outline=tuple(int(v*s) for v in (30,26,22)),width=max(2,int(10*s)))  # iron rail
        for j in range(12):
            a=j*math.pi/6+k*0.2; d.line([ccx+rr*math.cos(a),ccy+rr*0.92*math.sin(a),ccx+rr*0.94*math.cos(a),ccy+rr*0.92*0.94*math.sin(a)+16*s],fill=tuple(int(v*s) for v in (30,26,22)),width=max(1,int(4*s)))
        rh=r*0.60; d.ellipse([ccx-rh,ccy-rh*0.92,ccx+rh,ccy+rh*0.92],fill=tuple(int(v*s*0.6) for v in (40,38,36)))
    d.ellipse([ccx-34,ccy-30,ccx+34,ccy+30],fill=(0,0,0))  # bottomless centre
    for k in range(3):  # small slit windows with moonlight
        a=0.6+k*2.0; r=640*0.80**(k*2+1)*0.93
        x,y=ccx+r*math.cos(a),ccy+r*0.92*math.sin(a); d.rectangle([x-10,y-24,x+10,y+24],fill=(70,90,120))
        im=glow(im,(int(x),int(y)),60,(60,80,120),0.4); d=ImageDraw.Draw(im)
    if mode==1:  # small figure far down, face turned up
        x,y=ccx-150,ccy+70; d.ellipse([x-22,y-26,x+22,y+20],fill=(3,3,4)); d.ellipse([x-30,y+10,x+30,y+60],fill=(3,3,4))
        d.polygon([(x+24,y+20),(x+90,y-30),(x+96,y-20),(x+30,y+34)],fill=(3,3,4))  # arm on the rail
        d.ellipse([x-12,y-10,x-4,y-4],fill=(220,215,190)); d.ellipse([x+4,y-10,x+12,y-4],fill=(220,215,190))
    if mode==2:  # tall thin figure one turn below, face tilted up at us, long arm sliding along the rail
        x,y=ccx+160,ccy+300
        d.polygon([(x-70,y+40),(x+70,y+40),(x+110,y+260),(x-110,y+260)],fill=(3,3,4))  # shoulders/body (foreshortened)
        d.ellipse([x-55,y-75,x+55,y+55],fill=(3,3,4))  # head
        d.polygon([(x-40,y-50),(x-75,y+90),(x-50,y+90)],fill=(3,3,4)); d.polygon([(x+40,y-50),(x+75,y+90),(x+50,y+90)],fill=(3,3,4))  # hair
        d.polygon([(x-70,y+60),(x-300,y-40),(x-290,y-62),(x-60,y+30)],fill=(3,3,4))  # long arm on the rail
        for f in range(4): d.line([x-295,y-50,x-335+f*8,y-80+f*12],fill=(3,3,4),width=7)
        d.ellipse([x-32,y-24,x-10,y-10],fill=(240,232,200)); d.ellipse([x+10,y-24,x+32,y-10],fill=(240,232,200))
        im=glow(im,(x,y-15),60,(150,30,25),0.3); d=ImageDraw.Draw(im)
    im=cone(im,(cx-260,250),(ccx-420,1500),(ccx+260,1500),(220,190,130),0.10,50)  # our lantern light from above
    im=glow(im,(cx-260,330),120,(230,170,80),0.5)
    d=ImageDraw.Draw(im)
    d.polygon([(0,0),(BW,0),(BW,250),(0,330)],fill=(6,6,7))  # landing edge foreground
    d.line([0,330,BW,250],fill=(30,28,24),width=10)
    d.polygon([(0,BH),(0,1560),(240,1640),(300,BH)],fill=(5,5,6)); d.polygon([(BW,BH),(BW,1580),(BW-200,1660),(BW-250,BH)],fill=(5,5,6))
    return noise_tex(im,8)
def lantern():  # lantern room at the top: huge glowing Fresnel lens, storm through the glass
    im=base((8,10,16),(14,12,12)); d=ImageDraw.Draw(im)
    vgrad(d,(0,300,BW,1250),(12,18,30),(18,24,32))  # night outside the glass
    for k in range(30): y=1000+(k*29)%250; x=(k*211)%BW; d.arc([x-70,y-10,x+70,y+10],200,340,fill=(40,52,64),width=3)  # far sea
    for x in range(0,BW+200,200): d.line([x,300,x-120,1250],fill=(22,20,20),width=16)  # diagonal astragals
    d.line([0,780,BW,760],fill=(22,20,20),width=12)
    d.rectangle([0,1250,BW,BH],fill=(26,22,20)); d.rectangle([0,1240,BW,1262],fill=(46,40,34))  # iron floor
    for x in range(0,BW,90): d.line([x,1262,x-200,BH],fill=(20,18,16),width=4)
    lx,ly=cx,860  # lens centre
    d.rectangle([lx-70,1120,lx+70,1260],fill=(30,26,22)); d.polygon([(lx-130,1260),(lx+130,1260),(lx+90,1180),(lx-90,1180)],fill=(38,34,30))  # pedestal
    im=glow(im,(lx,ly),460,(240,180,90),0.3); d=ImageDraw.Draw(im)
    d.ellipse([lx-230,ly-300,lx+230,ly+300],fill=(150,105,50))  # beehive lens
    for k in range(13):  # prism rings
        y=ly-280+k*46; w=230*math.sqrt(max(0,1-((y-ly)/300)**2))
        d.line([lx-w,y,lx+w,y],fill=(250,220,150),width=6); d.line([lx-w,y+14,lx+w,y+14],fill=(150,100,50),width=4)
    d.ellipse([lx-60,ly-60,lx+60,ly+60],fill=(255,240,200)); im=glow(im,(lx,ly),130,(255,220,150),0.45)
    im=cone(im,(lx,ly),(-300,ly-200),(-300,ly+260),(240,210,150),0.35,30); im=cone(im,(lx,ly),(BW+300,ly-150),(BW+300,ly+300),(240,210,150),0.22,40)
    d=ImageDraw.Draw(im); _rain(d,90,9,(60,70,90))
    d.rectangle([60,1380,330,1440],fill=(36,28,22)); d.rectangle([80,1440,110,1700],fill=(26,20,16))  # small desk edge
    d.rounded_rectangle([120,1300,200,1380],10,fill=(40,34,28)); d.ellipse([140,1270,180,1310],fill=(70,60,40))  # oil can
    d.polygon([(0,0),(150,0),(110,BH),(0,BH)],fill=(6,6,7)); d.polygon([(BW,0),(BW-120,0),(BW-90,BH),(BW,BH)],fill=(5,5,6))  # iron frame foreground
    d.line([0,300,BW,300],fill=(10,10,11),width=30)
    return noise_tex(im,8)
def logbook(red=False,entry=('The new','keeper is','coming up.')):  # keeper's logbook open on a desk under an oil lamp; red = the new entry in fresh ink
    im=base((12,10,8),(18,14,10)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,BH],fill=(32,24,18))
    for y in range(0,BH,80): d.line([0,y+((y*7)%25),BW,y+((y*11)%25)],fill=(26,19,14),width=5)  # wood grain
    d.rectangle([780,330,1100,700],fill=(22,26,36)); d.line([940,330,940,700],fill=(10,10,12),width=10)  # porthole-ish window
    im=moon(im,1010,420,30,(170,176,190)); d=ImageDraw.Draw(im)
    d.polygon([(110,700),(cx,740),(cx,1400),(130,1440)],fill=(112,102,80)); d.polygon([(cx,740),(BW-110,700),(BW-130,1440),(cx,1400)],fill=(120,110,86))  # pages
    d.line([cx,740,cx,1400],fill=(90,80,60),width=8)
    d.polygon([(110,700),(130,1440),(110,1460),(90,710)],fill=(60,30,20)); d.polygon([(BW-110,700),(BW-130,1440),(BW-110,1460),(BW-90,710)],fill=(60,30,20))  # cover
    fh=F(SERIFD,30); fs=F(M,24)
    for k,(dt,txt) in enumerate((('OCT 29 1952','Wind NE. Lamp lit 5:02.'),('OCT 30 1952','Heard steps again.'),('OCT 31 1952','It is on the stairs.'))):
        y=800+k*170; d.text((170,y),dt,font=fs,fill=(50,40,30)); d.text((170,y+40),txt,font=F(SERIFD,26),fill=(40,32,24))
        d.line([170,y+90,520,y+92],fill=(120,110,88),width=2)
    for k in range(8): d.line([cx+50,790+k*70,BW-160,792+k*70],fill=(130,120,95),width=2)  # ruled lines right page
    d.text((cx+60,800),'NOV 2 2016',font=fs,fill=(120,20,16) if red else (50,40,30))
    if red:
        ink=(150,18,14)
        for k,ln in enumerate(entry): d.text((cx+60,860+k*70),ln,font=F(SERIFD,44),fill=ink)
        for x in (cx+120,cx+300,cx+210): d.line([x,1060,x+2,1060+(x%5)*18+40],fill=ink,width=5)  # wet ink running
    else:
        for k in range(3): d.line([cx+60,880+k*70,cx+300-k*40,878+k*70],fill=(70,30,24),width=6)  # scribbled lines
    d.line([cx+250,1250,BW-60,1520],fill=(20,16,12),width=14); d.polygon([(cx+250,1250),(cx+275,1270),(cx+240,1235)],fill=(40,40,44))  # fountain pen
    d.rectangle([120,300,260,330],fill=(40,30,22)); d.ellipse([140,340,240,480],fill=(200,150,70))  # oil lamp
    d.polygon([(150,330),(230,330),(250,520),(130,520)],fill=(120,90,50)); d.rectangle([120,520,260,560],fill=(50,38,28))
    im=glow(im,(190,420),300,(230,150,60) if not red else (220,90,50),0.3)
    im=cone(im,(190,420),(100,1500),(1000,1450),(210,150,80),0.07,60)
    if red: im=glow(im,(cx+200,950),260,(140,10,10),0.35)
    d=ImageDraw.Draw(im)
    d.polygon([(0,BH),(0,1560),(260,1620),(360,BH)],fill=(8,6,5)); d.polygon([(BW,BH),(BW,1600),(BW-180,1660),(BW-240,BH)],fill=(8,6,5))
    return noise_tex(im,7)
def lh_door(open_=False):  # top of the lighthouse: heavy iron door in the curved stone wall; open = empty stairs + wet footprints going down
    im=base((14,12,12),(8,8,10)); d=ImageDraw.Draw(im)
    for r in range(0,BH,70):  # curved stone wall blocks
        off=35 if (r//70)%2 else 0
        for x in range(-off,BW,140): d.rectangle([x+3,r+3,x+137,r+67],fill=(44+(x*7+r)%14,40+(x*5+r)%12,38+(x*3)%10))
    for (x,y,l) in ((140,520,180),(900,700,140),(820,1180,160)): d.line([x,y,x+l*0.4,y+l*0.5,x+l*0.2,y+l],fill=(22,20,20),width=4)  # cracks
    dx0,dy0,dx1,dy1=330,520,800,1420  # door frame
    d.rectangle([dx0-40,dy0-40,dx1+40,dy1],fill=(28,26,26)); d.pieslice([dx0-40,dy0-200,dx1+40,dy0+120],180,360,fill=(28,26,26))
    if open_:
        d.rectangle([dx0,dy0,dx1,dy1],fill=(6,6,8)); d.pieslice([dx0,dy0-160,dx1,dy0+80],180,360,fill=(6,6,8))
        for k in range(7):  # spiral steps going down into darkness
            s=1-k/7; y=dy1-40-k*95; xl=dx0+30+k*25; xr=dx1-30-k*60
            d.polygon([(xl,y),(xr,y-25),(xr,y+10),(xl,y+40)],fill=tuple(int(v*s) for v in (70,64,56)))
            d.line([xl,y,xr,y-25],fill=tuple(int(v*s) for v in (110,100,85)),width=3)
        d.line([dx1-60,dy1,dx1-160,dy0+60],fill=(30,26,22),width=10)  # iron rail
        d.polygon([(dx1,dy0-40),(dx1+200,dy0+20),(dx1+200,dy1+60),(dx1,dy1)],fill=(52,44,40))  # door swung open
        for y in range(dy0+60,dy1,110): d.ellipse([dx1+90,y,dx1+110,y+20],fill=(80,70,62))
        im=glow(im,(dx0+220,dy0+300),150,(30,40,70),0.4); d=ImageDraw.Draw(im)
    else:
        d.rectangle([dx0,dy0,dx1,dy1],fill=(54,46,42)); d.pieslice([dx0,dy0-160,dx1,dy0+80],180,360,fill=(54,46,42))
        for y in (dy0+40,dy0+420,dy1-120): d.rectangle([dx0,y,dx1,y+46],fill=(36,30,28))  # iron straps
        for y in (dy0+40,dy0+420,dy1-120):
            for x in range(dx0+30,dx1,60): d.ellipse([x-7,y+16,x+7,y+30],fill=(90,80,70))  # rivets
        d.ellipse([dx1-120,950,dx1-40,1030],outline=(110,96,70),width=12)  # ring handle
        d.rectangle([dx1-90,1060,dx1-70,1100],fill=(4,4,4)); im=glow(im,(dx1-80,1080),40,(160,190,230),0.6)  # keyhole, pale light
        im=glow(im,(cx,dy1-5),200,(80,100,140),0.25)  # cold light under the door
        d=ImageDraw.Draw(im); d.rectangle([dx0,dy1-6,dx1,dy1],fill=(140,160,190))
    d=ImageDraw.Draw(im)
    d.rectangle([0,dy1,BW,BH],fill=(26,22,20)); d.rectangle([0,dy1,BW,dy1+18],fill=(46,40,34))  # iron floor
    for x in range(0,BW+300,110): d.line([x,dy1+18,x-260,BH],fill=(18,16,14),width=4)
    if open_:  # wet footprints from the lamp room through the door, going down
        for k,(x,y) in enumerate(((cx+60,1690),(cx-40,1610),(cx+40,1540),(cx-30,1480),(cx+20,1435))):
            w=46-k*5; d.ellipse([x-w*0.5,y-w,x+w*0.5,y+w*0.4],fill=(70,82,96)); d.ellipse([x-w*0.4,y+w*0.5,x+w*0.4,y+w*1.0],fill=(70,82,96))
            d.ellipse([x-w*0.3,y-w*0.8,x,y-w*0.2],fill=(120,135,150))
    im=glow(im,(BW-60,600),360,(240,170,80),0.45)  # the great lens behind us (right)
    im=cone(im,(BW,620),(dx0,dy1+200),(dx1+300,dy1+300),(230,170,90),0.12,60)
    d=ImageDraw.Draw(im)
    d.rectangle([60,1280,230,1300],fill=(40,30,22)); d.ellipse([100,1180,190,1290],fill=(180,130,60)); im=glow(im,(145,1235),110,(230,150,60),0.4); d=ImageDraw.Draw(im)  # oil lamp on a ledge
    for k in range(5): d.arc([860+k*6,1300-k*16,1010-k*6,1360-k*16],0,360,fill=(70,56,36),width=8)  # coiled rope
    d.rectangle([110,640,250,720],fill=(70,62,44)); d.text((125,660),'NO. 112',font=F(M,30),fill=(30,24,18))  # brass plaque
    d.polygon([(0,0),(170,0),(130,BH),(0,BH)],fill=(6,6,7)); d.polygon([(BW,0),(BW-110,0),(BW-80,BH),(BW,BH)],fill=(5,5,6))  # iron frame foreground
    return noise_tex(im,8)
def dock_boat():  # stone jetty at night, cut mooring rope, my rowboat drifting out with a woman rowing it, lighthouse far behind
    im=base((6,9,18),(12,16,24)); d=ImageDraw.Draw(im); stars(d,60,600,41)
    im=moon(im,820,420,55,(195,200,214)); d=ImageDraw.Draw(im)
    for k,(x,y,w,h) in enumerate(((-150,520,700,140),(500,600,800,130))): d.ellipse([x,y,x+w,y+h],fill=(16+k*3,20+k*3,30+k*3))
    hy=900; d.rectangle([0,hy,BW,BH],fill=(10,16,22)); vgrad(d,(0,hy,BW,1500),(22,30,40),(8,12,18))
    d.polygon([(760,hy),(880,hy),(1000,1500),(640,1500)],fill=(30,40,52))  # moon path on the water
    for k in range(50): y=hy+15+(k*29)%600; x=(k*173)%BW; w=40+(k*31)%110; d.arc([x-w,y-10,x+w,y+10],200,340,fill=(52,66,80),width=3)
    lx=170; d.polygon([(lx-28,hy),(lx+28,hy),(lx+16,hy-230),(lx-16,hy-230)],fill=(120,118,112)); d.rectangle([lx-22,hy-280,lx+22,hy-230],fill=(250,210,130))  # distant lighthouse
    d.polygon([(lx-30,hy-280),(lx+30,hy-280),(lx,hy-315)],fill=(30,30,32)); d.polygon([(0,hy+10),(80,hy-20),(300,hy-10),(380,hy+12)],fill=(18,18,20))
    im=glow(im,(lx,hy-255),140,(240,180,90),0.6); im=cone(im,(lx,hy-255),(BW+200,hy-420),(BW+200,hy-200),(230,200,140),0.22,30)
    d=ImageDraw.Draw(im)
    bx,by=860,1150  # rowboat out on the water, on the moon path
    d.polygon([(bx-170,by),(bx+170,by),(bx+130,by+50),(bx-140,by+50)],fill=(40,30,24)); d.line([bx-170,by,bx+170,by],fill=(90,70,50),width=6)
    d.ellipse([bx-200,by+40,bx+200,by+70],fill=(50,64,78))  # wake
    figure(d,bx-10,by+6,230,(4,4,6),tilt=0.6,long_arms=False)
    d.polygon([(bx-25,by-215),(bx-62,by-80),(bx-32,by-100)],fill=(4,4,6)); d.polygon([(bx+20,by-215),(bx+48,by-90),(bx+22,by-100)],fill=(4,4,6))  # long hair
    d.line([bx-40,by-100,bx-230,by+60],fill=(14,12,10),width=8); d.line([bx+30,by-100,bx+200,by+60],fill=(14,12,10),width=8)  # oars
    d.ellipse([bx-14,by-196,bx-4,by-188],fill=(225,220,200)); d.ellipse([bx+10,by-196,bx+20,by-188],fill=(225,220,200))  # pale eyes looking back
    d.polygon([(0,1360),(560,1290),(620,1330),(640,BH),(0,BH)],fill=(36,34,32))  # stone jetty foreground
    for x in range(0,600,90): d.line([x,1360-x*0.12,x+30,BH],fill=(24,22,20),width=4)
    d.polygon([(0,1360),(560,1290),(570,1310),(0,1385)],fill=(60,58,54))
    d.rectangle([470,1180,540,1330],fill=(26,22,20)); d.ellipse([465,1165,545,1195],fill=(40,34,30))  # mooring post
    d.line([505,1230,560,1290,600,1360,640,1400],fill=(80,64,44),width=7); d.line([640,1400,660,1420],fill=(110,90,60),width=4)  # cut rope trailing in the water
    d=ImageDraw.Draw(im); _rain(d,90,13)
    d.polygon([(BW,BH),(BW,1450),(980,1500),(860,BH)],fill=(5,6,7))  # foreground rock right
    return noise_tex(im,8)
# ---------- Ep09: smart doorbell ----------
def _hoodie(d,x,y,s,col=(10,11,14),face=None,eyes=None,smile=False):
    """hooded person, head+shoulders; (x,y)=chin centre, s=scale (head width ~ 2*s*60)."""
    hw=60*s
    d.polygon([(x-hw*3.2,y+hw*4.2),(x-hw*2.6,y+hw*1.3),(x-hw*1.1,y+hw*0.5),(x+hw*1.1,y+hw*0.5),(x+hw*2.6,y+hw*1.3),(x+hw*3.2,y+hw*4.2)],fill=col)  # shoulders
    d.ellipse([x-hw*1.35,y-hw*2.6,x+hw*1.35,y+hw*0.7],fill=col)  # hood
    if face:
        d.ellipse([x-hw*0.85,y-hw*2.0,x+hw*0.85,y+hw*0.25],fill=face)
        sh=tuple(max(0,c-35) for c in face)
        d.chord([x-hw*0.85,y-hw*2.0,x+hw*0.85,y-hw*0.9],180,360,fill=sh)  # hood shadow on the forehead
        if eyes:
            for sx in (-1,1): d.ellipse([x+sx*hw*0.38-hw*0.16,y-hw*1.05-hw*0.09,x+sx*hw*0.38+hw*0.16,y-hw*1.05+hw*0.09],fill=eyes)
        else:
            for sx in (-1,1): d.ellipse([x+sx*hw*0.38-hw*0.14,y-hw*1.05-hw*0.07,x+sx*hw*0.38+hw*0.14,y-hw*1.05+hw*0.07],fill=sh)
        if smile: d.arc([x-hw*0.5,y-hw*0.75,x+hw*0.5,y-hw*0.05],15,165,fill=(20,24,26),width=max(3,int(hw*0.09)))
        d.line([x,y-hw*0.95,x-hw*0.08,y-hw*0.55],fill=sh,width=max(2,int(hw*0.05)))  # nose
    for sx in (-1,1): d.line([x+sx*hw*0.45,y+hw*0.6,x+sx*hw*0.55,y+hw*1.9],fill=(40,42,48),width=max(3,int(hw*0.07)))  # hoodie strings
def _ringfeed(mode):  # fisheye doorbell camera picture, IR black-and-white with a cyan tint, size 640x880
    sw,sh=640,880; im=Image.new('RGB',(sw,sh),(30,36,40)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,sw,sh*0.5],fill=(14,18,22))  # night sky / street
    for k in range(3): d.rectangle([60+k*190,170,150+k*190,330],fill=(24,30,34))  # houses across the street
    d.ellipse([500,90,540,130],fill=(120,135,140))  # streetlight
    d.polygon([(0,sh*0.5),(sw,sh*0.5),(sw,sh),(0,sh)],fill=(46,54,58))  # porch floor
    for k in range(1,8): d.line([0,sh*0.5+k*k*7,sw,sh*0.5+k*k*7],fill=(38,44,48),width=3)  # boards
    d.rectangle([0,0,70,sh],fill=(22,26,30)); d.rectangle([sw-70,0,sw,sh],fill=(22,26,30))  # porch posts
    d.rounded_rectangle([200,sh-150,440,sh-40],10,fill=(60,52,40)); d.text((320,sh-95),'WELCOME',font=F(B,30),fill=(90,80,62),anchor='mm')  # doormat
    if mode=='far':
        _hoodie(d,330,470,0.75,(8,10,12),face=(96,104,106))
        d.polygon([(330-150,470+190),(330+150,470+190),(330+120,sh-60),(330-120,sh-60)],fill=(8,10,12))  # body
        d.rectangle([330-110,sh-60,330-30,sh-40],fill=(6,8,10)); d.rectangle([330+30,sh-60,330+110,sh-40],fill=(6,8,10))
    elif mode=='close':
        _hoodie(d,320,560,2.0,(8,10,12),face=(92,100,102),eyes=(240,255,255),smile=True)
    im=im.filter(ImageFilter.GaussianBlur(1.2))
    # fisheye: bulge the picture towards the centre
    a=np.asarray(im,dtype=np.float32); yy,xx=np.mgrid[0:sh,0:sw].astype(np.float32)
    nx=(xx-sw/2)/(sw/2); ny=(yy-sh/2)/(sh/2); r=np.sqrt(nx*nx+ny*ny)+1e-6; k=np.clip(r**1.35/r,0,2)
    srcx=np.clip(sw/2+nx*k*0.92*sw/2,0,sw-1).astype(int); srcy=np.clip(sh/2+ny*k*0.92*sh/2,0,sh-1).astype(int)
    a=a[srcy,srcx]
    v=np.clip(1-0.55*(nx*nx*0.8+ny*ny*0.5),0.2,1)[...,None]; a=a*v
    a[::3]*=0.85; a+=np.random.default_rng(9).normal(0,9,a.shape[:2])[...,None]
    a=a*np.array([0.85,1.0,1.08])
    im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im)
    d.text((24,22),'FRONT DOOR',font=F(M,30),fill=(220,240,245)); d.ellipse([sw-130,28,sw-108,50],fill=(230,40,30)); d.text((sw-100,22),'LIVE',font=F(M,30),fill=(230,240,245))
    d.text((24,sh-50),'03:12:44 AM',font=F(M,30),fill=(220,240,245))
    return im
def ring_phone(mode='far'):  # phone held in a dark bedroom showing the doorbell app; mode notify = lock screen notification
    im=base((5,7,12),(10,9,12)); d=ImageDraw.Draw(im)
    d.rectangle([80,300,420,760],fill=(14,20,34)); im=moon(im,300,430,40); d=ImageDraw.Draw(im)  # window
    d.line([250,300,250,760],fill=(5,5,8),width=12); d.line([80,530,420,530],fill=(5,5,8),width=12)
    for x in (60,440): d.polygon([(x-30,270),(x+30,270),(x+50,960),(x-40,960)],fill=(10,9,13))  # curtains
    d.rectangle([760,380,1060,640],fill=(16,14,16)); d.rectangle([775,395,1045,625],fill=(24,24,30))  # picture frame
    d.rectangle([0,1120,BW,1135],fill=(22,20,24))
    vgrad(d,(0,1135,BW,BH),(26,24,32),(10,9,12))
    for k in range(6): d.arc([-200+k*60,1350+k*70,BW+200-k*60,2300],195,345,fill=(34,32,42),width=10)  # blanket folds
    im=cone(im,(250,530),(150,1500),(650,1500),(60,80,130),0.18,40); d=ImageDraw.Draw(im)
    px,py=cx,980; pw,ph=380,760
    d.rounded_rectangle([px-pw-14,py-ph-14,px+pw+14,py+ph+14],70,fill=(8,8,10)); d.rounded_rectangle([px-pw,py-ph,px+pw,py+ph],60,fill=(16,18,22))
    if mode=='notify':
        scr=Image.new('RGB',(2*pw-40,2*ph-60),(10,14,24)); sd=ImageDraw.Draw(scr); sw_,sh_=scr.size
        for k in range(40): sd.line([0,k*sh_/40,sw_,k*sh_/40+60],fill=(12+k//3,16+k//4,30+k//2),width=int(sh_/40)+2)
        sd.text((sw_/2,250),'3:12',font=F(B,190),fill=(235,240,250),anchor='mm'); sd.text((sw_/2,390),'Wednesday, November 11',font=F(B,34),fill=(190,200,215),anchor='mm')
        sd.rounded_rectangle([30,560,sw_-30,800],34,fill=(52,58,72))
        sd.rounded_rectangle([60,600,140,680],18,fill=(40,170,200)); sd.ellipse([82,622,118,658],outline=(240,250,255),width=6)
        sd.text((165,605),'DOORBELL',font=F(B,30),fill=(200,210,220)); sd.text((sw_-60,605),'now',font=F(B,28),fill=(170,180,195),anchor='ra')
        sd.text((165,655),'Front Door',font=F(B,40),fill=(245,248,252)); sd.text((60,720),'Someone is at your door.',font=F(B,36),fill=(225,230,238))
        im.paste(scr,(px-pw+20,py-ph+30)); im=glow(im,(px,py),520,(50,110,160),0.45); im.paste(scr,(px-pw+20,py-ph+30))
    else:
        im.paste(Image.new('RGB',(2*pw-40,2*ph-60),(14,16,20)),(px-pw+20,py-ph+30))
        feed=_ringfeed(mode).resize((2*pw-40,int((2*pw-40)*880/640))); im.paste(feed,(px-pw+20,py-ph+90))
        im=glow(im,(px,py),540,(60,130,150),0.5); im.paste(feed,(px-pw+20,py-ph+90)); d=ImageDraw.Draw(im)
        by=py+ph-190
        for k,lab in enumerate(('TALK','SIREN','UNLOCK')):
            bx=px-240+k*240; d.ellipse([bx-55,by-55,bx+55,by+55],fill=(34,40,48))
            d.ellipse([bx-20,by-20,bx+20,by+20],fill=(60,200,220) if lab!='SIREN' else (220,60,50))
    d=ImageDraw.Draw(im); d.rounded_rectangle([px-90,py-ph+8,px+90,py-ph+40],16,fill=(4,4,6))  # notch
    d.line([px-pw+60,py-ph+120,px-pw+260,py-ph+600],fill=(70,90,100),width=4)  # glare
    # hands holding the phone (dark, lit from the screen)
    for s in (-1,1):
        hx=px+s*(pw+10)
        d.polygon([(hx,py+80),(hx+s*70,py+40),(hx+s*150,py+500),(hx+s*120,BH),(hx-s*60,BH),(hx-s*30,py+560)],fill=(34,28,28))
        for f in range(3): d.rounded_rectangle([min(hx,hx-s*70),py+130+f*95,max(hx,hx-s*70),py+190+f*95],26,fill=(46,38,36))
    return noise_tex(im,7)
def keypad():  # close-up: smart lock keypad on the front door at night, a pale finger pressing a key, 'UNLOCKED'
    im=base((10,8,8),(16,12,10)); d=ImageDraw.Draw(im)
    for x in range(0,BW,64): d.line([x+_R.normal(0,4),0,x,BH],fill=(22,16,13),width=6)  # wood grain
    d.rectangle([0,0,140,BH],fill=(30,30,34)); d.rectangle([140,0,170,BH],fill=(12,10,10))  # door frame + gap
    d.rectangle([980,0,BW,BH],fill=(40,34,30)); d.rectangle([1000,0,BW,BH],fill=(26,22,20))  # panel edge
    kx,ky=600,880
    d.rounded_rectangle([kx-230,ky-430,kx+230,ky+470],50,fill=(14,14,16)); d.rounded_rectangle([kx-210,ky-410,kx+210,ky+450],40,fill=(26,26,30))
    d.rounded_rectangle([kx-160,ky-370,kx+160,ky-250],18,fill=(10,30,18)); d.text((kx,ky-310),'UNLOCKED',font=F(M,46),fill=(110,255,150),anchor='mm')
    for r_ in range(4):
        for c_ in range(3):
            lab=['1','2','3','4','5','6','7','8','9','*','0','#'][r_*3+c_]; bx=kx-120+c_*120; by=ky-150+r_*130
            d.ellipse([bx-48,by-48,bx+48,by+48],fill=(36,38,42)); d.ellipse([bx-44,by-44,bx+44,by+44],outline=(80,200,120),width=3)
            d.text((bx,by),lab,font=F(B,44),fill=(170,240,190),anchor='mm')
    d.ellipse([kx-36,ky+370,kx+36,ky+442],fill=(20,20,22)); d.ellipse([kx-14,ky+392,kx+14,ky+420],fill=(110,255,150))
    im=glow(im,(kx,ky),420,(40,160,80),0.45); im=glow(im,(kx,ky-310),160,(80,255,130),0.4); d=ImageDraw.Draw(im)
    # handle below
    d.rounded_rectangle([kx-60,ky+520,kx+60,ky+640],30,fill=(60,56,50)); d.rounded_rectangle([kx-40,ky+600,kx+330,ky+660],28,fill=(86,80,70))
    # pale finger + hand coming from the right, pressing '6'
    fx,fy=kx+120,ky-20
    d.polygon([(fx-10,fy-30),(fx+40,fy-40),(BW+40,fy+60),(BW+40,fy+330),(fx+300,fy+260),(fx+20,fy+40)],fill=(118,122,118))
    d.ellipse([fx-34,fy-40,fx+34,fy+36],fill=(130,134,128)); d.ellipse([fx-20,fy-30,fx+14,fy+4],fill=(170,170,160))  # fingertip + nail
    d.polygon([(fx+140,fy+90),(fx+380,fy+120),(fx+390,fy+170),(fx+150,fy+150)],fill=(98,102,98))  # knuckle shadow
    d.polygon([(fx+380,fy-10),(BW+40,fy-60),(BW+40,fy+360),(fx+420,fy+300)],fill=(14,14,18))  # dark hoodie sleeve
    im=cone(im,(kx,ky),(kx-500,1700),(kx+500,1700),(40,140,70),0.15,60)
    d=ImageDraw.Draw(im); d.polygon([(0,BH),(0,1720),(260,1800),(360,BH)],fill=(6,6,8))
    return noise_tex(im,8)
def slats():  # view from inside a closet through the slats: a hooded man standing right outside in my bedroom
    im=base((10,12,20),(14,13,16)); d=ImageDraw.Draw(im)
    d.rectangle([700,360,1050,820],fill=(22,32,52)); im=moon(im,930,480,45); d=ImageDraw.Draw(im)  # window
    d.line([875,360,875,820],fill=(6,6,8),width=12); d.line([700,590,1050,590],fill=(6,6,8),width=12)
    d.rounded_rectangle([80,1080,560,1420],24,fill=(40,34,42)); d.rounded_rectangle([60,960,180,1420],24,fill=(46,40,48))  # bed
    d.rounded_rectangle([200,1040,420,1120],26,fill=(120,120,138)); d.polygon([(180,1180),(560,1140),(560,1420),(180,1420)],fill=(56,50,66))
    d.rectangle([0,1420,BW,BH],fill=(20,17,18))
    d.rounded_rectangle([1000,1380,1180,1700],10,fill=(26,22,24)); d.rectangle([1010,1300,1050,1380],fill=(30,26,28))  # lamp (off)
    im=cone(im,(875,590),(560,1600),(1150,1600),(70,90,140),0.25,40); d=ImageDraw.Draw(im)
    # the man: hooded, standing close, face lit by the moon, staring at the slats
    _hoodie(d,620,820,1.5,(8,9,12),face=(105,112,124),eyes=(235,245,250))
    d.polygon([(620-280,820+250),(620+280,820+250),(620+240,1800),(620-240,1800)],fill=(8,9,12))
    d.polygon([(620+250,1000),(620+330,1020),(620+300,1500),(620+240,1500)],fill=(8,9,12))  # arm, hand reaching to the door
    im=glow(im,(620,760),160,(60,70,100),0.2); d=ImageDraw.Draw(im)
    # foreground slats (inside the closet: very dark), with narrow gaps
    for y in range(0,BH,76): d.polygon([(0,y),(BW,y),(BW,y+34),(0,y+38)],fill=(6,5,6))
    d.rectangle([0,0,90,BH],fill=(4,4,5)); d.rectangle([BW-90,0,BW,BH],fill=(4,4,5))
    d.rectangle([590,0,620,BH],fill=(3,3,4))  # centre seam between the two closet doors
    for k in range(5): x=150+k*30; d.line([x,200,x+20,1500],fill=(8,7,8),width=10)  # hanging clothes edge
    return noise_tex(im,7)
def porch():  # outside a house at night: me (hooded) at my own front door, ringing; doorbell ring glowing; a figure behind the curtain inside
    im=base((6,9,20),(14,14,22)); d=ImageDraw.Draw(im); stars(d,60,500,21)
    im=moon(im,980,360,45); d=ImageDraw.Draw(im)
    for x,h in ((40,560),(1160,620)): pine(d,x,1180,h,150,(6,9,12))
    d.rectangle([150,560,1060,1260],fill=(30,30,36)); d.polygon([(100,580),(cx,330),(1110,580)],fill=(18,18,24))  # house + roof
    for y in range(600,1260,42): d.line([150,y,1060,y],fill=(36,36,42),width=4)  # siding
    d.rectangle([200,700,420,960],fill=(16,16,20)); d.rectangle([215,715,405,945],fill=(70,58,40))  # left window (warm, curtain)
    d.polygon([(215,715),(300,715),(280,945),(215,945)],fill=(50,40,28))
    d.ellipse([320,770,370,825],fill=(12,10,10)); d.rectangle([318,820,372,945],fill=(12,10,10))  # someone watching from inside
    d.rectangle([800,700,1010,960],fill=(16,16,20)); d.rectangle([815,715,995,945],fill=(20,22,30))
    d.rectangle([520,760,700,1250],fill=(16,14,14)); d.rectangle([535,775,685,1250],fill=(52,36,26))  # front door
    for yy in (800,1020): d.rectangle([555,yy,665,yy+190],outline=(40,28,20),width=6)
    d.ellipse([650,1000,672,1022],fill=(150,130,80))
    d.rounded_rectangle([716,960,746,1030],10,fill=(20,20,24)); d.ellipse([721,985,741,1005],outline=(80,220,255),width=5)  # doorbell
    im=glow(im,(731,995),60,(60,200,255),0.8); im=glow(im,(610,720),200,(200,160,90),0.5); d=ImageDraw.Draw(im)
    d.rounded_rectangle([590,700,630,740],8,fill=(255,220,150))  # porch light
    d.rectangle([380,1250,840,1290],fill=(40,36,34)); d.rectangle([340,1290,880,1330],fill=(34,30,30)); d.rectangle([300,1330,920,1370],fill=(28,26,26))  # steps
    im=cone(im,(610,720),(360,1300),(860,1300),(200,160,100),0.22,40); d=ImageDraw.Draw(im)
    vgrad(d,(0,1370,BW,BH),(18,20,22),(8,9,10)); d.polygon([(450,1370),(770,1370),(980,BH),(240,BH)],fill=(30,30,32))  # path
    # me, seen from behind, hood up, arm raised to the doorbell
    x,y=640,1310
    d.ellipse([x-55,y-430,x+55,y-310],fill=(8,8,10)); d.polygon([(x-90,y-330),(x+90,y-330),(x+110,y-110),(x+80,y),(x-80,y),(x-110,y-110)],fill=(8,8,10))
    d.polygon([(x+70,y-310),(x+100,y-290),(x+90,y-320),(x+86,y-325)],fill=(8,8,10)); d.line([x+80,y-300,x+90,y-320],fill=(8,8,10),width=26)
    d.line([x+85,y-305,x+716-640+5,995-1310+y+5],fill=(8,8,10),width=26)  # arm to the doorbell
    d.polygon([(0,BH),(0,1600),(200,1680),(300,BH)],fill=(4,5,7)); d.polygon([(BW,BH),(BW,1560),(1000,1660),(900,BH)],fill=(4,5,7))  # foreground bushes
    return noise_tex(im,7)
def _hand_writing(d,x,y,text,size,col):  # slightly wobbly handwritten-looking line (letters jittered)
    f=F(B,size); xx=x
    for k,ch in enumerate(text):
        d.text((xx,y+math.sin(k*1.7)*2),ch,font=f,fill=col); xx+=d.textlength(ch,font=f)
def bnb_house():  # rental house at night: lockbox on the door, porch light, and a small basement window glowing red at ground level
    im=base((6,8,18),(14,13,20)); d=ImageDraw.Draw(im); stars(d,70,520,33)
    im=moon(im,240,380,50); d=ImageDraw.Draw(im)
    for x,h in ((60,620),(1150,680),(1030,480)): pine(d,x,1230,h,150,(6,9,12))
    d.polygon([(110,700),(cx,400),(1100,700)],fill=(20,18,24)); d.polygon([(110,700),(cx,400),(cx,430),(150,700)],fill=(28,26,32))  # roof
    d.rectangle([170,700,1040,1300],fill=(34,32,38))
    for y in range(720,1300,40): d.line([170,y,1040,y],fill=(40,38,44),width=4)  # siding
    d.rectangle([540,520,670,640],fill=(14,14,18)); d.rectangle([552,532,658,628],fill=(24,26,34))  # attic window
    for wx in (230,800):
        d.rectangle([wx,780,wx+180,1000],fill=(14,14,18)); d.rectangle([wx+12,792,wx+168,988],fill=(20,22,30))
        d.line([wx+90,792,wx+90,988],fill=(12,12,16),width=8); d.line([wx+12,890,wx+168,890],fill=(12,12,16),width=8)
        d.rectangle([wx-20,770,wx+200,790],fill=(28,26,30)); d.rectangle([wx-14,1000,wx+194,1016],fill=(28,26,30))
    d.rectangle([520,820,690,1240],fill=(14,12,12)); d.rectangle([534,834,676,1240],fill=(58,30,24))  # red front door
    for yy in (870,1060): d.rectangle([552,yy,658,yy+150],outline=(40,20,16),width=6)
    d.ellipse([650,1040,670,1060],fill=(170,150,90))
    d.rounded_rectangle([700,1000,744,1070],6,fill=(20,20,22)); d.rectangle([708,1010,736,1040],fill=(70,72,76))  # key lockbox
    d.ellipse([716,1046,728,1058],fill=(150,150,150))
    d.rounded_rectangle([590,770,620,800],8,fill=(255,215,150))  # porch light
    im=glow(im,(605,790),190,(200,150,80),0.55); im=cone(im,(605,790),(380,1320),(830,1320),(200,150,90),0.22,40); d=ImageDraw.Draw(im)
    d.rectangle([420,1240,790,1275],fill=(42,38,36)); d.rectangle([380,1275,830,1310],fill=(34,30,30))  # steps
    d.rectangle([170,1300,1040,1345],fill=(26,24,26))  # foundation
    d.rectangle([860,1304,980,1340],fill=(12,6,6)); d.rectangle([866,1308,974,1336],fill=(150,30,22))  # basement window, glowing red
    d.line([920,1308,920,1336],fill=(30,8,8),width=5)
    im=glow(im,(920,1322),110,(190,30,20),0.7); d=ImageDraw.Draw(im)
    d.ellipse([890,1312,906,1330],fill=(20,6,6))  # a shape behind the basement glass
    vgrad(d,(0,1345,BW,BH),(16,18,20),(7,8,9)); d.polygon([(470,1345),(740,1345),(900,BH),(320,BH)],fill=(28,28,30))  # path
    d.rectangle([0,1345,BW,1352],fill=(22,24,22))
    for k in range(40): gx=_R.random()*BW; gy=1360+_R.random()*500; d.line([gx,gy,gx+_R.normal(0,4),gy-14-_R.random()*14],fill=(14,18,14),width=3)  # grass
    # foreground: rental car edge + suitcase handle, lower right; mailbox lower left
    d.polygon([(BW,BH),(BW,1620),(1060,1640),(940,1760),(880,BH)],fill=(5,6,8)); d.line([1000,1700,1150,1680],fill=(40,44,52),width=5)
    d.rectangle([60,1450,90,1900],fill=(5,5,7)); d.rounded_rectangle([10,1380,170,1470],30,fill=(6,6,8))
    return noise_tex(im,7)
def bnb_rules(red=False):  # handwritten HOUSE RULES note on a fridge under a dim pendant light; bottom torn off; red = rule 2 circled
    im=base((12,12,14),(18,16,16)); d=ImageDraw.Draw(im)
    for y in range(0,BH,120):  # kitchen wall tiles left side
        for x in range(0,170,120): d.rectangle([x+4,y+4,x+116,y+116],outline=(22,22,24),width=4)
    d.rectangle([150,200,1150,BH],fill=(30,32,34)); d.rectangle([170,200,1130,BH],fill=(40,42,44))  # fridge
    vgrad(d,(170,200,1130,BH),(46,48,50),(28,30,32))
    d.line([170,760,1130,760],fill=(20,20,22),width=10)  # freezer seam
    d.rounded_rectangle([1050,300,1090,700],18,fill=(70,72,74)); d.rounded_rectangle([1050,840,1090,1500],18,fill=(70,72,74))  # handles
    # other fridge stuff: takeaway menu, wifi card, magnets
    d.polygon([(230,300),(470,280),(480,620),(240,640)],fill=(120,110,90)); d.text((350,360),'PIZZA',font=F(B,40),fill=(110,30,24),anchor='mm')
    for k in range(6): d.line([260,430+k*30,450,425+k*30],fill=(90,82,66),width=5)
    d.rounded_rectangle([760,330,980,500],10,fill=(150,150,150)); d.text((870,380),'WIFI',font=F(B,36),fill=(40,40,44),anchor='mm'); d.text((870,440),'guest3am',font=F(M,30),fill=(50,50,54),anchor='mm')
    for mx,my,mc in ((350,285,(160,40,30)),(870,320,(40,90,150)),(300,1720,(50,120,60))): d.ellipse([mx-22,my-22,mx+22,my+22],fill=mc)
    # the note
    nx0,ny0,nx1,ny1=270,860,960,1640
    d.polygon([(nx0+10,ny0+16),(nx1+10,ny0+6),(nx1+16,ny1+10),(nx0+16,ny1+20)],fill=(18,18,20))  # shadow
    pts=[(nx0,ny0+10),(nx1,ny0)]
    for k in range(13): pts.append((nx1-k*(nx1-nx0)/12,ny1+(18 if k%2 else -6)+_R.normal(0,4)))  # torn bottom edge
    d.polygon(pts,fill=(150,142,118))
    for k in range(8): d.line([nx0+20,ny0+140+k*62,nx1-20,ny0+132+k*62],fill=(170,180,200),width=2)  # ruled lines
    d.ellipse([cx-30,ny0-30,cx+30,ny0+30],fill=(170,30,24)); d.ellipse([cx-12,ny0-18,cx+4,ny0-6],fill=(230,120,100))  # red magnet
    ink=(12,10,22)
    _hand_writing(d,nx0+150,ny0+60,'HOUSE RULES',56,ink); d.line([nx0+150,ny0+130,nx0+520,ny0+126],fill=ink,width=5)
    _hand_writing(d,nx0+40,ny0+190,'1. Never open the',44,ink); _hand_writing(d,nx0+90,ny0+250,'basement door.',44,ink)
    _hand_writing(d,nx0+40,ny0+350,'2. This house has',44,ink); _hand_writing(d,nx0+90,ny0+410,'no basement.',44,ink)
    _hand_writing(d,nx0+40,ny0+520,'3. If it kno',44,ink)  # torn off mid-word
    if red:
        d.ellipse([nx0+10,ny0+325,nx1-40,ny0+490],outline=(170,14,10),width=10); d.line([nx0+90,ny0+472,nx0+420,ny0+468],fill=(170,14,10),width=7)
    im=glow(im,(600,180),200,(200,170,110),0.35)
    im=cone(im,(600,120),(150,1900),(1050,1900),(200,170,110),0.08,60)
    if red: im=glow(im,(560,1290),300,(170,20,15),0.35)
    d=ImageDraw.Draw(im)
    d.rectangle([560,0,640,120],fill=(10,10,10)); d.polygon([(470,120),(730,120),(680,40),(520,40)],fill=(22,20,18))  # pendant lamp
    d.ellipse([570,105,630,135],fill=(255,225,170))
    d.polygon([(0,BH),(0,1750),(240,1800),(320,BH)],fill=(5,5,6))  # foreground counter edge
    return noise_tex(im,7)
def bnb_door(mode='knock'):  # basement door in a narrow hallway: chain, three deadbolts, 'DO NOT OPEN'; light seeping under it.
    # mode knock = shadows of feet under the door + knock rings; mode turn = knob turning, bolts unlocked (red), pale fingers reaching out under the door
    turn=(mode=='turn')
    im=base((12,10,10),(18,14,12)); d=ImageDraw.Draw(im)
    for x in range(0,BW,56): d.line([x,0,x,1620],fill=(22,17,14),width=4)  # old wallpaper stripes
    for k in range(30): px_=_R.random()*BW; py_=300+_R.random()*1200; d.ellipse([px_,py_,px_+5,py_+5],fill=(26,20,16))
    d.rectangle([0,1620,BW,BH],fill=(26,20,16))
    for k in range(12): d.line([0,1620+k*48,BW,1620+k*48],fill=(34,26,20),width=3)  # floorboards
    d.rectangle([310,380,900,1630],fill=(28,20,16))  # frame
    dx0,dy0,dx1,dy1=340,410,870,1620
    d.rectangle([dx0,dy0,dx1,dy1],fill=(56,38,28))
    x0=dx0+40; pw=dx1-x0-40
    d.rectangle([x0,dy0+50,x0+pw,dy0+550],outline=(40,26,18),width=12); d.rectangle([x0,dy0+610,x0+pw,dy0+1160],outline=(40,26,18),width=12)
    px0=dx0+150  # the 'DO NOT OPEN' paper taped on
    d.polygon([(px0,dy0+160),(px0+300,dy0+150),(px0+306,dy0+330),(px0+6,dy0+340)],fill=(196,186,160))
    _hand_writing(d,px0+34,dy0+190,'DO NOT',50,(150,24,18)); _hand_writing(d,px0+44,dy0+255,'OPEN',58,(150,24,18))
    for tx,ty in ((px0-10,dy0+150),(px0+280,dy0+140)): d.rectangle([tx,ty,tx+40,ty+18],fill=(170,165,140))
    for k in range(3):  # deadbolts (turned red when unlocked from the other side)
        by=dy0+420+k*190; d.rounded_rectangle([dx1-110,by,dx1-30,by+70],10,fill=(110,100,80))
        if turn: d.rectangle([dx1-74,by+12,dx1-66,by+58],fill=(40,30,24)); d.ellipse([dx1-46,by+24,dx1-34,by+36],fill=(255,60,40))
        else: d.ellipse([dx1-84,by+20,dx1-56,by+50],fill=(40,36,30))
    kx,ky=dx1-126,dy0+784
    d.ellipse([kx-26,ky-26,kx+26,ky+26],fill=(160,130,70)); d.ellipse([kx-14,ky-18,kx-2,ky-6],fill=(220,200,140))  # knob
    if turn:
        d.ellipse([kx-8,ky-8,kx+8,ky+8],fill=(90,70,40))
        for r in (50,72):  d.arc([kx-r,ky-r,kx+r,ky+r],200,320,fill=(230,210,170),width=6)  # turning motion
        d.polygon([(kx+60,ky-40),(kx+86,ky-60),(kx+80,ky-24)],fill=(230,210,170))
        for k in range(9): t=k/8; lx=dx1-40-t*20; ly=dy0+1000+t*200; d.ellipse([lx-9,ly-6,lx+9,ly+6],outline=(150,140,110),width=4)  # chain hanging loose
    else:
        for k in range(9): t=k/8; lx=dx1-60-t*120; ly=dy0+1000+math.sin(t*math.pi)*70; d.ellipse([lx-9,ly-6,lx+9,ly+6],outline=(150,140,110),width=4)
    lc=(190,40,24)
    d.rectangle([dx0,dy1-12,dx1,dy1+4],fill=(230,80,50) if not turn else (255,110,70))
    if turn:
        im=glow(im,(cx,dy1),360,lc,0.75); d=ImageDraw.Draw(im)
        for k,fx in enumerate((440,480,520,560,700,740,780)):  # long pale fingers sliding out under the door
            ln=60+((k*37)%50); d.rounded_rectangle([fx-13,dy1-4,fx+13,dy1+ln],12,fill=(160,156,146)); d.ellipse([fx-9,dy1+ln-18,fx+9,dy1+ln-4],fill=(200,196,186))
        im=glow(im,(kx,ky),110,(220,190,120),0.45)
    else:
        for k in range(2): d.rectangle([470+k*190,dy1-14,540+k*190,dy1+6],fill=(10,4,3))  # feet shadows
        im=glow(im,(cx,dy1),300,lc,0.55); d=ImageDraw.Draw(im)
        for r in (60,100,140):  # knock rings
            d.arc([cx-r-40,dy0+700-r,cx+r-40,dy0+700+r],200,250,fill=(200,180,150),width=5); d.arc([cx-r-40,dy0+700-r,cx+r-40,dy0+700+r],290,340,fill=(200,180,150),width=5)
    d=ImageDraw.Draw(im)  # hallway: light switch, framed photo, small table with a lamp
    d.rounded_rectangle([960,900,1010,980],8,fill=(150,140,120)); d.rectangle([978,925,992,955],fill=(90,84,72))
    d.rectangle([60,620,250,860],fill=(36,28,22)); d.rectangle([76,636,234,844],fill=(60,58,54)); d.ellipse([125,680,185,750],fill=(40,38,36))
    d.rectangle([980,1300,1190,1330],fill=(30,22,16)); d.rectangle([1000,1330,1020,1620],fill=(24,18,12)); d.rectangle([1150,1330,1170,1620],fill=(24,18,12))
    d.polygon([(1030,1180),(1150,1180),(1120,1100),(1060,1100)],fill=(110,90,60)); d.rectangle([1085,1180,1095,1300],fill=(60,50,40))
    im=glow(im,(1090,1150),150,(200,150,90),0.4)
    im=cone(im,(1090,1170),(700,1700),(1209,1700),(180,130,80),0.15,40); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(130,0),(150,BH),(0,BH)],fill=(6,5,5))  # foreground wall edge
    return noise_tex(im,7)
def bnb_stairs(mode='down'):  # narrow basement stairway seen from the top: wooden steps, bare bulb, red light below.
    # mode down = empty, red glow at the bottom; woman = a pale woman sitting at the bottom with a suitcase, looking up;
    # up = looking up the stairs from the bottom: the basement door shut at the top, light line under it, three red bolt lights
    up=(mode=='up')
    im=base((10,6,6),(16,8,8)); d=ImageDraw.Draw(im)
    vx,vy=cx,820  # far end of the stairway
    fw,nw=150,560  # half widths: far end / near end
    # side walls (old brick left, wood panelling right)
    d.polygon([(0,0),(vx-fw,vy-360),(vx-fw,vy+120),(0,BH)],fill=(30,20,18))
    d.polygon([(BW,0),(vx+fw,vy-360),(vx+fw,vy+120),(BW,BH)],fill=(26,18,14))
    for k in range(18):  # brick courses on the left wall
        t=k/18; y0=t*BH; y1=vy-360+t*480
        d.line([0,y0,vx-fw,y1],fill=(22,14,12),width=4)
    for k in range(10):  # vertical panel seams on the right wall
        t=k/10; xa=BW-t*(BW-(vx+fw)); d.line([xa,0+t*(vy-360),xa,BH-t*(BH-vy-120)],fill=(18,12,10),width=5)
    d.polygon([(0,0),(BW,0),(vx+fw,vy-360),(vx-fw,vy-360)],fill=(12,8,8))  # low ceiling
    for k in range(5): t=k/5; yy=t*(vy-360); d.line([t*(vx-fw),yy,BW-t*(BW-vx-fw),yy],fill=(20,14,12),width=8)  # joists
    # far end
    if up:
        d.rectangle([vx-fw,vy-360,vx+fw,vy+120],fill=(20,14,12)); d.rectangle([vx-fw+16,vy-340,vx+fw-16,vy+110],fill=(56,38,28))
        d.rectangle([vx-fw+30,vy-310,vx+fw-30,vy-120],outline=(40,26,18),width=6)
        for k in range(3): by=vy-200+k*70; d.ellipse([vx+fw-52,by,vx+fw-36,by+16],fill=(255,50,30))
        d.rectangle([vx-fw+16,vy+104,vx+fw-16,vy+116],fill=(255,200,140))
        im=glow(im,(vx,vy+110),140,(220,160,100),0.6); d=ImageDraw.Draw(im)
        for x_ in (vx-50,vx+20): d.rectangle([x_,vy+102,x_+36,vy+118],fill=(14,8,6))  # her feet, on the other side
        for k in range(3): by=vy-200+k*70; im=glow(im,(vx+fw-44,by+8),30,(255,40,20),0.6)
        d=ImageDraw.Draw(im)
    else:
        d.rectangle([vx-fw,vy-360,vx+fw,vy+120],fill=(150,26,18))
        d.rectangle([vx-fw,vy+60,vx+fw,vy+120],fill=(110,20,14))  # basement floor
        d.rectangle([vx-fw+20,vy-300,vx-fw+70,vy+60],fill=(60,12,10)); d.rectangle([vx+fw-60,vy-260,vx+fw-20,vy+60],fill=(70,14,10))  # boxes / pipe
        im=glow(im,(vx,vy-100),300,(200,30,20),0.75); d=ImageDraw.Draw(im)
    # steps from near (bottom of frame) to far
    n=11
    for k in range(n):
        t0=k/n; t1=(k+1)/n
        def pt(t):
            tt=t**0.8; return vy+120+(BH+200-(vy+120))*(1-tt), fw+(nw-fw)*(1-tt)
        y0,w0=pt(1-t0); y1,w1=pt(1-t1)
        tread=(48,34,26) if not up else (42,30,24); riser=(26,18,14)
        d.polygon([(vx-w0,y0),(vx+w0,y0),(vx+w1,y1),(vx-w1,y1)],fill=riser)
        ym=y1+(y0-y1)*0.45
        d.polygon([(vx-w0,y0),(vx+w0,y0),(vx+w0*0.98,ym),(vx-w0*0.98,ym)],fill=tread)
        d.line([vx-w0,y0,vx+w0,y0],fill=(70,52,40),width=4)
        if k%3==1: d.line([vx-w0*0.3,ym+8,vx-w0*0.1,y0-6],fill=(30,20,16),width=3)  # cracks
    # handrail on the right
    d.line([vx+fw-10,vy+40,BW-60,BH-60],fill=(40,28,20),width=22); d.line([vx+fw-10,vy+30,BW-60,BH-80],fill=(80,60,44),width=6)
    if mode=='woman':
        wx,wy=vx,vy+110
        d.rounded_rectangle([wx+30,wy-60,wx+110,wy],8,fill=(70,46,30)); d.rectangle([wx+55,wy-74,wx+85,wy-60],outline=(90,64,40),width=5)  # suitcase
        d.polygon([(wx+94,wy-56),(wx+120,wy-30),(wx+104,wy-24)],fill=(200,190,160))  # tag
        d.polygon([(wx-60,wy),(wx+30,wy),(wx+20,wy-110),(wx-50,wy-110)],fill=(8,6,6))  # body, sitting
        d.polygon([(wx-50,wy-110),(wx+20,wy-110),(wx+10,wy-130),(wx-40,wy-130)],fill=(10,8,8))
        d.ellipse([wx-42,wy-196,wx+6,wy-130],fill=(150,140,130))  # pale face, looking up
        d.polygon([(wx-48,wy-190),(wx+12,wy-190),(wx+18,wy-110),(wx-54,wy-110)],fill=(6,4,4))  # long dark hair
        d.ellipse([wx-34,wy-180,wx-2,wy-140],fill=(160,150,140))
        for ex in (wx-26,wx-12): d.ellipse([ex-4,wy-170,ex+4,wy-164],fill=(10,4,4))
        d.arc([wx-28,wy-160,wx-8,wy-148],10,170,fill=(60,20,20),width=2)  # faint smile
        im=glow(im,(wx-18,wy-160),60,(200,180,170),0.25); d=ImageDraw.Draw(im)
    # bare bulb at the top of frame on a cord
    d.line([cx-260,0,cx-260,330],fill=(10,8,8),width=4); d.ellipse([cx-282,320,cx-238,376],fill=(255,220,160))
    im=glow(im,(cx-260,350),180,(220,170,110),0.45)
    im=cone(im,(cx-260,350),(cx-640,BH),(cx+300,BH),(200,150,90),0.12,50); d=ImageDraw.Draw(im)
    # foreground: door frame edges at the top of the stairs (or bottom), my hand on the frame
    d.polygon([(0,0),(110,0),(140,BH),(0,BH)],fill=(6,4,4)); d.polygon([(BW,0),(BW-110,0),(BW-140,BH),(BW,BH)],fill=(6,4,4))
    if not up:
        d.rounded_rectangle([96,1020,190,1110],30,fill=(120,96,84))
        for f in range(4): d.rounded_rectangle([150,1030+f*20,232,1048+f*20],9,fill=(130,104,92))
    return noise_tex(im,7)
def bnb_tag():  # close-up: old paper luggage tag on a worn suitcase handle in red light, 'CHECKED IN 03/14/1998', pale fingers holding it
    im=base((16,6,6),(10,4,4)); d=ImageDraw.Draw(im)
    for y in range(0,BH,60): d.line([0,y,BW,y+30],fill=(22,10,9),width=3)  # concrete basement wall texture
    for k in range(40): px_=_R.random()*BW; py_=_R.random()*BH; d.ellipse([px_,py_,px_+8,py_+6],fill=(26,12,10))
    d.rectangle([0,1200,BW,BH],fill=(40,20,14))  # old suitcase body
    vgrad(d,(0,1200,BW,BH),(70,40,26),(30,16,12))
    d.line([0,1260,BW,1260],fill=(90,60,40),width=6); d.line([0,1290,BW,1290],fill=(26,14,10),width=4)
    for x in (120,1090): d.rounded_rectangle([x-40,1180,x+40,1320],10,fill=(120,100,60)); d.ellipse([x-10,1240,x+10,1260],fill=(50,40,24))  # brass latches
    d.rounded_rectangle([380,1060,840,1220],60,outline=(50,30,20),width=46)  # handle
    d.line([610,1080,610,700],fill=(170,160,130),width=6)  # string
    tx0,ty0,tx1,ty1=330,560,900,1060
    d.polygon([(tx0+16,ty0+26),(tx1+16,ty0+10),(tx1+24,ty1+20),(tx0+24,ty1+30)],fill=(10,4,4))
    d.polygon([(tx0+80,ty0),(tx1-60,ty0-10),(tx1,ty0+60),(tx1,ty1),(tx0,ty1+10),(tx0,ty0+70)],fill=(196,180,146))
    d.ellipse([600,ty0+30,640,ty0+70],fill=(120,40,30)); d.ellipse([608,ty0+38,632,ty0+62],fill=(30,10,8))
    ink=(30,20,40)
    d.text((615,ty0+130),'GUEST',font=F(B,52),fill=(120,30,24),anchor='mm')
    d.line([tx0+40,ty0+170,tx1-40,ty0+166],fill=(120,30,24),width=4)
    _hand_writing(d,tx0+50,ty0+210,'CHECKED IN',58,ink)
    _hand_writing(d,tx0+70,ty0+300,'03/14/1998',62,(150,20,16))
    _hand_writing(d,tx0+50,ty0+400,'CHECK OUT',44,ink); _hand_writing(d,tx0+340,ty0+400,'____',44,ink)
    for k in range(5): d.ellipse([tx0+60+k*90,ty1-40,tx0+80+k*90,ty1-26],fill=(150,130,100))  # water stains
    for k,(fx,fy) in enumerate(((290,820),(290,880),(296,940))):  # pale fingers on the left edge
        d.rounded_rectangle([fx-150,fy,fx+60,fy+46],22,fill=(170,164,154)); d.ellipse([fx+20,fy+6,fx+56,fy+40],fill=(196,190,180))
    d.polygon([(0,780),(150,800),(150,1010),(0,1060)],fill=(150,144,136))
    im=glow(im,(615,780),420,(190,30,20),0.4)
    im=glow(im,(900,200),260,(200,40,30),0.4); d=ImageDraw.Draw(im)
    d.polygon([(BW,0),(BW,560),(1000,420),(960,0)],fill=(6,3,3))  # foreground shadow upper right
    return noise_tex(im,7)
def bnb_text(mode='rule'):  # phone in a dark bedroom: chat with the host, 'Rule 3: Answer it. Or it comes up.'
    im=base((5,6,10),(10,8,10)); d=ImageDraw.Draw(im)
    d.rectangle([800,300,1120,720],fill=(14,18,30)); d.line([960,300,960,720],fill=(5,5,8),width=12); d.line([800,510,1120,510],fill=(5,5,8),width=12)
    for x in (780,1140): d.polygon([(x-30,270),(x+30,270),(x+50,960),(x-40,960)],fill=(10,9,13))
    d.rectangle([60,420,300,640],fill=(16,14,16)); d.rectangle([74,434,286,626],fill=(26,24,28))  # generic art print
    vgrad(d,(0,1135,BW,BH),(26,22,30),(10,9,12))
    for k in range(6): d.arc([-200+k*60,1350+k*70,BW+200-k*60,2300],195,345,fill=(34,30,40),width=10)
    px,py=cx,1080; pw,ph=380,740
    d.rounded_rectangle([px-pw-14,py-ph-14,px+pw+14,py+ph+14],70,fill=(8,8,10))
    sw_,sh_=2*pw-40,2*ph-60; scr=Image.new('RGB',(sw_,sh_),(14,14,18)); sd=ImageDraw.Draw(scr)
    sd.rectangle([0,0,sw_,170],fill=(26,26,32)); sd.ellipse([40,60,120,140],fill=(90,80,70)); sd.text((150,72),'Host',font=F(B,40),fill=(240,240,245)); sd.text((150,120),'online',font=F(B,26),fill=(110,220,140))
    sd.text((sw_/2,215),'3:06 AM',font=F(B,26),fill=(140,140,150),anchor='mm')
    def bub(y,txt,me):
        f=F(B,36); lines=txt.split('\n'); w=max(sd.textlength(l,font=f) for l in lines)+60; h=len(lines)*48+36
        x0=sw_-w-30 if me else 30
        sd.rounded_rectangle([x0,y,x0+w,y+h],30,fill=(40,110,220) if me else (50,50,58))
        for k,l in enumerate(lines): sd.text((x0+30,y+18+k*48),l,font=f,fill=(250,250,252))
        return y+h+24
    if mode=='checkout':
        y=bub(260,"I answered it.\nShe left. The door\nlocked behind her",True)
        y=bub(y,"Let me out",True)
        sd.text((sw_-40,y-14),'Read 3:19 AM',font=F(B,24),fill=(130,130,140),anchor='ra'); y+=30
        f=F(B,44); txt=["Thanks for answering.","Checkout is when","the next guest","answers."]
    else:
        y=bub(260,"Someone is knocking\non the basement door",True)
        y=bub(y,"You said there's\nno basement??",True)
        sd.text((sw_-40,y-14),'Read 3:06 AM',font=F(B,24),fill=(130,130,140),anchor='ra'); y+=30
        f=F(B,46); txt=["Rule 3:","Answer it.","Or it comes up."]
    bw_=max(sd.textlength(l,font=f) for l in txt)+70
    sd.rounded_rectangle([30,y,30+bw_,y+len(txt)*62+40],30,fill=(120,22,18))
    for k,l in enumerate(txt): sd.text((60,y+22+k*62),l,font=f,fill=(255,240,236))
    sd.rounded_rectangle([30,sh_-110,sw_-30,sh_-40],34,fill=(34,34,40)); sd.text((70,sh_-75),'Message',font=F(B,30),fill=(120,120,130),anchor='lm')
    im.paste(scr,(px-pw+20,py-ph+30)); im=glow(im,(px,py),520,(140,40,40),0.45); im.paste(scr,(px-pw+20,py-ph+30)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([px-90,py-ph+8,px+90,py-ph+40],16,fill=(4,4,6))
    for s in (-1,1):
        hx=px+s*(pw+10)
        d.polygon([(hx,py+80),(hx+s*70,py+40),(hx+s*150,py+500),(hx+s*120,BH),(hx-s*60,BH),(hx-s*30,py+560)],fill=(34,28,28))
        for f_ in range(3): d.rounded_rectangle([min(hx,hx-s*70),py+130+f_*95,max(hx,hx-s*70),py+190+f_*95],26,fill=(46,38,36))
    return noise_tex(im,7)
def _speaker(im,x,y,s,ring=(60,200,230)):  # generic cylinder smart speaker; (x,y)=bottom centre, s=scale
    w=110*s; h=260*s
    im=glow(im,(x,y-h),int(170*s),ring,0.55); d=ImageDraw.Draw(im)
    d.rectangle([x-w,y-h,x+w,y],fill=(22,24,30)); d.ellipse([x-w,y-h*0.06-w*0.25,x+w,y+w*0.25-h*0.06],fill=(22,24,30))
    for k in range(9):  # fabric mesh rows
        yy=y-h*0.12-k*h*0.085; d.arc([x-w,yy-w*0.22,x+w,yy+w*0.22],10,170,fill=(30,32,40),width=max(2,int(3*s)))
    d.rectangle([x-w,y-h*0.98,x-w*0.82,y-h*0.05],fill=(14,15,20))  # shading left edge
    d.rectangle([x+w*0.55,y-h*0.98,x+w,y-h*0.05],fill=(34,36,44))  # highlight right edge (lit from screen side)
    d.ellipse([x-w,y-h-w*0.25,x+w,y-h+w*0.25],fill=(30,32,40))  # top
    d.ellipse([x-w,y-h-w*0.25,x+w,y-h+w*0.25],outline=ring,width=max(4,int(12*s)))  # light ring
    d.ellipse([x-w*0.5,y-h-w*0.12,x+w*0.5,y-h+w*0.12],fill=(18,20,26))
    for b in (-1,1): d.ellipse([x+b*w*0.25-6*s,y-h-5*s,x+b*w*0.25+6*s,y-h+5*s],fill=(50,52,60))
    return im
def alexa(mode='whisper'):  # close-up: smart speaker glowing on a nightstand at 3 AM, bedroom and a closet door ajar behind it
    red=(mode=='red'); ring=(230,40,30) if red else (60,200,230)
    im=base((6,8,14),(10,9,12)); d=ImageDraw.Draw(im)
    for x in range(0,BW,110): d.line([x,0,x,1150],fill=(10,12,18),width=2)  # wallpaper stripes
    # closet far right behind, door ajar with a black gap
    d.rectangle([760,320,1150,1150],fill=(18,17,20)); d.rectangle([780,340,1130,1150],fill=(28,26,28))
    d.polygon([(900,350),(1120,330),(1120,1150),(900,1150)],fill=(34,31,32)); d.rectangle([884,350,904,1150],fill=(2,2,3))
    d.ellipse([918,740,936,758],fill=(90,80,60))  # knob
    if red:  # two pale eyes in the gap
        for ex in (889,899): d.ellipse([ex-4,640,ex+4,648],fill=(220,215,190))
    # window left with moon, curtains
    d.rectangle([60,330,420,760],fill=(14,20,34)); im=moon(im,280,450,38); d=ImageDraw.Draw(im)
    d.line([240,330,240,760],fill=(5,5,8),width=12); d.line([60,545,420,545],fill=(5,5,8),width=12)
    for x in (50,430): d.polygon([(x-30,300),(x+30,300),(x+50,1000),(x-40,1000)],fill=(12,10,14))
    im=cone(im,(240,545),(120,1150),(700,1150),(60,80,130),0.15,40); d=ImageDraw.Draw(im)
    d.rectangle([0,1150,BW,1160],fill=(20,18,22)); vgrad(d,(0,1160,BW,BH),(22,20,24),(8,7,9))
    # nightstand top (foreground, close)
    vgrad(d,(0,1180,BW,1260),(52,40,34),(40,30,26)); d.rectangle([0,1260,BW,BH],fill=(26,20,18))
    d.line([0,1182,BW,1182],fill=(80,64,52),width=4)
    for k in range(5): d.line([0,1300+k*90,BW,1300+k*90+20],fill=(32,25,22),width=5)  # wood grain on the drawer front
    d.rounded_rectangle([cx-120,1440,cx+120,1480],12,fill=(46,36,30))  # drawer handle
    # objects: lamp (off) left, glass of water, phone face down
    d.polygon([(150,860),(330,860),(380,1060),(100,1060)],fill=(40,36,38)); d.rectangle([228,1060,252,1200],fill=(30,28,30)); d.ellipse([170,1190,310,1225],fill=(30,28,30))
    d.rectangle([800,1080,880,1215],fill=(60,70,80)); d.rectangle([808,1110,872,1210],fill=(40,52,64))
    d.rounded_rectangle([890,1190,1080,1225],10,fill=(12,12,14))
    im=_speaker(im,cx-20,1215,1.35,ring); d=ImageDraw.Draw(im)
    for k in range(3):  # whisper sound waves
        r=200+k*70; d.arc([cx-20-r,1215-351-r*0.5,cx-20+r,1215-351+r*0.5],200,340,fill=tuple(int(c*(0.5-0.12*k)) for c in ring),width=6)
    im=cone(im,(cx-20,860),(cx-260,1215),(cx+220,1215),ring,0.18,30)
    d=ImageDraw.Draw(im); d.polygon([(0,BH),(0,1600),(140,1650),(260,BH)],fill=(6,5,6))  # foreground blanket edge
    return noise_tex(im,7)
def alexa_room():  # wide: me sitting up in bed in the dark, speaker glowing on the nightstand, closet door ajar across the room
    im=base((6,8,14),(10,9,12)); d=ImageDraw.Draw(im)
    for x in range(0,BW,110): d.line([x,0,x,1180],fill=(10,12,18),width=2)
    d.rectangle([70,330,430,780],fill=(14,20,34)); im=moon(im,300,460,40); d=ImageDraw.Draw(im)
    d.line([250,330,250,780],fill=(5,5,8),width=12); d.line([70,555,430,555],fill=(5,5,8),width=12)
    for x in (55,445): d.polygon([(x-30,300),(x+30,300),(x+50,1020),(x-40,1020)],fill=(12,10,14))
    # closet on the right wall, door ajar, black gap
    d.rectangle([700,360,1110,1180],fill=(18,17,20)); d.rectangle([720,380,1090,1180],fill=(30,27,28))
    d.polygon([(850,390),(1080,370),(1080,1180),(850,1180)],fill=(36,32,32)); d.rectangle([832,390,852,1180],fill=(2,2,3))
    d.ellipse([866,780,884,798],fill=(90,80,60))
    d.rectangle([520,420,660,560],fill=(20,18,22)); d.rectangle([532,432,648,548],fill=(30,30,36))  # picture frame
    d.rectangle([0,1180,BW,1192],fill=(22,20,24)); vgrad(d,(0,1192,BW,BH),(24,21,24),(9,8,10))
    for k in range(8): d.line([0,1250+k*k*9,BW,1250+k*k*9],fill=(18,16,18),width=3)  # floorboards
    im=cone(im,(250,555),(100,1500),(800,1500),(60,80,130),0.2,40); d=ImageDraw.Draw(im)
    # bed: headboard left, blanket
    d.rounded_rectangle([-40,1000,620,1220],30,fill=(30,26,30))  # headboard
    d.polygon([(-40,1200),(640,1200),(760,1640),(-40,1640)],fill=(44,40,54))
    for k in range(5): d.arc([-200+k*40,1260+k*60,760-k*20,1900],200,330,fill=(56,52,66),width=8)
    d.rounded_rectangle([60,1130,330,1230],30,fill=(150,150,165))  # pillow
    # me sitting up: silhouette
    d.ellipse([300,980,400,1100],fill=(16,14,16)); d.polygon([(260,1110),(440,1110),(480,1340),(230,1340)],fill=(18,16,20))
    d.line([440,1150,560,1250],fill=(18,16,20),width=34)  # arm reaching toward the nightstand
    # nightstand right of bed with speaker
    d.rectangle([560,1210,760,1420],fill=(36,28,24)); d.rectangle([550,1195,770,1215],fill=(50,40,32))
    d.rounded_rectangle([640,1290,680,1306],6,fill=(56,44,36))
    im=_speaker(im,660,1196,0.6); d=ImageDraw.Draw(im)
    im=cone(im,(660,1040),(420,1190),(900,1190),(60,200,230),0.15,30); d=ImageDraw.Draw(im)
    d.polygon([(BW-120,250),(BW,250),(BW,BH),(BW-170,BH)],fill=(5,5,7))  # doorframe foreground
    return noise_tex(im,7)
def voice_app(mode='list'):  # phone in a dark bedroom showing the speaker app's voice history; new = tonight's red entry; play = waveform playing
    im=base((5,6,10),(10,8,10)); d=ImageDraw.Draw(im)
    d.rectangle([820,300,1130,720],fill=(14,18,30)); d.line([975,300,975,720],fill=(5,5,8),width=12); d.line([820,510,1130,510],fill=(5,5,8),width=12)
    for x in (800,1150): d.polygon([(x-30,270),(x+30,270),(x+50,960),(x-40,960)],fill=(10,9,13))
    im=_speaker(im,170,1120,0.5,(60,200,230) if mode!='new' else (230,40,30)); d=ImageDraw.Draw(im)
    d.rectangle([20,1120,330,1135],fill=(40,32,28))
    vgrad(d,(0,1135,BW,BH),(26,22,30),(10,9,12))
    for k in range(6): d.arc([-200+k*60,1350+k*70,BW+200-k*60,2300],195,345,fill=(34,30,40),width=10)
    px,py=cx,1060; pw,ph=380,740
    d.rounded_rectangle([px-pw-14,py-ph-14,px+pw+14,py+ph+14],70,fill=(8,8,10))
    sw_,sh_=2*pw-40,2*ph-60; scr=Image.new('RGB',(sw_,sh_),(14,16,20)); sd=ImageDraw.Draw(scr)
    sd.rectangle([0,0,sw_,170],fill=(22,26,32)); sd.text((40,60),'<',font=F(B,46),fill=(80,200,230)); sd.text((sw_/2,85),'Voice History',font=F(B,44),fill=(240,242,246),anchor='mm')
    sd.text((40,200),'Bedroom Speaker',font=F(B,30),fill=(120,130,140))
    if mode=='play':
        sd.rounded_rectangle([30,260,sw_-30,1060],30,fill=(28,32,38))
        sd.text((70,300),'Today  3:00 AM',font=F(B,32),fill=(150,160,170)); sd.text((70,350),'User: Guest',font=F(B,40),fill=(240,242,246))
        sd.text((70,420),'"Alexa, tell me',font=F(B,46),fill=(250,250,252)); sd.text((70,480),"when he's asleep.\"",font=F(B,46),fill=(250,250,252))
        r=np.random.default_rng(4)
        for k in range(46):  # waveform
            x=70+k*13; a=(r.random()*0.8+0.2)*130*math.sin(k/46*math.pi)
            sd.rectangle([x,750-a,x+7,750+a],fill=(80,200,230) if k<28 else (70,76,86))
        sd.ellipse([sw_/2-60,920,sw_/2+60,1040],fill=(80,200,230)); sd.rectangle([sw_/2-22,955,sw_/2-8,1005],fill=(14,16,20)); sd.rectangle([sw_/2+8,955,sw_/2+22,1005],fill=(14,16,20))
        sd.text((sw_/2,1110),'Playing recording...',font=F(B,32),fill=(150,160,170),anchor='mm')
    else:
        y=260; rows=[("Nov 11","3:00 AM"),("Nov 10","3:00 AM"),("Nov 9","3:00 AM"),("Nov 8","3:00 AM"),("Nov 7","3:00 AM")]
        if mode=='new':
            sd.rounded_rectangle([30,y,sw_-30,y+300],26,fill=(120,22,18))
            sd.text((60,y+28),'Today  3:03 AM',font=F(B,30),fill=(255,210,200)); sd.text((sw_-60,y+28),'NEW',font=F(B,30),fill=(255,240,236),anchor='ra')
            sd.text((60,y+80),'User: Guest',font=F(B,38),fill=(255,240,236))
            sd.text((60,y+150),'"Tell him I\'m',font=F(B,46),fill=(255,250,248)); sd.text((60,y+210),'in the closet."',font=F(B,46),fill=(255,250,248))
            y+=330; rows=rows[:3]
        for dte,tm in rows:
            sd.rounded_rectangle([30,y,sw_-30,y+190],22,fill=(30,34,40))
            sd.text((60,y+24),f'{dte}  {tm}',font=F(B,28),fill=(140,150,160)); sd.text((sw_-60,y+24),'Guest',font=F(B,28),fill=(230,120,100),anchor='ra')
            sd.text((60,y+80),'"Alexa, tell me',font=F(B,36),fill=(225,228,232)); sd.text((60,y+126),"when he's asleep.\"",font=F(B,36),fill=(225,228,232))
            y+=212
    im.paste(scr,(px-pw+20,py-ph+30)); im=glow(im,(px,py),520,(140,40,40) if mode=='new' else (50,120,150),0.45); im.paste(scr,(px-pw+20,py-ph+30)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([px-90,py-ph+8,px+90,py-ph+40],16,fill=(4,4,6))
    d.line([px-pw+60,py-ph+120,px-pw+220,py-ph+520],fill=(60,70,80),width=4)
    for s in (-1,1):
        hx=px+s*(pw+10)
        d.polygon([(hx,py+80),(hx+s*70,py+40),(hx+s*150,py+500),(hx+s*120,BH),(hx-s*60,BH),(hx-s*30,py+560)],fill=(34,28,28))
        for f_ in range(3): d.rounded_rectangle([min(hx,hx-s*70),py+130+f_*95,max(hx,hx-s*70),py+190+f_*95],26,fill=(46,38,36))
    return noise_tex(im,7)
def under_bed():  # low view along the floorboards: the dark gap under my bed, a pale woman's face peeking out and long fingers reaching across the floor, speaker glowing red above
    im=base((6,6,10),(8,7,9)); d=ImageDraw.Draw(im)
    d.rectangle([0,300,BW,560],fill=(12,13,20))  # wall behind
    d.rectangle([BW-360,520,BW,545],fill=(46,36,30)); d.rectangle([BW-340,545,BW-40,820],fill=(30,24,20))  # nightstand
    vgrad(d,(0,1240,BW,BH),(30,20,20),(14,10,10))  # floor
    for k in range(12): yy=1240+k*k*6; d.line([0,yy,BW,yy],fill=(20,14,14),width=3)
    for k in range(-8,10): d.line([cx+k*50,1240,cx+k*230,BH],fill=(22,15,15),width=3)
    # blanket hanging over the side of the bed, with folds and a quilted pattern
    vgrad(d,(0,560,BW,900),(44,40,56),(32,28,40))
    for k in range(9): x=k*150-40; d.polygon([(x,620),(x+40,620),(x+90,900),(x+20,900)],fill=(28,25,36))
    for y in range(600,880,70):
        for x in range(30,BW,120): d.line([x,y,x+40,y+20],fill=(54,50,66),width=3)
    for x in range(0,BW,90): d.chord([x-10,860,x+100,960],0,180,fill=(36,32,46))  # wavy hem
    d.rectangle([0,930,BW,962],fill=(24,18,16))  # bed frame rail
    d.rectangle([0,962,BW,1250],fill=(1,1,2))  # the black gap under the bed
    for x in (30,BW-90): d.rectangle([x,950,x+60,1262],fill=(28,20,18))
    # her face, tilted, peeking out of the dark; hair drawn behind and around it
    fx,fy=cx+60,1110
    im=glow(im,(fx,fy),170,(110,80,80),0.3); d=ImageDraw.Draw(im)
    d.ellipse([fx-150,fy-140,fx+140,fy+150],fill=(5,4,5))  # hair mass
    for k in range(10): d.line([fx-140+k*30,fy+60,fx-170+k*34,fy+160+_R.normal(0,15)],fill=(5,4,5),width=16)  # hair spilling on the floor
    d.ellipse([fx-80,fy-105,fx+80,fy+105],fill=(112,106,104))
    d.ellipse([fx-60,fy-90,fx+70,fy+95],fill=(124,118,114))  # light on the face
    for ex in (-34,34):
        d.ellipse([fx+ex-28,fy-24,fx+ex+28,fy+20],fill=(52,44,46))  # dark sunken sockets
        d.ellipse([fx+ex-17,fy-11,fx+ex+17,fy+9],fill=(228,222,206)); d.ellipse([fx+ex-4,fy-5,fx+ex+4,fy+3],fill=(8,6,6))  # wide stare, pinpoint pupils
    d.ellipse([fx-14,fy+52,fx+14,fy+66],fill=(30,20,22))  # small open mouth
    for k in range(7):  # long hair strands hanging over the face
        x0=fx-95+k*16 if k<4 else fx+40+(k-4)*18; d.line([x0,fy-115,x0+_R.normal(0,6),fy+120],fill=(5,4,5),width=13)
    d.polygon([(fx-110,fy-125),(fx+90,fy-125),(fx+70,fy-80),(fx-100,fy-70)],fill=(5,4,5))  # hairline
    # long pale grey hand reaching out of the dark across the floor toward the camera
    hx,hy=cx-210,1330
    d.polygon([(hx-20,1200),(hx+50,1200),(hx+60,hy),(hx-40,hy+5)],fill=(92,86,84))  # thin wrist from the dark
    d.polygon([(hx-60,hy-5),(hx+75,hy-12),(hx+95,hy+40),(hx+90,hy+95),(hx-80,hy+100),(hx-85,hy+40)],fill=(118,110,106))  # palm
    for k,(ax,ay) in enumerate(((-130,230),(-55,275),(20,285),(90,245))):
        bx,by=hx-62+k*50,hy+92
        mx,my=(bx+hx+ax)/2+8,(by+hy+ay)/2
        d.line([bx,by,mx,my],fill=(118,110,106),width=22); d.line([mx,my,hx+ax,hy+ay],fill=(118,110,106),width=17)
        d.ellipse([mx-12,my-12,mx+12,my+12],fill=(126,118,112)); d.polygon([(hx+ax-9,hy+ay-6),(hx+ax+9,hy+ay-6),(hx+ax,hy+ay+16)],fill=(150,140,134))  # long nails
    d.line([hx+90,hy+30,hx+165,hy+115],fill=(118,110,106),width=20)  # thumb
    im=_speaker(im,BW-190,522,0.55,(230,40,30)); d=ImageDraw.Draw(im)
    im=cone(im,(BW-190,380),(cx-300,1600),(BW,1600),(200,40,30),0.16,40); d=ImageDraw.Draw(im)
    d.polygon([(0,BH),(0,1660),(160,1720),(300,BH)],fill=(5,4,5))
    return noise_tex(im,7)
# ---------- Ep13: rideshare at night (back seat of a gray sedan) ----------
_PLATE='7KDL 214'
def _car_inside(im,mirror_mode=None,exit_sign=False,lock_red=False):  # view from the back seat: windshield, dark highway, driver's head on the left, rear-view mirror top centre
    d=ImageDraw.Draw(im)
    vgrad(d,(0,300,BW,900),(6,10,22),(14,16,26)); stars(d,40,620,31)
    for x in range(-40,BW+80,70): pine(d,x,900,120+(x*31)%110,40,(5,7,9))
    d.polygon([(0,900),(BW,900),(BW,1000),(0,1000)],fill=(12,12,14))
    vx=cx+40
    d.polygon([(vx-20,900),(vx+20,900),(BW,1010),(0,1010)],fill=(28,28,31))
    for k in range(5): t=k/4; y=905+100*t**1.6; d.line([vx-2-40*t,y,vx+2+40*t,y+6+12*t],fill=(200,175,80),width=int(2+5*t))
    im=cone(im,(vx-160,1100),(vx-40,900),(vx+60,900),(200,190,150),0.35,26); im=cone(im,(vx+160,1100),(vx-40,900),(vx+60,900),(200,190,150),0.35,26)
    d=ImageDraw.Draw(im)
    if exit_sign:
        d.line([BW-420,640,BW-420,900],fill=(60,62,64),width=8); d.line([BW-300,640,BW-300,900],fill=(60,62,64),width=8)
        d.rounded_rectangle([BW-490,500,BW-230,680],12,fill=(22,92,52)); d.rounded_rectangle([BW-482,508,BW-238,672],10,outline=(220,230,220),width=4)
        d.text((BW-375,555),'EXIT 41',font=F(B,42),fill=(235,240,235),anchor='mm'); d.text((BW-375,625),'ELM ST',font=F(B,34),fill=(235,240,235),anchor='mm')
        d.polygon([(BW-262,640),(BW-245,605),(BW-279,605)],fill=(235,240,235))
    # roof liner, pillars, dashboard
    d.polygon([(0,0),(BW,0),(BW,300),(0,300)],fill=(18,17,20)); d.arc([-200,180,BW+200,520],190,350,fill=(24,23,26),width=30)
    d.polygon([(0,300),(160,300),(0,1150)],fill=(9,9,10)); d.polygon([(BW,300),(BW-160,300),(BW,1150)],fill=(9,9,10))
    d.polygon([(0,1000),(BW,1000),(BW,1140),(0,1140)],fill=(20,19,21)); d.rectangle([0,1140,BW,1260],fill=(14,13,15))
    im=glow(im,(260,1060),120,(40,110,140),0.5); d=ImageDraw.Draw(im)
    d.rounded_rectangle([180,1030,340,1090],12,fill=(30,90,110)); d.text((260,1060),'64',font=F(B,34),fill=(200,240,250),anchor='mm')  # speedo
    d.rounded_rectangle([cx-120,1040,cx+120,1120],14,fill=(26,60,80))  # centre screen
    for k in range(4): d.line([cx-100,1060+k*15,cx+90,1058+k*16],fill=(50,110,130),width=3)
    # rear-view mirror
    mx,my=cx,420
    d.rectangle([mx-14,300,mx+14,370],fill=(26,25,28))
    d.rounded_rectangle([mx-230,360,mx+230,500],40,fill=(30,29,32)); d.rounded_rectangle([mx-212,374,mx+212,486],32,fill=(14,16,24))
    if mirror_mode:
        red=mirror_mode=='red'
        d.rectangle([mx-212,374,mx+212,486],fill=(40,30,28) if not red else (60,22,20))
        d.rounded_rectangle([mx-212,374,mx+212,486],32,outline=(30,29,32),width=10)
        d.polygon([(mx-200,380),(mx+200,380),(mx+180,420),(mx-180,420)],fill=(10,9,10))  # brow/hair shadow
        ec=(240,230,210) if not red else (255,236,220)
        for ex in (-70,70):
            d.ellipse([mx+ex-46,my+4,mx+ex+46,my+44],fill=(70,58,54)); d.ellipse([mx+ex-30,my+12,mx+ex+30,my+38],fill=ec)
            d.ellipse([mx+ex-9,my+15,mx+ex+9,my+35],fill=(10,8,8))
        if red:  # smiling eyes: cheeks push the lower lids up
            for ex in (-70,70): d.chord([mx+ex-50,my+24,mx+ex+50,my+80],180,360,fill=(84,66,60))
            im=glow(im,(mx-70,my+22),40,(255,60,40),0.5); im=glow(im,(mx+70,my+22),40,(255,60,40),0.5); d=ImageDraw.Draw(im)
        d.line([mx-180,380,mx-120,486],fill=(70,72,84),width=4)
    else:
        d.line([mx-180,380,mx-120,486],fill=(50,54,68),width=5)
    d.ellipse([mx+150,380,mx+190,404],fill=(160,30,20) if lock_red else (40,40,44))
    # driver: back of head, shoulders, headrest on the left
    hx=330
    d.rounded_rectangle([hx-150,760,hx+150,1000],50,fill=(22,21,24))  # headrest
    d.rectangle([hx-40,980,hx-20,1060],fill=(40,40,44)); d.rectangle([hx+20,980,hx+40,1060],fill=(40,40,44))
    d.ellipse([hx-120,700,hx+120,960],fill=(6,6,7)); d.ellipse([hx+95,800,hx+135,870],fill=(8,8,9))  # head + ear
    d.polygon([(hx-260,1260),(hx-170,1010),(hx+170,1010),(hx+270,1260)],fill=(8,8,10))  # shoulders/seat back
    # empty passenger seat on the right
    px=BW-320
    d.rounded_rectangle([px-130,800,px+130,990],50,fill=(32,31,34)); d.rectangle([px-30,985,px+30,1060],fill=(40,40,44))
    d.polygon([(px-220,1260),(px-170,1040),(px+170,1040),(px+230,1260)],fill=(26,25,28))
    d.line([px-160,1060,px+150,1250],fill=(18,18,20),width=10)  # seat seam
    return im
def back_seat(mode=''):  # wide from my seat in the back: the driver ahead of me, my knees, the empty seat beside me, the door lock
    im=base((6,8,16),(12,10,12)); im=_car_inside(im,exit_sign=(mode=='exit'),lock_red=(mode=='exit')); d=ImageDraw.Draw(im)
    vgrad(d,(0,1260,BW,BH),(30,28,32),(14,13,15))  # back bench
    d.rounded_rectangle([40,1300,520,1520],60,fill=(22,21,24)); d.rounded_rectangle([60,1320,500,1500],50,fill=(28,27,30))  # my knees/jeans
    d.rounded_rectangle([620,1290,1180,1560],50,fill=(40,38,42)); d.rounded_rectangle([640,1310,1160,1540],44,fill=(46,44,48))  # empty seat beside me
    d.line([900,1310,900,1540],fill=(30,28,32),width=8)
    d.polygon([(1150,1280),(BW,1260),(BW,1620),(1130,1640)],fill=(18,17,20))  # rear door
    if mode=='exit':
        im=glow(im,(1170,1330),60,(230,30,20),0.8); d=ImageDraw.Draw(im)
        d.rounded_rectangle([1150,1300,1190,1360],10,fill=(220,40,30)); d.text((960,1400),'CHILD LOCK ON',font=F(B,30),fill=(230,70,60),anchor='mm')
    d.rectangle([1150,1240,1172,1300],fill=(70,70,76))  # lock pin
    d.line([40,1260,40,1700],fill=(60,58,40),width=14)  # seat belt strap
    d.polygon([(0,BH),(0,1640),(240,1700),(420,BH)],fill=(8,8,9))
    return noise_tex(im,7)
def rear_eyes(red=False):  # close on the rear-view mirror: the driver's eyes staring back at me
    im=base((6,8,16),(12,10,12)); im=_car_inside(im,mirror_mode=('red' if red else 'eyes'))
    im=im.crop((cx-380,110,cx+380,110+int(760*BH/BW))).resize((BW,BH),Image.BICUBIC)  # punch in on the mirror
    if red: im=glow(im,(cx,500),380,(160,20,15),0.35)
    return noise_tex(im,8)
def rear_window():  # I turn around: through the rear window, a second gray sedan right behind us, same plate
    im=base((5,8,18),(10,10,14)); d=ImageDraw.Draw(im); stars(d,50,600,37)
    for x in range(-40,BW+80,80): pine(d,x,860,180+(x*23)%140,55,(5,7,9))
    d.rectangle([0,860,BW,BH],fill=(14,14,16))
    d.polygon([(cx-30,860),(cx+30,860),(BW+300,BH),(-300,BH)],fill=(26,26,29))
    # the other car
    c=cx; y=1100
    d.polygon([(c-300,y-170),(c+300,y-170),(c+360,y+20),(c-360,y+20)],fill=(70,72,76))  # roof/windshield frame
    d.polygon([(c-260,y-150),(c+260,y-150),(c+310,y+5),(c-310,y+5)],fill=(16,18,24))  # dark windshield, nobody visible
    figure(d,c-150,y+20,150,(6,6,8))  # a driver shape, barely there
    d.rounded_rectangle([c-420,y+10,c+420,y+260],40,fill=(84,86,90)); d.rectangle([c-200,y+70,c+200,y+160],fill=(30,30,34))  # body + grille
    for k in range(5): d.line([c-190,y+85+k*16,c+190,y+85+k*16],fill=(54,54,58),width=4)
    d.rounded_rectangle([c-130,y+180,c+130,y+245],8,fill=(232,232,226)); d.text((c,y+213),_PLATE,font=F(B,44),fill=(30,50,120),anchor='mm')
    for s in (-1,1):
        im=glow(im,(c+s*300,y+110),150,(240,235,210),0.9); im=cone(im,(c+s*300,y+110),(c+s*700,BH),(c+s*100,BH),(200,195,170),0.25,40)
    d=ImageDraw.Draw(im)
    for s in (-1,1): d.ellipse([c+s*300-70,y+80,c+s*300+70,y+140],fill=(255,252,240))
    d.rounded_rectangle([c-150,y+175,c+150,y+250],8,fill=(236,236,230)); d.rectangle([c-150,y+175,c+150,y+188],fill=(150,30,30)); d.text((c,y+220),_PLATE,font=F(B,50),fill=(20,40,110),anchor='mm')
    # our rear window frame and back shelf (foreground)
    d.rectangle([0,0,BW,330],fill=(16,15,18)); d.polygon([(0,330),(150,330),(40,1500),(0,1500)],fill=(9,9,10)); d.polygon([(BW,330),(BW-150,330),(BW-40,1500),(BW,1500)],fill=(9,9,10))
    for k in range(8): d.line([140,420+k*60,BW-140,420+k*60],fill=(60,22,18),width=2)  # defroster lines
    d.rectangle([0,1480,BW,BH],fill=(18,17,19)); d.polygon([(0,1480),(BW,1480),(BW,1540),(0,1540)],fill=(26,25,28))
    d.rounded_rectangle([200,1420,460,1500],30,fill=(22,21,24)); d.rounded_rectangle([750,1420,1010,1500],30,fill=(22,21,24))  # rear headrests
    d.polygon([(0,BH),(0,1700),(260,1760),(380,BH)],fill=(8,8,9)); d.polygon([(BW,BH),(BW,1680),(BW-300,1740),(BW-420,BH)],fill=(10,9,10))  # my hand on the seat back
    return noise_tex(im,7)
def ride_app(mode='cancel'):  # my phone in the back seat with the ride app; driver's eyes faint in the mirror above
    im=base((6,8,16),(12,10,12)); im=_car_inside(im,mirror_mode=('eyes' if mode in ('cancel','text_red') else None)); d=ImageDraw.Draw(im)
    vgrad(d,(0,1260,BW,BH),(30,28,32),(14,13,15))
    px,py=cx,1180; pw,ph=320,560
    d.rounded_rectangle([px-pw-14,py-ph-14,px+pw+14,py+ph+14],64,fill=(8,8,10))
    sw_,sh_=2*pw-36,2*ph-56; scr=Image.new('RGB',(sw_,sh_),(16,18,22)); sd=ImageDraw.Draw(scr)
    red=mode in ('cancel','text_red')
    if mode in ('cancel','card'):
        my0=0 if mode=='cancel' else 480
        sd.rectangle([0,my0,sw_,my0+560],fill=(28,32,38))
        for k in range(9): sd.line([0,my0+40+k*70,sw_,my0+10+k*75],fill=(40,46,54),width=10)
        for k in range(6): sd.line([60+k*110,my0,30+k*120,my0+560],fill=(40,46,54),width=10)
        sd.line([100,my0+500,180,my0+380,380,my0+330,470,my0+150],fill=(70,170,230),width=14,joint='curve')
        sd.ellipse([86,my0+486,114,my0+514],fill=(255,255,255)); sd.rounded_rectangle([450,my0+130,490,my0+170],8,fill=(240,240,240))
        if mode=='cancel': sd.rectangle([0,560,sw_,sh_],fill=(20,22,26))
        else: sd.rectangle([0,0,sw_,480],fill=(20,22,26))
        if mode=='cancel':
            sd.rounded_rectangle([24,600,sw_-24,940],26,fill=(130,22,18))
            sd.text((sw_/2,660),'TRIP CANCELLED',font=F(B,42),fill=(255,236,230),anchor='mm')
            sd.text((sw_/2,740),'Your driver Dale',font=F(B,36),fill=(255,220,212),anchor='mm')
            sd.text((sw_/2,790),'cancelled the trip.',font=F(B,36),fill=(255,220,212),anchor='mm')
            sd.text((sw_/2,870),'Reason: rider no-show',font=F(B,32),fill=(255,190,180),anchor='mm')
            sd.text((sw_/2,990),'Finding you a new driver...',font=F(B,30),fill=(150,160,170),anchor='mm')
        else:
            sd.text((40,40),'On trip  2:51 AM',font=F(B,32),fill=(140,150,160))
            sd.ellipse([40,110,160,230],fill=(60,64,72)); sd.ellipse([78,130,122,174],fill=(30,32,36)); sd.chord([56,170,144,270],180,360,fill=(30,32,36))
            sd.text((190,120),'Dale',font=F(B,52),fill=(240,242,246)); sd.text((190,190),'4.9  Gray Camry',font=F(B,32),fill=(150,160,170))
            sd.rounded_rectangle([40,280,sw_-40,370],14,fill=(196,196,188)); sd.text((sw_/2,325),_PLATE,font=F(B,48),fill=(30,50,120),anchor='mm')
            sd.text((sw_/2,425),'Picked up 2:38 AM',font=F(B,30),fill=(120,200,140),anchor='mm')
    else:
        sd.rectangle([0,0,sw_,140],fill=(24,28,34)); sd.text((40,50),'<',font=F(B,44),fill=(70,170,230)); sd.text((sw_/2,70),'Dale  (driver)',font=F(B,38),fill=(240,242,246),anchor='mm')
        sd.text((sw_/2,190),'2:57 AM',font=F(B,26),fill=(120,130,140),anchor='mm')
        def bub(y,lines,col):
            h=40+len(lines)*52; sd.rounded_rectangle([30,y,sw_-90,y+h],30,fill=col)
            for k,t in enumerate(lines): sd.text((60,y+24+k*52),t,font=F(B,38),fill=(245,245,248))
            return y+h+30
        y=bub(240,["I'm behind you.","Who is driving?"],(48,52,60))
        if mode=='text_red':
            y=bub(y,["Get out.","That car was","crushed in 2019."],(150,24,18))
        sd.rounded_rectangle([30,sh_-110,sw_-30,sh_-30],40,fill=(30,34,40)); sd.text((70,sh_-70),'Message...',font=F(B,30),fill=(110,120,130),anchor='lm')
    im.paste(scr,(px-pw+18,py-ph+28)); im=glow(im,(px,py),460,(150,30,25) if red else (50,110,150),0.4); im.paste(scr,(px-pw+18,py-ph+28)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([px-80,py-ph+6,px+80,py-ph+36],14,fill=(4,4,6))
    d.line([px-pw+50,py-ph+110,px-pw+190,py-ph+470],fill=(60,70,80),width=4)
    for s in (-1,1):  # my hands holding the phone
        hx=px+s*(pw+10)
        d.polygon([(hx,py+80),(hx+s*70,py+40),(hx+s*150,py+500),(hx+s*120,BH),(hx-s*60,BH),(hx-s*30,py+560)],fill=(34,28,28))
        for f_ in range(3): d.rounded_rectangle([min(hx,hx-s*70),py+130+f_*95,max(hx,hx-s*70),py+190+f_*95],26,fill=(46,38,36))
    return noise_tex(im,7)
SC={'title':title,'outside':outside,'phone':phone,'phone_red':lambda:phone(True),'cam_empty':lambda:cam(0),'cam_man':lambda:cam(1),'cam_man_close':lambda:cam(2),'dark':dark,'dark_red':lambda:dark(True),
    'building':building,'elev9':lambda:elevator(9),'elev13':lambda:elevator(13),'hall':lambda:hall(False),'hall_woman':lambda:hall(True),'room_woman':room,
    'cabin':cabin,'door':door,'prints':prints,'closet':lambda:closet(False),'closet_woman':lambda:closet(True),
    'road':road,'gps':gps,'gps_red':lambda:gps(True),'mirror':mirror,'mirror_eyes':lambda:mirror(True),
    'farmhouse':farmhouse,'farmhouse_woman':lambda:farmhouse(True),'clipping':clipping,
    'monitor':monitor,'monitor_man':lambda:monitor('man'),'monitor_me':lambda:monitor('me'),'nursery':nursery,
    'lighthouse':lighthouse,'lantern':lantern,'lh_stairs':lambda:lh_stairs(0),'lh_stairs_man':lambda:lh_stairs(1),'lh_stairs_close':lambda:lh_stairs(2),
    'logbook':logbook,'logbook_red':lambda:logbook(True),
    'lh_door':lh_door,'lh_door_open':lambda:lh_door(True),'dock_boat':dock_boat,'logbook_shift':lambda:logbook(True,('Shift change.','Hers is over.','Mine begins.')),
    'ring_notify':lambda:ring_phone('notify'),'ring_far':lambda:ring_phone('far'),'ring_close':lambda:ring_phone('close'),'keypad':keypad,'slats':slats,'porch':porch,
    'bnb_house':bnb_house,'bnb_rules':bnb_rules,'bnb_rules_red':lambda:bnb_rules(True),'bnb_door':bnb_door,'bnb_door_turn':lambda:bnb_door('turn'),'bnb_text':bnb_text,
    'bnb_stairs':bnb_stairs,'bnb_stairs_woman':lambda:bnb_stairs('woman'),'bnb_stairs_up':lambda:bnb_stairs('up'),'bnb_tag':bnb_tag,'bnb_text_checkout':lambda:bnb_text('checkout'),
    'alexa':alexa,'alexa_red':lambda:alexa('red'),'alexa_room':alexa_room,'voice_app':voice_app,'voice_new':lambda:voice_app('new'),'voice_play':lambda:voice_app('play'),'under_bed':under_bed,
    'ride_cancel':lambda:ride_app('cancel'),'ride_card':lambda:ride_app('card'),'ride_text':lambda:ride_app('text'),'ride_text_red':lambda:ride_app('text_red'),
    'back_seat':back_seat,'back_exit':lambda:back_seat('exit'),'rear_eyes':rear_eyes,'rear_eyes_red':lambda:rear_eyes(True),'rear_window':rear_window}
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
