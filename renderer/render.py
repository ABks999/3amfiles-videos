# ===================== GROWTH RULES v3 (channel manager, from Studio Analytics 12 Nov 2026) =====================
# These OVERRIDE v2 below wherever they disagree. 64-87% swiped away in the first 2-4 s, Part 1s did worst,
# best video was a RULE opener ("Never answer three knocks at 3 AM", 36% stayed). Audience: mostly Philippines/Malaysia.
# - NO Part 1 / Part 2 any more. Every story ends on its own (TOPLABEL stays ""). A sequel gets its own standalone hook.
# - LINE 1 = the impossible fact or a rule, max 12 words. Never open with a place, date, time or job.
#   Write 3 hook variants (impossible fact / rule / direct "you") and keep the most concrete and impossible one.
# - Line 2 must open a NEW question within 3 seconds.
# - At least every 3rd story uses the Rules format: "Never..." or "Rule one at...".
# - The last story line loops back to line 1 (LOOP = True). Then the sign-off as its own final LINES entry:
#   ("File closed. For now.", <same scene as the last line>, 0.2). tts.py reads it in a low, calm voice and
#   render.py/sfx.py treat the line BEFORE it as the twist.
# - 25-35 seconds in total.
# - Visuals: line 1's scene must SHOW the shock itself (the wrong thing), never a neutral establishing shot.
#   Frame 1 has movement and no fade/flash; the spoken line 1 is shown word for word as big text in frame 1
#   (render.py does this automatically from LINES[0]; the bottom caption is hidden during line 1).
#   story.py sets FILE = "FILE #015" etc. (shown small in the top-left corner the whole video).
#   If a whispered line fits, put the whisper (FEMALE) in the opening line: it stops the scroll.
# - HOOK is no longer shown when OPEN_TEXT is on (default). Keep HOOK = "" or a short fallback.
# ==========================================================================================================
# ===================== GROWTH RULES v2 (Hamza approved, 10 Nov 2026) =====================
# YouTube data after the first 7 Shorts: only 19% of viewers "stayed to watch", 81% swiped away in the
# first second. These rules OVERRIDE any older line/word counts in the task prompt:
# - LINE 1 IS A COLD OPEN: the single most shocking concrete fact of the story, max ~9 words, said as if
#   it is happening now. No time stamp or scene-setting first. Good: "There's a man standing in my baby's
#   nursery." / "Something is climbing my stairs. It's counting." Bad: "At 3:10 AM, the lighthouse turned on."
#   The documentary details (exact time, place) come in line 2-3 ("It started at 2:47 AM...").
# - Part 2: line 1 recaps the cliffhanger as a cold open ("It was on step 111. I was on 112.").
# - 8-10 lines, 60-80 words, target 25-32 seconds. Every line must add new information; cut filler.
# - HOOK: 2-4 words, a threat or a question, e.g. "DON'T LOOK UP", "WHO LIT IT?". Max ~14 characters
#   so it fits on ONE line.
# - Pauses: 0.15-0.3 s (tts.py caps them at 0.3, and 0.6 before the twist). Voice is sped up 12%.
# - The first scene must show the scary thing or a strong, readable image (a figure, eyes, a door ajar),
#   not an empty establishing shot.
# - MAKE THEM HOOKED (Hamza, 10 Nov): every story needs an OPEN LOOP the viewer must see closed.
#   * Relatable setting the viewer knows (their phone, Uber, babysitting, Ring doorbell, group chat,
#     night shift, hotel room, Airbnb, school bus, smart speaker) beats exotic places.
#   * One clear impossible detail early ("The text came from my own number.") and a question in the
#     viewer's head by line 2 that only the last line answers.
#   * Escalate every line: each line must be scarier or stranger than the last. No calm middle.
#   * Rule-based / instruction hooks work well: "If your Alexa ever whispers your name, don't answer."
#   * The twist must re-frame everything in one short line (max ~10 words) and land on the last word.
#   * Use "you" sometimes (second person) so the viewer feels it is happening to them.
#   * Make loops when possible: last line ends mid-thought that the first line completes.
# - render.py now: punch-in + flash + shake on the first frame, opening sound hit, brand name and
#   location stamp only appear after the first line, so the first second is just image + hook + caption.
# ==========================================================================================
# ===================== STORY + LOOK STYLE (documentary style, inspired by channels like Fern) =====================
# Hamza wants the channel to feel like a cinematic documentary, not a cheap jump-scare video:
# - Narration: calm, precise, documentary tone. Concrete details (exact times, places, objects, numbers).
#   (The OPENING follows GROWTH RULES v2 above: line 1 is a cold open, exact time/place come in line 2-3.) Dread builds fast,
#   short factual sentences, then a quiet but chilling twist. Stories stay FICTIONAL: never claim it is a true
#   story, never use real people or real crimes.
# - story.py may set LOCATION = ("DULUTH, MINNESOTA", "OCTOBER 14, 2019") (fictional details are fine): it is typed
#   out like a case file (lower left, above the captions) when line 2 starts. Use it in almost every episode.
# - The HOOK is shown in a clean serif title style. Keep it short and intriguing.
# - Look: desaturated filmic grade, soft halation, heavy grain, slow smooth camera moves, dips to black between
#   lines, subtle red pulse + push-in on the twist. No cartoon colours.
# ==================================================================================================================
import sys, json, os, subprocess, random, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw import *
import story as _story
HOOK=getattr(_story,'HOOK','')          # big text shown on top during the first line (only if OPEN_TEXT is False)
FILE=getattr(_story,'FILE','')          # e.g. "FILE #015", small in the top-left corner
OPEN_TEXT=getattr(_story,'OPEN_TEXT',True)  # v3: frame 1 shows the spoken line 1 word for word as big text
SIGNOFF=getattr(_story,'SIGNOFF','File closed. For now.')
TOPLABEL=getattr(_story,'TOPLABEL','')  # e.g. "PART 1" / "PART 2"
LOCATION=getattr(_story,'LOCATION',None) # e.g. ("DULUTH, MINNESOTA","OCTOBER 14, 2019")
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
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
    g=a.mean(axis=2,keepdims=True); a=a*0.62+g*0.38              # desaturate: documentary film look
    a=a*0.94+0.035                                            # lifted blacks (filmic)
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
    out=np.clip(br+np.asarray(bloom,dtype=np.float32)*np.array([1.0,0.75,0.6])*0.9,0,255).astype(np.uint8)
    return Image.fromarray(out)
