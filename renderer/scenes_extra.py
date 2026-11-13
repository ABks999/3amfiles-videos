# ===================== EXTRA SCENES (added 12 Nov 2026) =====================
# draw.py is now ~130 KB and the GitHub connector can only write whole files, so NEW scenes go in THIS file.
# Same style guide as the top of draw.py. All draw.py helpers are available (from draw import *).
# Register every new scene in SC_EXTRA at the bottom. render.py merges SC_EXTRA into SC automatically.
# Scene ids must not clash with ids already in draw.py's SC.
# ============================================================================
from draw import *
def _hotel_wall(d,top=0,bot=1180):  # damask-ish hotel wallpaper + crown moulding
    d.rectangle([0,top,BW,bot],fill=(16,14,18))
    for y in range(top+40,bot,120):
        for x in range(((y//120)%2)*60,BW,120): d.polygon([(x,y-26),(x+16,y),(x,y+26),(x-16,y)],fill=(21,18,23))
    d.rectangle([0,top,BW,top+20],fill=(26,23,28))
def hotel_phone(mode='desk'):  # close-up: beige hotel desk phone on a nightstand at 3 AM, lit display, room key card, lamp; red = display BATHROOM 414
    red=(mode=='red'); acc=(230,45,35) if red else (240,170,70)
    im=base((8,8,12),(10,9,12)); d=ImageDraw.Draw(im); _hotel_wall(d,0,1150)
    # framed generic hotel art + heavy curtains with a streetlight slit
    d.rectangle([520,330,900,640],fill=(40,34,30)); d.rectangle([540,350,880,620],fill=(30,36,40))
    d.polygon([(540,620),(650,470),(720,540),(800,440),(880,620)],fill=(22,26,30))
    d.polygon([(0,240),(300,240),(330,1150),(0,1150)],fill=(28,16,20))
    for x in range(20,300,55): d.line([x,240,x+12,1150],fill=(20,11,14),width=10)
    d.rectangle([300,240,318,1150],fill=(70,80,100)); im=cone(im,(309,240),(150,1150),(470,1150),(80,95,130),0.22,30); d=ImageDraw.Draw(im)
    # lamp on the right (warm, dim)
    im=glow(im,(900,860),160,(140,90,40),0.3); d=ImageDraw.Draw(im)
    d.polygon([(800,760),(1000,760),(1060,960),(740,960)],fill=(90,70,46)); d.rectangle([890,960,910,1190],fill=(40,34,28)); d.ellipse([830,1180,970,1215],fill=(40,34,28))
    # nightstand top
    vgrad(d,(0,1180,BW,1270),(58,42,32),(42,30,24)); d.rectangle([0,1270,BW,BH],fill=(28,20,17))
    d.line([0,1182,BW,1182],fill=(90,70,52),width=4)
    for k in range(5): d.line([0,1320+k*80,BW,1330+k*80],fill=(34,25,21),width=5)
    d.rounded_rectangle([cx-120,1440,cx+120,1478],12,fill=(50,38,30))
    # notepad + pen, key card
    d.polygon([(60,1200),(330,1190),(345,1265),(70,1275)],fill=(120,116,106)); d.line([90,1225,300,1218],fill=(150,150,160),width=3)
    d.line([240,1265,380,1190],fill=(20,20,30),width=10)
    d.polygon([(790,1230),(960,1222),(966,1262),(796,1270)],fill=(150,30,30)); d.text((812,1232),'414',font=F(B,26),fill=(230,220,210))
    # the phone (big, centre)
    px,py=cx-60,1215
    d.polygon([(px-260,py),(px+260,py),(px+220,py-200),(px-220,py-200)],fill=(92,86,74))
    d.polygon([(px-220,py-200),(px+220,py-200),(px+200,py-225),(px-200,py-225)],fill=(110,104,90))
    d.polygon([(px-260,py),(px-220,py-200),(px-205,py-200),(px-240,py)],fill=(62,58,50))
    # handset in cradle, rattling
    off=0 if red else 6
    d.rounded_rectangle([px-250,py-300+off,px+250,py-225+off],38,fill=(98,92,80)); d.rounded_rectangle([px-250,py-300+off,px+250,py-280+off],20,fill=(118,111,96))
    for s in (-1,1): d.ellipse([px+s*210-55,py-320+off,px+s*210+55,py-235+off],fill=(86,80,70))
    d.line([px+250,py-260,px+330,py-180],fill=(60,56,50),width=8)
    for k in range(6): d.arc([px+300+k*12,py-200+k*25,px+360+k*12,py-170+k*25],0,180,fill=(60,56,50),width=6)  # coiled cord
    # keypad
    for r in range(4):
        for c in range(3):
            kx=px-70+c*70; ky=py-170+r*40; d.rounded_rectangle([kx-26,ky-14,kx+26,ky+14],6,fill=(66,62,54))
    # display
    im=glow(im,(px+150,py-130),90,acc,0.35); d=ImageDraw.Draw(im)
    d.rectangle([px+75,py-175,px+215,py-95],fill=tuple(int(c*0.35) for c in acc)); d.rectangle([px+82,py-168,px+208,py-102],fill=tuple(int(c*0.8) for c in acc))
    d.text((px+145,py-150),'BATHROOM' if red else 'FRONT',font=F(M,20),fill=(20,10,5),anchor='mm'); d.text((px+145,py-122),'414' if red else 'DESK',font=F(M,24),fill=(20,10,5),anchor='mm')
    d.ellipse([px-200,py-185,px-180,py-165],fill=acc)  # message light
    for k in range(3):  # ring vibration marks
        r=290+k*60; d.arc([px-r,py-270-r*0.4,px+r,py-270+r*0.4],205,335,fill=tuple(int(c*(0.55-0.15*k)) for c in acc),width=6)
    im=cone(im,(px+145,py-135),(px-200,py+300),(px+500,py+300),acc,0.07,40); d=ImageDraw.Draw(im)
    d.polygon([(0,BH),(0,1620),(180,1660),(300,BH)],fill=(8,6,7))  # foreground bedsheet edge
    return noise_tex(im,7)
def hotel_room(mode='wide'):  # wide hotel room at night seen from the entry: me sitting on the bed, closed bathroom door on the right; bed = empty side of room, lump under the covers with a pale hand
    im=base((7,8,12),(10,9,12)); d=ImageDraw.Draw(im); _hotel_wall(d,0,1160)
    # window with curtains, city glow through the gap
    d.rectangle([80,300,480,880],fill=(20,24,38))
    for k in range(10): d.rectangle([100+k*36,560+(k*37)%200,118+k*36,880],fill=(14,16,26))  # distant buildings
    for k in range(18): x=110+(k*53)%340; y=620+(k*71)%220; d.rectangle([x,y,x+6,y+8],fill=(150,130,80))
    for x0,x1 in ((40,250),(320,520)): d.polygon([(x0,270),(x1,270),(x1+10,1160),(x0-10,1160)],fill=(30,17,21))
    d.rectangle([250,270,320,1160],fill=(0,0,0),outline=None); d.rectangle([250,300,320,880],fill=(26,30,46))
    im=cone(im,(285,600),(120,1600),(620,1600),(80,95,140),0.18,40); d=ImageDraw.Draw(im)
    # bathroom door right wall, light under it
    d.rectangle([700,340,1010,1160],fill=(36,32,34)); d.rectangle([720,360,990,1160],fill=(48,43,44))
    d.rectangle([742,390,968,740],outline=(40,36,38),width=6); d.rectangle([742,780,968,1120],outline=(40,36,38),width=6)
    d.ellipse([738,770,760,792],fill=(150,130,90))
    im=glow(im,(855,1162),120,(235,225,190),0.5); d=ImageDraw.Draw(im); d.rectangle([720,1152,990,1162],fill=(250,240,210))
    d.rectangle([0,1160,BW,1172],fill=(26,22,24)); vgrad(d,(0,1172,BW,BH),(34,26,26),(10,8,9))
    for k in range(9): d.line([0,1230+k*k*9,BW,1230+k*k*9],fill=(30,22,22),width=2)  # carpet pattern
    # light spill from door on carpet
    d.polygon([(720,1172),(990,1172),(1120,1400),(640,1400)],fill=(58,48,44))
    # bed (left, low): headboard, sheets, pillows
    d.rectangle([-20,960,560,1180],fill=(46,34,30)); d.rectangle([-20,950,560,970],fill=(70,54,44))
    d.polygon([(-40,1170),(580,1170),(680,1640),(-40,1640)],fill=(92,90,102)); d.polygon([(-40,1300),(620,1300),(680,1640),(-40,1640)],fill=(120,40,46))  # bed runner
    d.rounded_rectangle([20,1090,250,1190],30,fill=(118,118,128)); d.rounded_rectangle([280,1090,510,1190],30,fill=(118,118,128))
    # nightstand + lamp between bed and door
    d.rectangle([570,1080,690,1300],fill=(40,30,24)); im=glow(im,(630,1010),90,(240,170,70),0.4); d=ImageDraw.Draw(im)
    d.rectangle([600,1050,660,1080],fill=(30,24,20)); d.ellipse([608,1062,652,1076],fill=(240,170,70))  # phone display glowing
    if mode=='bed':
        # someone under the covers, body shape, pale hand on the pillow
        d.polygon([(40,1260),(120,1180),(420,1170),(560,1230),(600,1330),(80,1340)],fill=(64,60,74))
        d.arc([60,1170,580,1360],200,340,fill=(44,40,52),width=12); d.arc([140,1200,520,1330],210,330,fill=(44,40,52),width=8)
        d.ellipse([220,1095,340,1185],fill=(8,7,8)); d.polygon([(220,1150),(180,1210),(260,1190)],fill=(8,7,8))  # dark hair on pillow
        d.polygon([(330,1150),(400,1140),(440,1155),(400,1165),(330,1165)],fill=(215,205,195))
        for f in range(4): d.line([430,1150+f*5,465,1146+f*6],fill=(215,205,195),width=5)
        # my shadow cast across the bed from the bathroom light
        d.polygon([(700,1400),(760,1390),(560,1240),(480,1250)],fill=(14,12,14))
    else:
        # me sitting on the edge of the bed, silhouette facing the bathroom door
        d.ellipse([420,1010,500,1110],fill=(14,12,14)); d.polygon([(400,1110),(520,1110),(560,1330),(380,1330)],fill=(16,14,18))
        d.polygon([(470,1320),(640,1330),(640,1360),(470,1360)],fill=(16,14,18)); d.line([640,1340,650,1520],fill=(16,14,18),width=30)
    d.polygon([(BW-110,240),(BW,240),(BW,BH),(BW-160,BH)],fill=(5,5,7)); d.polygon([(0,BH),(0,1700),(220,BH)],fill=(5,5,7))  # entry doorframe
    return noise_tex(im,7)
def hotel_bath(mode='closed'):  # close on the closed bathroom door from the carpet: bright light under it, two shadows of feet breaking the strip; a cord dangling (the wall phone)
    im=base((7,7,10),(9,8,10)); d=ImageDraw.Draw(im); _hotel_wall(d,0,1250)
    # door frame + door
    d.rectangle([170,200,910,1260],fill=(40,36,36)); d.rectangle([200,230,880,1260],fill=(56,50,50))
    for (x0,y0,x1,y1) in ((250,290,830,720),(250,770,830,1200)):
        d.rectangle([x0,y0,x1,y1],outline=(44,40,40),width=10); d.line([x0+6,y0+6,x1-6,y0+6],fill=(70,64,62),width=3)
    d.rectangle([228,720,268,820],fill=(120,105,80)); d.ellipse([214,750,264,800],fill=(170,150,110))  # handle
    d.rounded_rectangle([450,560,630,640],8,fill=(180,170,150)); d.text((540,600),'PRIVATE',font=F(B,26),fill=(60,50,40),anchor='mm')  # hanging sign
    d.line([480,560,540,470],fill=(150,140,120),width=3); d.line([600,560,540,470],fill=(150,140,120),width=3); d.ellipse([530,460,550,480],fill=(140,120,90))
    # light seeping around the door and underneath
    im=glow(im,(540,1262),240,(240,232,200),0.65); d=ImageDraw.Draw(im)
    d.rectangle([200,1250,880,1264],fill=(255,248,225)); d.line([882,240,882,1250],fill=(200,190,160),width=3)
    # two feet shadows in the light strip, standing right behind the door
    for fx in (430,600): d.rectangle([fx,1248,fx+70,1266],fill=(10,8,8))
    # light beams on carpet
    im=cone(im,(540,1265),(80,BH),(1000,BH),(220,210,180),0.28,30); d=ImageDraw.Draw(im)
    vgrad(d,(0,1266,BW,BH),(42,34,32),(12,10,10))
    for k in range(10): d.line([0,1300+k*k*7,BW,1300+k*k*7],fill=(34,26,26),width=2)
    d.polygon([(200,1266),(880,1266),(1000,1460),(80,1460)],fill=(78,66,58))
    for fx in (430,600): d.polygon([(fx,1266),(fx+70,1266),(fx+110,1460),(fx-30,1460)],fill=(30,24,22))  # long feet shadows
    # light switch, thermostat on the wall
    d.rounded_rectangle([960,700,1030,810],8,fill=(150,145,135)); d.rectangle([985,735,1005,775],fill=(110,105,96))
    d.rounded_rectangle([950,880,1050,960],10,fill=(30,34,30)); d.text((1000,920),'68',font=F(M,30),fill=(90,200,120),anchor='mm')
    # foreground: bed corner and a sheet hanging, left
    d.polygon([(0,1380),(150,1400),(230,BH),(0,BH)],fill=(10,9,11)); d.polygon([(BW,BH),(BW,1560),(900,BH)],fill=(6,5,6))
    return noise_tex(im,7)


# ---------- Ep15 mall night guard scenes (added 13 Nov 2026) ----------
def _mannequin(d,x,y,h,col=(196,188,176),wave=False,tilt=0,eyes=None,uniform=False,shade=(150,142,132)):
    """smooth featureless shop mannequin. (x,y)=base of the stand, h=height to the top of the head."""
    hd=h*0.075; hx=x+tilt*hd*0.6; hy=y-h+hd
    body=(50,60,96) if uniform else col; bshade=(30,36,62) if uniform else shade
    # stand
    d.line([x,y-h*0.08,x,y],fill=(60,60,64),width=8); d.ellipse([x-h*0.09,y-10,x+h*0.09,y+12],fill=(48,48,52))
    # legs
    for s in (-1,1):
        d.polygon([(x+s*h*0.012,y-h*0.47),(x+s*h*0.075,y-h*0.47),(x+s*h*0.05,y-h*0.08),(x+s*h*0.02,y-h*0.08)],fill=body)
    # torso (hourglass), shading on the right side
    t=[(x-h*0.085,y-h+hd*2.4),(x+h*0.085,y-h+hd*2.4),(x+h*0.06,y-h*0.66),(x+h*0.08,y-h*0.47),(x-h*0.08,y-h*0.47),(x-h*0.06,y-h*0.66)]
    d.polygon(t,fill=body); d.polygon([(x+h*0.03,y-h+hd*2.4),(x+h*0.085,y-h+hd*2.4),(x+h*0.06,y-h*0.66),(x+h*0.08,y-h*0.47),(x+h*0.04,y-h*0.47)],fill=bshade)
    if uniform:
        d.line([x,y-h+hd*2.5,x,y-h*0.47],fill=(16,18,30),width=4)
        for k in range(4): d.ellipse([x-5,y-h+hd*3+k*h*0.06-5,x+5,y-h+hd*3+k*h*0.06+5],fill=(180,170,120))
        d.rectangle([x-h*0.075,y-h*0.73,x+h*0.07,y-h*0.71],fill=(14,14,20))  # belt
        d.polygon([(x-h*0.06,y-h+hd*3.2),(x-h*0.025,y-h+hd*3.2),(x-h*0.025,y-h+hd*4.0),(x-h*0.06,y-h+hd*4.0)],fill=(190,170,90))  # badge
        d.rectangle([x+h*0.02,y-h+hd*3.3,x+h*0.07,y-h+hd*3.75],fill=(220,215,200))  # name tag
    # neck + head
    d.rectangle([hx-hd*0.3,hy+hd*0.8,hx+hd*0.3,y-h+hd*2.5],fill=col)
    d.ellipse([hx-hd*0.8,hy-hd,hx+hd*0.8,hy+hd],fill=col); d.chord([hx-hd*0.8,hy-hd,hx+hd*0.8,hy+hd],300,60,fill=shade)
    if uniform:  # guard cap
        d.chord([hx-hd*0.9,hy-hd*1.25,hx+hd*0.9,hy+hd*0.2],180,360,fill=(28,32,54)); d.polygon([(hx-hd*0.9,hy-hd*0.5),(hx+hd*1.25,hy-hd*0.5),(hx+hd*0.9,hy-hd*0.3),(hx-hd*0.9,hy-hd*0.3)],fill=(14,16,28))
    if eyes is not None:
        e=hd*0.17
        for s in (-1,1): d.ellipse([hx+s*hd*0.33-e,hy-e*0.5,hx+s*hd*0.33+e,hy+e*0.7],fill=eyes)
    # arms
    sh_y=y-h+hd*2.6; aw=max(6,int(h*0.032))
    lx,rx=x-h*0.09,x+h*0.09
    d.line([lx,sh_y,lx-h*0.03,sh_y+h*0.2,lx-h*0.02,sh_y+h*0.36],fill=body if uniform else col,width=aw,joint='curve')
    d.ellipse([lx-h*0.02-aw*0.7,sh_y+h*0.36-aw*0.7,lx-h*0.02+aw*0.7,sh_y+h*0.36+aw*0.9],fill=col)
    if wave:  # forearm up, open hand
        ex,ey=rx+h*0.11,sh_y+h*0.08; hx2,hy2=rx+h*0.13,sh_y-h*0.14
        d.line([rx,sh_y,ex,ey,hx2,hy2],fill=body if uniform else col,width=aw,joint='curve')
        d.ellipse([hx2-aw*1.0,hy2-aw*1.5,hx2+aw*1.0,hy2+aw*0.6],fill=col)
        for f in range(4): d.line([hx2-aw*0.75+f*aw*0.5,hy2-aw*1.0,hx2-aw*0.9+f*aw*0.65,hy2-aw*2.4],fill=col,width=max(3,aw//3))
        d.line([hx2+aw*0.9,hy2,hx2+aw*1.8,hy2-aw*0.9],fill=col,width=max(3,aw//3))
    else:
        d.line([rx,sh_y,rx+h*0.03,sh_y+h*0.2,rx+h*0.02,sh_y+h*0.36],fill=body if uniform else col,width=aw,joint='curve')
        d.ellipse([rx+h*0.02-aw*0.7,sh_y+h*0.36-aw*0.7,rx+h*0.02+aw*0.7,sh_y+h*0.36+aw*0.9],fill=col)

def mall_window(mode='wave'):  # closed clothing shop window inside a dark mall at 3 AM; wave = middle mannequin waving, head tilted; reflect = my guard reflection waving in the glass; guard = mannequin in guard uniform in the window, my flashlight on the floor
    acc=(90,220,190)
    im=base((5,7,10),(8,9,11)); d=ImageDraw.Draw(im)
    # mall ceiling + skylight band, upper floor railing
    d.rectangle([0,0,BW,330],fill=(10,12,16))
    for x in range(-40,BW,150): d.line([x,0,x+60,330],fill=(16,18,24),width=6)
    d.rectangle([0,300,BW,340],fill=(26,28,32))
    # shop facade + sign
    d.rectangle([40,340,BW-40,1420],fill=(20,20,24)); d.rectangle([70,370,BW-70,470],fill=(14,14,18))
    d.text((cx,420),'LUNA  APPAREL',font=F(SERIFD,58),fill=(70,76,80),anchor='mm')
    # shutter half-down at top
    d.rectangle([90,490,BW-90,610],fill=(40,42,46))
    for y in range(495,610,16): d.line([90,y,BW-90,y],fill=(30,32,36),width=4)
    # inside the window: back wall, shelves, display light
    d.rectangle([90,610,BW-90,1400],fill=(14,22,22))
    for y in (760,900): d.rectangle([110,y,330,y+12],fill=(24,34,34)); d.rectangle([BW-330,y,BW-110,y+12],fill=(24,34,34))
    for k in range(6): d.rectangle([125+k*32,y-110 if k%2 else y-90,148+k*32,y],fill=(28,40,40))
    im=glow(im,(cx,640),330,acc,0.18); im=cone(im,(cx,612),(200,1500),(BW-200,1500),acc,0.12,40); d=ImageDraw.Draw(im)
    d.rectangle([90,1400,BW-90,1560],fill=(14,22,22)); d.rectangle([90,1500,BW-90,1560],fill=(30,40,40)); d.line([90,1502,BW-90,1502],fill=(70,100,96),width=3)  # display platform
    # mannequins
    if mode=='guard':
        _mannequin(d,300,1500,540,col=(140,134,126),shade=(110,104,98)); _mannequin(d,BW-300,1500,540,col=(140,134,126),shade=(110,104,98),tilt=0.4)
        _mannequin(d,cx,1505,600,col=(170,162,150),shade=(130,122,112),wave=True,uniform=True,tilt=-0.5,eyes=(20,10,10))
    elif mode=='reflect':
        _mannequin(d,280,1500,540,col=(96,94,90),shade=(76,74,70)); _mannequin(d,cx-150,1505,580,col=(104,100,96),shade=(80,78,74)); _mannequin(d,BW-260,1500,540,col=(96,94,90),shade=(76,74,70),tilt=0.6)
    else:
        _mannequin(d,290,1500,530,col=(140,134,126),shade=(110,104,98)); _mannequin(d,BW-290,1500,530,col=(140,134,126),shade=(110,104,98))
        _mannequin(d,cx,1505,600,col=(176,168,156),shade=(132,124,114),wave=True,tilt=-0.9,eyes=(12,4,4))
    # glass: frame mullions, diagonal reflections
    for x in (90,cx+260,BW-90): d.rectangle([x-8,610,x+8,1560],fill=(34,36,40))
    gl=Image.new('RGB',im.size,(0,0,0)); g=ImageDraw.Draw(gl)
    for x0 in (180,560,900): g.polygon([(x0,610),(x0+60,610),(x0-170,1560),(x0-230,1560)],fill=(50,58,66))
    if mode=='reflect':  # my reflection: guard silhouette with cap and flashlight, arm raised
        rx,ry=cx+120,1520
        g.ellipse([rx-48,ry-690,rx+48,ry-590],fill=(120,135,160)); g.chord([rx-58,ry-720,rx+58,ry-620],180,360,fill=(110,125,150)); g.rectangle([rx-60,ry-660,rx+75,ry-648],fill=(110,125,150))
        g.polygon([(rx-85,ry-580),(rx+85,ry-580),(rx+95,ry-260),(rx+60,ry),(rx-60,ry),(rx-95,ry-260)],fill=(100,115,140))
        g.line([rx+80,ry-570,rx+170,ry-470,rx+180,ry-720],fill=(100,115,140),width=34,joint='curve'); g.ellipse([rx+150,ry-790,rx+212,ry-700],fill=(120,135,160))
        g.line([rx-80,ry-570,rx-120,ry-380],fill=(100,115,140),width=34); g.rectangle([rx-150,ry-400,rx-100,ry-300],fill=(150,160,180))
    gl=gl.filter(ImageFilter.GaussianBlur(3 if mode=='reflect' else 6))
    im=Image.fromarray(np.clip(np.asarray(im,float)+np.asarray(gl,float)*(0.62 if mode=='reflect' else 0.28),0,255).astype('uint8')); d=ImageDraw.Draw(im)
    # mall floor: polished tiles reflecting the window light
    vgrad(d,(0,1580,BW,BH),(30,34,36),(10,11,12))
    for k in range(8): d.line([0,1600+k*k*8,BW,1600+k*k*8],fill=(22,24,26),width=3)
    for k in range(-6,8): d.line([cx+k*60,1580,cx+k*260,BH],fill=(22,24,26),width=3)
    im=cone(im,(cx,1580),(160,BH),(BW-160,BH),acc,0.12,50); d=ImageDraw.Draw(im)
    if mode=='guard':  # my flashlight on the floor, still on, beam across the tiles
        fx,fy=260,1700; d.polygon([(fx,fy),(fx+150,fy-30),(fx+160,fy+10),(fx+10,fy+40)],fill=(30,30,34)); d.ellipse([fx+140,fy-34,fx+172,fy+14],fill=(250,240,200))
        im=cone(im,(fx+160,fy-10),(BW,fy-160),(BW,fy+200),(240,230,190),0.3,30); d=ImageDraw.Draw(im)
    # EXIT sign far right + foreground pillar and bench silhouettes
    d.rectangle([BW-250,250,BW-120,300],fill=(30,10,10)); d.text((BW-185,275),'EXIT',font=F(B,32),fill=(230,60,50),anchor='mm'); im=glow(im,(BW-185,275),70,(200,40,30),0.4); d=ImageDraw.Draw(im)
    d.polygon([(0,240),(70,240),(90,BH),(0,BH)],fill=(5,5,7)); d.polygon([(BW,BH),(BW,1720),(BW-260,1760),(BW-300,BH)],fill=(6,6,8))
    return noise_tex(im,7)

def mall_rules(mode='desk'):  # security desk: clipboard with a photocopied NIGHT GUARD RULES sheet under a flashlight beam, radio, keys, coffee
    im=base((6,7,10),(9,8,8)); d=ImageDraw.Draw(im)
    # back: guard booth window to the dark mall, a mannequin silhouette far away
    d.rectangle([0,0,BW,620],fill=(10,12,16)); d.rectangle([60,120,BW-60,600],fill=(14,18,24))
    for k in range(5): d.rectangle([100+k*220,380,240+k*220,600],fill=(18,22,28)); d.rectangle([110+k*220,390,230+k*220,420],fill=(24,30,34))
    _mannequin(d,860,590,250,col=(120,118,112),wave=True,shade=(90,88,84))
    d.rectangle([40,600,BW-40,640],fill=(30,30,34))
    # desk surface
    vgrad(d,(0,640,BW,BH),(46,40,36),(16,14,13))
    for k in range(7): d.line([0,700+k*140,BW,680+k*150],fill=(40,35,31),width=3)
    # clipboard + sheet (slightly rotated look via polygon)
    d.polygon([(190,760),(1010,730),(1050,1700),(220,1730)],fill=(80,58,36)); d.rounded_rectangle([520,700,700,790],14,fill=(170,170,176))
    d.polygon([(230,800),(980,775),(1015,1660),(260,1685)],fill=(168,162,148))
    def L(y,txt,f,col=(30,28,26)):
        x=262+ (y-800)*0.033; d.text((x,y),txt,font=f,fill=col)
    L(830,'NIGHT GUARD RULES',F(B,52)); d.line([262,900,950,880],fill=(30,28,26),width=4)
    L(940,'1. Never wave back at the',F(SERIFD,40)); L(990,'   mannequins after 3 AM.',F(SERIFD,40))
    L(1070,'2. Count them every hour.',F(SERIFD,40)); L(1120,'   There are NINE.',F(SERIFD,40),(150,20,18))
    L(1200,'3. Do not look at the glass',F(SERIFD,40)); L(1250,'   for too long.',F(SERIFD,40))
    for k in range(5): d.line([300,1340+k*55,880+((k*97)%80),1320+k*55],fill=(150,146,136),width=6)
    d.ellipse([820,1060,900,1150],outline=(170,20,20),width=5)  # red pen circle around NINE
    # tally marks scribbled at the bottom
    for k in range(9): d.line([320+k*26,1600,330+k*26,1540],fill=(40,40,90),width=5)
    d.line([310,1585,560,1550],fill=(40,40,90),width=5)
    # flashlight lying on the desk, beam across the sheet
    d.polygon([(BW-40,1290),(BW-330,1440),(BW-300,1500),(BW,1360)],fill=(26,26,30)); d.ellipse([BW-360,1420,BW-290,1520],fill=(250,240,205))
    im=cone(im,(BW-320,1470),(100,700),(300,1800),(250,235,190),0.08,40); d=ImageDraw.Draw(im)
    # radio + keys + coffee cup
    d.rounded_rectangle([40,1250,190,1560],18,fill=(20,20,22)); d.rectangle([150,1150,170,1260],fill=(16,16,18)); d.ellipse([70,1290,160,1380],fill=(34,34,38)); d.rectangle([80,1420,150,1460],fill=(80,160,90))
    d.ellipse([1000,760,1150,830],fill=(40,30,26)); d.rectangle([1000,795,1150,1000],fill=(200,195,185)); d.ellipse([1000,970,1150,1030],fill=(180,175,165)); d.ellipse([1012,768,1138,822],fill=(36,22,14))
    return noise_tex(im,7)

def mall_cctv(mode='count'):  # security monitor wall: 4 grainy green CCTV feeds; count = food court with mannequins standing between tables; guard = big feed of a mannequin in a guard uniform, face close, name tag
    acc=(110,220,140)
    im=base((5,6,8),(8,8,9)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,BW,BH],fill=(9,10,12))
    for y in range(0,BW*2,90): d.line([0,y,BW,y-200],fill=(11,12,14),width=2)
    # monitor housing
    d.rounded_rectangle([50,300,BW-50,1450],24,fill=(22,22,26)); d.rounded_rectangle([75,325,BW-75,1425],18,fill=(4,6,5))
    def feed(box,label,draw_fn):
        x0,y0,x1,y1=box; sub=Image.new('RGB',(x1-x0,y1-y0),(8,22,12)); s=ImageDraw.Draw(sub); draw_fn(s,sub.size)
        a=np.asarray(sub,float); a+=np.random.default_rng(x0+y0).normal(0,14,a.shape[:2])[...,None]
        a[::4]*=0.75; sub=Image.fromarray(np.clip(a,0,255).astype('uint8'))
        im.paste(sub,(x0,y0)); d.text((x0+14,y0+10),label,font=F(M,24),fill=(190,240,190))
        d.ellipse([x1-34,y0+14,x1-16,y0+32],fill=(220,40,30))
    def court(s,sz,n=10):
        w,h=sz; s.rectangle([0,0,w,int(h*0.45)],fill=(14,34,20)); s.polygon([(0,h),(w,h),(w*0.8,h*0.45),(w*0.2,h*0.45)],fill=(22,48,28))
        for k in range(5): s.rectangle([int(w*0.08+k*w*0.18),int(h*0.15),int(w*0.08+k*w*0.18+w*0.12),int(h*0.42)],fill=(26,56,32))
        r=np.random.default_rng(4)
        for k in range(6): tx=int(w*(0.15+0.14*k)); ty=int(h*(0.62+0.18*(k%2))); s.ellipse([tx-40,ty-10,tx+40,ty+10],fill=(40,80,46))
        for k in range(n):
            mx=int(w*(0.1+0.8*r.random())); my=int(h*(0.55+0.4*r.random())); mh=int(h*(0.22+0.25*(my/h-0.55)/0.4))
            _mannequin(s,mx,my,mh,col=(150,200,150),shade=(110,160,110),wave=(k==n-1))
    def corridor(s,sz):
        w,h=sz; s.polygon([(0,0),(w*0.4,h*0.4),(w*0.4,h*0.7),(0,h)],fill=(18,40,22)); s.polygon([(w,0),(w*0.6,h*0.4),(w*0.6,h*0.7),(w,h)],fill=(18,40,22)); s.polygon([(0,h),(w,h),(w*0.6,h*0.7),(w*0.4,h*0.7)],fill=(26,52,30))
    def escal(s,sz):
        w,h=sz; s.polygon([(w*0.2,h),(w*0.45,h),(w*0.8,h*0.2),(w*0.65,h*0.2)],fill=(30,60,34))
        for k in range(8): s.line([w*0.25+k*w*0.06,h-k*h*0.1,w*0.45+k*w*0.045,h-k*h*0.1],fill=(18,40,22),width=3)
    if mode=='guard':
        def guard(s,sz):
            w,h=sz; s.rectangle([0,0,w,h],fill=(12,30,16)); s.rectangle([0,int(h*0.75),w,h],fill=(20,44,24))
            for k in range(3): s.rectangle([int(w*0.05+k*w*0.33),int(h*0.1),int(w*0.25+k*w*0.33),int(h*0.6)],fill=(18,40,22))
            _mannequin(s,int(w*0.25),int(h*0.95),int(h*0.6),col=(140,190,140),shade=(100,150,100))
            _mannequin(s,int(w*0.55),int(h*1.35),int(h*1.3),col=(170,220,170),shade=(120,170,120),uniform=True,tilt=-0.6,eyes=(10,20,10))
        feed((95,345,BW-95,1060),'CAM 4  FOOD COURT  03:14',guard)
        feed((95,1080,cx-10,1405),'CAM 2',corridor); feed((cx+10,1080,BW-95,1405),'CAM 7',lambda s,sz:court(s,sz,6))
        d.text((BW-120,1000),'11',font=F(M,64),fill=(240,60,50),anchor='rm')
    else:
        feed((95,345,BW-95,900),'CAM 4  FOOD COURT  02:00',court)
        feed((95,920,cx-10,1405),'CAM 2',corridor); feed((cx+10,920,BW-95,1405),'CAM 5',escal)
        d.text((BW-120,850),'10',font=F(M,64),fill=(240,60,50),anchor='rm')
    im=glow(im,(cx,800),520,acc,0.16); d=ImageDraw.Draw(im)
    # desk edge, keyboard, my hand silhouette holding a pen; foreground chair back
    d.rectangle([0,1470,BW,BH],fill=(18,16,15)); d.line([0,1472,BW,1472],fill=(50,46,42),width=4)
    d.polygon([(200,1520),(900,1510),(940,1600),(170,1615)],fill=(30,30,34))
    for r in range(3):
        for c in range(12): d.rectangle([220+c*56,1528+r*26,262+c*56,1548+r*26],fill=(44,44,50))
    im=cone(im,(cx,1440),(0,BH),(BW,BH),acc,0.1,50); d=ImageDraw.Draw(im)
    d.polygon([(BW,1500),(BW-200,1600),(BW-160,BH),(BW,BH)],fill=(5,5,6))
    return noise_tex(im,7)

def mall_hall(mode='wave'):  # long dark mall corridor at 3 AM from my flashlight: closed shutters both sides, dead escalator; a single mannequin standing in the MIDDLE of the walkway, waving at me, face lit by the beam
    im=base((5,6,9),(8,8,10)); d=ImageDraw.Draw(im)
    vx,vy=cx,900
    d.polygon([(0,0),(BW,0),(vx+120,vy-200),(vx-120,vy-200)],fill=(10,11,15))  # ceiling
    for k in range(7): yy=60+k*k*12; d.line([vx-120-(vx-120)*(1-(vy-200-yy)/(vy-200)),yy,vx+120+(BW-vx-120)*(1-(vy-200-yy)/(vy-200)),yy],fill=(16,18,22),width=6)
    for s in (-1,1):  # walls with shop shutters
        xs=0 if s<0 else BW; xi=vx+s*120
        d.polygon([(xs,0),(xi,vy-200),(xi,vy+60),(xs,1500)],fill=(18,18,22))
        for k in range(5):
            t0=k/5; t1=(k+0.8)/5
            def P(t,yA,yB): return (xs+(xi-xs)*t, yA+(yB-yA)*t)
            a=P(t0,260,vy-150); b=P(t1,260,vy-150); c=P(t1,1380,vy+40); e=P(t0,1380,vy+40)
            d.polygon([a,b,c,e],fill=(30,31,35))
            for j in range(1,9):
                f=j/9; d.line([a[0]+(e[0]-a[0])*f,a[1]+(e[1]-a[1])*f,b[0]+(c[0]-b[0])*f,b[1]+(c[1]-b[1])*f],fill=(24,25,28),width=3)
            sa=P(t0,200,vy-170); sb=P(t1,200,vy-170); d.polygon([sa,sb,(b[0],b[1]-10),(a[0],a[1]-10)],fill=(14,14,18))
    d.rectangle([vx-120,vy-200,vx+120,vy+60],fill=(6,7,9))
    # escalator in the distance, EXIT glow
    d.polygon([(vx-60,vy+60),(vx+10,vy+60),(vx+80,vy-150),(vx+40,vy-150)],fill=(28,28,32))
    d.rectangle([vx-40,vy-185,vx+40,vy-160],fill=(30,10,10)); im=glow(im,(vx,vy-172),50,(200,40,30),0.4); d=ImageDraw.Draw(im)
    # floor tiles, polished
    d.polygon([(0,1500),(BW,1500),(vx+120,vy+60),(vx-120,vy+60)],fill=(26,28,30)); d.rectangle([0,1500,BW,BH],fill=(22,24,26))
    for k in range(-7,8): d.line([vx+k*24,vy+60,vx+k*300,BH],fill=(18,20,22),width=3)
    for k in range(10): yy=vy+60+k*k*13; d.line([0,yy,BW,yy],fill=(18,20,22),width=3)
    # flashlight beam from bottom
    im=cone(im,(cx+60,BH+100),(cx-330,880),(cx+420,880),(240,232,200),0.32,30); d=ImageDraw.Draw(im)
    # the mannequin in the middle of the walkway, waving, head tilted
    if mode=='wave':
        _mannequin(d,cx+20,1420,620,col=(215,206,192),wave=True,tilt=0.8,eyes=(18,6,6))
        d.ellipse([cx-90,1405,cx+130,1440],fill=(12,12,14))
    # benches + planter foreground, my hand with flashlight bottom right
    d.polygon([(0,1600),(260,1580),(280,1660),(0,1700)],fill=(8,8,10)); d.rectangle([20,1660,50,1800],fill=(8,8,10)); d.rectangle([220,1650,250,1780],fill=(8,8,10))
    d.polygon([(BW-60,BH),(BW-280,1820),(BW-220,1760),(BW,1880)],fill=(10,10,12)); d.ellipse([BW-300,1770,BW-230,1840],fill=(250,240,210))
    return noise_tex(im,7)

SC_EXTRA={
    'hotel_phone':hotel_phone,'hotel_phone_red':lambda:hotel_phone('red'),  # beige hotel desk phone ringing; display FRONT DESK / BATHROOM 414
    'hotel_room':hotel_room,  # wide hotel room: me sitting on the bed, closed bathroom door with light under it
    'hotel_bed':lambda:hotel_room('bed'),  # same room: someone lying under the covers, dark hair and a pale hand on the pillow
    'hotel_bath':hotel_bath,  # closed bathroom door, bright light under it, shadows of two feet standing behind it
    'mall_wave':mall_window,  # shop window at 3 AM, middle mannequin waving with head tilted and dark eyes
    'mall_reflect':lambda:mall_window('reflect'),  # same window: my guard reflection in the glass raising its hand
    'mall_guard':lambda:mall_window('guard'),  # same window: a mannequin in a GUARD UNIFORM waving, my flashlight on the floor
    'mall_rules':mall_rules,  # NIGHT GUARD RULES sheet on the security desk under a flashlight
    'mall_cctv':mall_cctv,  # CCTV wall, food court with mannequins, counter shows 10
    'mall_cctv_guard':lambda:mall_cctv('guard'),  # CCTV: a mannequin in a guard uniform close to cam 4, counter 11
    'mall_hall':mall_hall,  # dark mall corridor, one mannequin in the middle of the walkway waving in the flashlight beam
}
