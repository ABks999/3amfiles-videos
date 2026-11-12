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

SC_EXTRA={
    'hotel_phone':hotel_phone,'hotel_phone_red':lambda:hotel_phone('red'),  # beige hotel desk phone ringing; display FRONT DESK / BATHROOM 414
    'hotel_room':hotel_room,  # wide hotel room: me sitting on the bed, closed bathroom door with light under it
    'hotel_bed':lambda:hotel_room('bed'),  # same room: someone lying under the covers, dark hair and a pale hand on the pillow
    'hotel_bath':hotel_bath,  # closed bathroom door, bright light under it, shadows of two feet standing behind it
}
