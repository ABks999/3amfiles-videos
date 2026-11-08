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
SC={'title':title,'outside':outside,'phone':phone,'phone_red':lambda:phone(True),'cam_empty':lambda:cam(0),'cam_man':lambda:cam(1),'cam_man_close':lambda:cam(2),'dark':dark,'dark_red':lambda:dark(True),
    'building':building,'elev9':lambda:elevator(9),'elev13':lambda:elevator(13),'hall':lambda:hall(False),'hall_woman':lambda:hall(True),'room_woman':room,
    'cabin':cabin,'door':door,'prints':prints,'closet':lambda:closet(False),'closet_woman':lambda:closet(True),
    'road':road,'gps':gps,'gps_red':lambda:gps(True),'mirror':mirror,'mirror_eyes':lambda:mirror(True),
    'farmhouse':farmhouse,'farmhouse_woman':lambda:farmhouse(True),'clipping':clipping}
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