scenes_used=set(l[1] for l in LINES)|{'dark_red'}
bgs={k:grade(SC[k]()) for k in scenes_used}

yy,xx=np.mgrid[0:H,0:W]; vig=1-0.62*(((xx-W/2)/(W*0.75))**2+((yy-H/2)/(H*0.7))**2); vig=np.clip(vig,0.25,1)[...,None].astype(np.float32)
grains=[rng.normal(0,11,(H,W,1)).astype(np.float32) for _ in range(6)]
# drifting fog: a wide, soft noise texture that scrolls sideways
_f=rng.random((24,72)).astype(np.float32)
FOG=np.asarray(Image.fromarray((_f*255).astype(np.uint8)).resize((W*3,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)),dtype=np.float32)/255.0
FOG=(np.clip(FOG-0.35,0,1)*1.6)[...,None]*np.array([150,160,185],dtype=np.float32)[None,None,:]*(np.linspace(0.3,1,H)[:,None,None])
# floating dust particles
NP=40; PX=rng.random(NP)*W; PY=rng.random(NP)*H; PV=rng.random(NP)*25+8; PS=rng.random(NP)*3+1.5; PA=rng.random(NP)*0.6+0.3

segs=[]; prev=0.0
for i,(a,b) in enumerate(times):
    segs.append((LINES[i][1],CAPTIONS[i],prev,b)); prev=b
segs.append((LINES[-1][1] if getattr(_story,'LOOP',False) else 'dark_red','__END__',prev,prev+1.2))
HAS_SIGN=len(LINES)>1 and LINES[-1][0].strip()==SIGNOFF
TWIST=len(LINES)-(2 if HAS_SIGN else 1)  # last story line = twist: punch-in, shake, red flash (the sign-off comes after it)

