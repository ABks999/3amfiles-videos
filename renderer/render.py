import sys, json, os, subprocess, random, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw import *
import story as _story
HOOK=getattr(_story,'HOOK','')          # big text shown on top during the first line
TOPLABEL=getattr(_story,'TOPLABEL','')  # e.g. "PART 1" / "PART 2"
times=json.load(open('times.json'))
speech=json.load(open('speech.json')) if os.path.exists('speech.json') else [[a,b-0.3] for a,b in times]
FPS=30; os.makedirs('parts',exist_ok=True)
random.seed(3); rng=np.random.default_rng(1)

# ---------- look: colour grade, painted texture, bloom (applied once per scene) ----------
def grade(im):
    a=np.asarray(im,dtype=np.float32)/255.0
    a=np.clip(a,0,1)**0.82                                    # lift dark scenes a bit
    a=np.clip((a-0.5)*1.15+0.5+0.03,0,1)                     # contrast
    lum=a.mean(axis=2,keepdims=True)
    sh=np.array([0.80,0.95,1.18])[None,None,:]; hi=np.array([1.12,1.0,0.88])[None,None,:]
    a=a*(sh*(1-lum)+hi*lum)                                   # cold shadows, warm lights
    tex=rng.normal(0,1,(a.shape[0]//6,a.shape[1]//6)).astype(np.float32)
    tex=np.asarray(Image.fromarray(((tex*20)+128).clip(0,255).astype(np.uint8)).resize((a.shape[1],a.shape[0]),Image.BICUBIC),dtype=np.float32)/255.0
    a=a*(0.88+0.24*tex[...,None])                             # painted / grainy surface
    hh,ww=a.shape[:2]; gy,gx=np.mgrid[0:hh,0:ww].astype(np.float32)
    moon=np.exp(-(((gx-ww*0.15)/(ww*0.7))**2+((gy-hh*0.12)/(hh*0.45))**2))[...,None]*np.array([0.10,0.14,0.24])
    floor=np.exp(-(((gx-ww*0.5)/(ww*0.9))**2+((gy-hh*0.95)/(hh*0.3))**2))[...,None]*np.array([0.10,0.05,0.03])
    a=a+moon+floor                                            # cold moonlight from above, warm bounce below
    img=Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
    br=np.asarray(img,dtype=np.float32); mask=np.clip((br.mean(axis=2,keepdims=True)-90)/120,0,1)
    bloom=Image.fromarray((br*mask).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))
    out=np.clip(br+np.asarray(bloom,dtype=np.float32)*0.85,0,255).astype(np.uint8)
    return Image.fromarray(out)
scenes_used=set(l[1] for l in LINES)|{'dark_red'}
bgs={k:grade(SC[k]()) for k in scenes_used}

yy,xx=np.mgrid[0:H,0:W]; vig=1-0.5*(((xx-W/2)/(W*0.75))**2+((yy-H/2)/(H*0.7))**2); vig=np.clip(vig,0.25,1)[...,None].astype(np.float32)
grains=[rng.normal(0,8,(H,W,1)).astype(np.float32) for _ in range(6)]
# drifting fog: a wide, soft noise texture that scrolls sideways
_f=rng.random((24,72)).astype(np.float32)
FOG=np.asarray(Image.fromarray((_f*255).astype(np.uint8)).resize((W*3,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)),dtype=np.float32)/255.0
FOG=(np.clip(FOG-0.35,0,1)*1.6)[...,None]*np.array([150,160,185],dtype=np.float32)[None,None,:]*(np.linspace(0.3,1,H)[:,None,None])
# floating dust particles
NP=70; PX=rng.random(NP)*W; PY=rng.random(NP)*H; PV=rng.random(NP)*25+8; PS=rng.random(NP)*3+1.5; PA=rng.random(NP)*0.6+0.3

segs=[]; prev=0.0
for i,(a,b) in enumerate(times):
    segs.append((LINES[i][1],CAPTIONS[i],prev,b)); prev=b
segs.append((LINES[-1][1] if getattr(_story,'LOOP',False) else 'dark_red','__END__',prev,prev+1.2))
TWIST=len(LINES)-1  # last line = twist: punch-in, shake, red flash

def brand_layer():
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((W//2,120),'THE 3AM FILES',font=F(B,38),fill=(235,230,220,170),anchor='mm')
    if TOPLABEL:
        d.rounded_rectangle([W//2-130,165,W//2+130,235],18,fill=(200,30,25,230))
        d.text((W//2,200),TOPLABEL,font=F(B,44),fill=(255,255,255),anchor='mm')
    return lay
def hook_layer(text):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); f=F(B,92)
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>960 and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); y=330
    for ln in lines:
        d.text((W//2,y),ln,font=f,fill=(255,235,80),anchor='mm',stroke_width=10,stroke_fill=(0,0,0)); y+=110
    return lay
ENDTEXT=getattr(_story,'ENDTEXT',None)  # e.g. ("FOLLOW FOR","PART 2")
def end_layer():
    if not ENDTEXT: return endcard()
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((W//2,1640),ENDTEXT[0],font=F(B,70),fill=(255,255,255),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    d.text((W//2,1735),ENDTEXT[1],font=F(B,70),fill=(225,40,30),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    return lay
BRAND=brand_layer(); HOOKL=hook_layer(HOOK) if HOOK else None

# ---------- word-by-word captions (2-3 words at a time, the spoken word in yellow) ----------
CF=F(B,92); _cc={}
def chunks(text):
    words=text.split(); out=[]; cur=[]
    for w in words:
        if cur and (len(cur)>=3 or len(' '.join(cur+[w]))>16): out.append(cur); cur=[]
        cur.append(w)
    if cur: out.append(cur)
    return out
def word_caption(i,t):
    """caption image for line i at time t (seconds since the video start)."""
    s0,s1=speech[i]; ch=chunks(CAPTIONS[i]); words=[w for c in ch for w in c]
    wts=np.array([len(w)+2 for w in words],dtype=float); cum=np.concatenate([[0],np.cumsum(wts)])/wts.sum()
    p=(t-s0)/max(0.3,s1-s0); k=int(np.searchsorted(cum,np.clip(p,0,0.9999),side='right')-1)
    k=max(0,min(len(words)-1,k)); ci=0; acc=0
    for n,c in enumerate(ch):
        if k<acc+len(c): ci=n; break
        acc+=len(c)
    key=(i,ci,k-acc)
    if key not in _cc:
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); c=ch[ci]
        sp=d.textlength(' ',font=CF); ws=[d.textlength(w,font=CF) for w in c]; tot=sum(ws)+sp*(len(c)-1)
        if tot>980:  # too wide: two rows
            rows=[c[:len(c)//2+len(c)%2],c[len(c)//2+len(c)%2:]]
        else: rows=[c]
        y=1600-(len(rows)-1)*55; j=0
        for row in rows:
            rw=[d.textlength(w,font=CF) for w in row]; x=W/2-(sum(rw)+sp*(len(row)-1))/2
            for w,ww in zip(row,rw):
                col=(255,222,40) if j==k-acc else (255,255,255)
                d.text((x,y),w,font=CF,fill=col,anchor='lm',stroke_width=10,stroke_fill=(0,0,0)); x+=ww+sp; j+=1
            y+=110
        _cc[key]=lay
    return _cc[key],ci

SEG=[0]; _last_chunk=[None,0.0]
def frame(scene,cap_img,tg,ti,first,dur=2.5,twist=False):
    bg=bgs[scene]; n=SEG[0]; p=min(1.0,ti/max(0.5,dur))
    # camera: slow push + pan that alternates direction each line, handheld sway, punch-in on the twist
    z=(1.0 if n%2==0 else 1.06)+0.07*p
    if twist and ti<0.6: z+=0.22*(1-ti/0.6)**2
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]; dx,dy=dirs[n%4]
    sx=math.sin(tg*1.3)*7+math.sin(tg*2.9)*4; sy=math.cos(tg*1.1)*6+math.sin(tg*2.3)*3
    if twist and ti<0.9: amp=28*(1-ti/0.9); sx+=random.uniform(-amp,amp); sy+=random.uniform(-amp,amp)
    cw,ch=int(W/z),int(H/z); room_x=(BW-cw)//2; room_y=(BH-ch)//2
    x0=int(room_x+dx*(p-0.5)*room_x*0.8+sx); y0=int(room_y+dy*(p-0.5)*room_y*0.8+sy)
    x0=max(0,min(BW-cw,x0)); y0=max(0,min(BH-ch,y0))
    im=bg.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.BILINEAR)
    a=np.asarray(im,dtype=np.float32)
    off=int((tg*35)%(2*W)); a=a+FOG[:,off:off+W]*0.22                     # drifting fog
    a=a*vig+grains[int(tg*FPS)%6]
    fl=0.85 if random.random()<0.04 else (1.0+0.04*math.sin(tg*17)*(random.random()<0.3))  # light flicker
    a*=fl
    if ti<0.1 and n>0:  # cut: quick bright flash
        a=a*(1+1.2*(1-ti/0.1))
    if twist and ti<0.5: a[...,0]+=140*(1-ti/0.5); a[...,1]*=1-0.4*(1-ti/0.5); a[...,2]*=1-0.4*(1-ti/0.5)  # red flash
    glitch=(ti<0.13 and n>0) or (twist and ti<0.4) or (('woman' in scene or 'man' in scene or 'eyes' in scene) and random.random()<0.04)
    if glitch:  # RGB split
        s=random.randint(8,18); a[...,0]=np.roll(a[...,0],s,axis=1); a[...,2]=np.roll(a[...,2],-s,axis=1)
    a=np.clip(a,0,255).astype(np.uint8)
    im=Image.fromarray(a).convert('RGBA')
    dl=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(dl)               # dust
    for k in range(NP):
        x=(PX[k]+math.sin(tg*0.7+k)*30)%W; y=(PY[k]-tg*PV[k])%H; r=PS[k]
        d.ellipse([x-r,y-r,x+r,y+r],fill=(225,225,235,int(110*PA[k])))
    im.alpha_composite(dl)
    im.alpha_composite(BRAND)
    if first and HOOKL is not None:
        if ti<0.15:  # hook pops in
            sc=1.25-0.25*ti/0.15; hl=HOOKL.resize((int(W*sc),int(H*sc))); ox=(hl.width-W)//2; oy=int(330*sc-330)
            im.alpha_composite(hl.crop((ox,oy,ox+W,oy+H)))
        else: im.alpha_composite(HOOKL)
    if cap_img is not None: im.alpha_composite(cap_img)
    return im.convert('RGB').tobytes()

def cap_at(i,t):
    img,ci=word_caption(i,t)
    if _last_chunk[0]!=(i,ci): _last_chunk[0]=(i,ci); _last_chunk[1]=t
    age=t-_last_chunk[1]
    if age<0.08:  # each new chunk pops in
        sc=1.12-0.12*age/0.08; big=img.resize((int(W*sc),int(H*sc))); ox=(big.width-W)//2; oy=int(1600*sc-1600)
        return big.crop((ox,oy,ox+W,oy+H))
    return img

if __name__=='__main__':
    lst=[]
    for n,(scene,cap,a,b) in enumerate(segs):
        SEG[0]=n
        nf=round(b*FPS)-round(a*FPS); endimg=end_layer() if cap=='__END__' else None
        tmp=f'parts/p{n:02d}.tmp.mp4'; out=f'parts/p{n:02d}.mp4'
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
        for f in range(nf):
            tg=a+f/FPS; ci=endimg if endimg is not None else cap_at(n,tg)
            p.stdin.write(frame(scene,ci,tg,f/FPS,n==0,b-a,n==TWIST and cap!='__END__'))
        p.stdin.close()
        if p.wait()==0: os.rename(tmp,out)
        lst.append(f"file 'p{n:02d}.mp4'")
    open('parts/list.txt','w').write('\n'.join(lst))
    print('done', segs[-1][3])