def brand_layer():
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((W//2,120),'THE 3AM FILES',font=F(B,38),fill=(235,230,220,170),anchor='mm')
    if TOPLABEL:
        d.rounded_rectangle([W//2-130,165,W//2+130,235],18,fill=(200,30,25,230))
        d.text((W//2,200),TOPLABEL,font=F(B,44),fill=(255,255,255),anchor='mm')
    return lay
def hook_layer(text):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); f=F(SERIF,96)
    for sz in (96,90,84,78):  # prefer ONE big line: shrink a little before wrapping
        if d.textlength(text,font=F(SERIF,sz))<=940: f=F(SERIF,sz); break
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>940 and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); y=340
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    for k,ln in enumerate(lines): sd.text((W//2,y+k*104),ln,font=f,fill=(0,0,0,200),anchor='mm')
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    for ln in lines:
        d.text((W//2,y),ln,font=f,fill=(245,240,232),anchor='mm',stroke_width=3,stroke_fill=(0,0,0)); y+=104
    d.rectangle([W//2-70,y-30,W//2+70,y-24],fill=(200,30,25))
    return lay
ENDTEXT=getattr(_story,'ENDTEXT',None)  # e.g. ("FOLLOW FOR","PART 2")
def end_layer():
    if not ENDTEXT: return endcard()
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((W//2,1640),ENDTEXT[0],font=F(B,70),fill=(255,255,255),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    d.text((W//2,1735),ENDTEXT[1],font=F(B,70),fill=(225,40,30),anchor='mm',stroke_width=8,stroke_fill=(0,0,0))
    return lay
def file_layer():
    lay=Image.new('RGBA',(W,H),(0,0,0,0))
    if not FILE: return lay
    d=ImageDraw.Draw(lay); f=F(M,38)
    d.rectangle([52,92,64,104],fill=(200,30,25,235))
    d.text((76,98),FILE,font=f,fill=(235,230,220,215),anchor='lm',stroke_width=3,stroke_fill=(0,0,0,170))
    return lay
FILEL=file_layer()
OPEN=LINES[0][0].strip()
BRAND=brand_layer(); HOOKL=hook_layer(OPEN if OPEN_TEXT else HOOK) if (OPEN_TEXT or HOOK) else None
_s=TOPLABEL; TOPLABEL=''; BRAND0=None
if _s:  # first line: only the PART label, no channel name (less clutter in the first second)
    BRAND0=Image.new('RGBA',(W,H),(0,0,0,0)); _d=ImageDraw.Draw(BRAND0)
    _d.rounded_rectangle([W//2-130,165,W//2+130,235],18,fill=(200,30,25,230)); _d.text((W//2,200),_s,font=F(B,44),fill=(255,255,255),anchor='mm')
TOPLABEL=_s
LOC0=times[1][0] if len(times)>1 else 0.0  # location stamp starts with line 2
MF=F(M,40); _lc={}
def location_layer(t):
    """case-file style place/date, typed out during the first seconds."""
    t=t-LOC0
    if not LOCATION or t<0 or t>6.0: return None
    full='\n'.join(LOCATION); n=min(len(full),int(t*28)); cur='_' if int(t*3)%2==0 and n<len(full) or t<4.5 and int(t*3)%2==0 else ''
    alpha=1.0 if t<5.2 else max(0.0,(6.0-t)/0.8); key=(n,cur,round(alpha,1))
    if key not in _lc:
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
        txt=full[:n]+cur; y=1330
        for k,ln in enumerate(txt.split('\n')):
            d.text((70,y+k*56),ln,font=MF,fill=(235,230,220,int(235*alpha)),stroke_width=3,stroke_fill=(0,0,0,int(200*alpha)))
        if n>0: d.rectangle([70,y-22,110,y-17],fill=(200,30,25,int(255*alpha)))
        _lc[key]=lay
    return _lc[key]

# ---------- word-by-word captions (2-3 words at a time, the spoken word in yellow) ----------
CF=F(B,78); _cc={}
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
                col=(255,214,120) if j==k-acc else (245,242,236)
                d.text((x,y),w,font=CF,fill=col,anchor='lm',stroke_width=7,stroke_fill=(0,0,0)); x+=ww+sp; j+=1
            y+=96
        sh=lay.getchannel('A').filter(ImageFilter.GaussianBlur(12)); shadow=Image.new('RGBA',(W,H),(0,0,0,0)); shadow.putalpha(sh.point(lambda v:int(v*0.6)))
        shadow.alpha_composite(lay); lay=shadow
        _cc[key]=lay
    return _cc[key],ci

SEG=[0]; _last_chunk=[None,0.0]
def frame(scene,cap_img,tg,ti,first,dur=2.5,twist=False):
    bg=bgs[scene]; n=SEG[0]; p=min(1.0,ti/max(0.5,dur))
    # camera: slow push + pan that alternates direction each line, handheld sway, punch-in on the twist
    e=p*p*(3-2*p)  # ease in-out
    z=(1.0 if n%2==0 else 1.06)+0.08*e
    if twist and ti<0.6: z+=0.22*(1-ti/0.6)**2
    if first and ti<0.5: z+=0.25*(1-ti/0.5)**2   # opening punch-in
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]; dx,dy=dirs[n%4]
    sx=math.sin(tg*0.5)*5; sy=math.cos(tg*0.4)*4
    if twist and ti<0.6: amp=14*(1-ti/0.6); sx+=random.uniform(-amp,amp); sy+=random.uniform(-amp,amp)
    if first and ti<0.4: amp=12*(1-ti/0.4); sx+=random.uniform(-amp,amp); sy+=random.uniform(-amp,amp)
    cw,ch=int(W/z),int(H/z); room_x=(BW-cw)//2; room_y=(BH-ch)//2
    x0=int(room_x+dx*(e-0.5)*room_x*0.8+sx); y0=int(room_y+dy*(e-0.5)*room_y*0.8+sy)
    x0=max(0,min(BW-cw,x0)); y0=max(0,min(BH-ch,y0))
    im=bg.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.BILINEAR)
    a=np.asarray(im,dtype=np.float32)
    off=int((tg*35)%(2*W)); a=a+FOG[:,off:off+W]*0.22                     # drifting fog
    a=a*vig+grains[int(tg*FPS)%6]
    fl=0.9 if random.random()<0.02 else 1.0  # rare light flicker
    a*=fl
    if ti<0.18 and n>0: a=a*(ti/0.18)  # dip from black between lines
    if dur-ti<0.1 and not twist and not first: a=a*max(0.0,(dur-ti)/0.1)  # no black frames inside line 1
    if twist: r=max(0.0,1-ti/1.2); a[...,0]+=60*r; a[...,1]*=1-0.35*r; a[...,2]*=1-0.35*r  # slow red pulse
    glitch=(twist and ti<0.25)
    if glitch:  # RGB split
        s=random.randint(8,18); a[...,0]=np.roll(a[...,0],s,axis=1); a[...,2]=np.roll(a[...,2],-s,axis=1)
    a=np.clip(a,0,255).astype(np.uint8)
    im=Image.fromarray(a).convert('RGBA')
    dl=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(dl)               # dust
    for k in range(NP):
        x=(PX[k]+math.sin(tg*0.5+k)*30)%W; y=(PY[k]-tg*PV[k]*0.6)%H; r=PS[k]
        d.ellipse([x-r,y-r,x+r,y+r],fill=(225,220,210,int(80*PA[k])))
    im.alpha_composite(dl)
    if first: 
        if BRAND0 is not None: im.alpha_composite(BRAND0)
    else: im.alpha_composite(BRAND)
    im.alpha_composite(FILEL)
    if first and HOOKL is not None:
        if ti<0.15:  # hook pops in
            sc=(1.07-0.07*ti/0.15) if OPEN_TEXT else (1.25-0.25*ti/0.15); hl=HOOKL.resize((int(W*sc),int(H*sc))); ox=(hl.width-W)//2; oy=int(330*sc-330)
            im.alpha_composite(hl.crop((ox,oy,ox+W,oy+H)))
        else: im.alpha_composite(HOOKL)
    ll=location_layer(tg)
    if ll is not None: im.alpha_composite(ll)
    if cap_img is not None and not (first and OPEN_TEXT and HOOKL is not None): im.alpha_composite(cap_img)  # line 1 text is already big on screen
    return im.convert('RGB').tobytes()

def cap_at(i,t):
    img,ci=word_caption(i,t)
    if _last_chunk[0]!=(i,ci): _last_chunk[0]=(i,ci); _last_chunk[1]=t
    age=t-_last_chunk[1]
    if age<0.08:  # each new chunk eases in
        sc=1.05-0.05*age/0.08; big=img.resize((int(W*sc),int(H*sc))); ox=(big.width-W)//2; oy=int(1600*sc-1600)
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
