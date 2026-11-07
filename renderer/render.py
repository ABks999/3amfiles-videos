import sys, json, os, subprocess, random, numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw import *
times=json.load(open('times.json'))
FPS=30; os.makedirs('parts',exist_ok=True)
scenes_used=set(l[1] for l in LINES)|{'dark_red'}
bgs={k:SC[k]() for k in scenes_used}
yy,xx=np.mgrid[0:H,0:W]; vig=1-0.65*(((xx-W/2)/(W*0.75))**2+((yy-H/2)/(H*0.7))**2); vig=np.clip(vig,0.25,1)[...,None]
rng=np.random.default_rng(1); grains=[rng.normal(0,9,(H,W,1)) for _ in range(6)]
segs=[]; prev=0.0
for i,(a,b) in enumerate(times):
    segs.append((LINES[i][1],CAPTIONS[i],prev,b)); prev=b
segs.append(('dark_red','__END__',prev,prev+1.5))
group_start={}
def frame(scene,cap_img,tg,ti):
    bg=bgs[scene]
    gs=group_start.setdefault(scene,tg); z=1.0+min((tg-gs)/40,0.1)
    cw,ch=int(BW/z/1.12),int(BH/z/1.12)
    x0=(BW-cw)//2; y0=(BH-ch)//2
    im=bg.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.BILINEAR)
    if ('woman' in scene or 'man' in scene or '13' in scene) and random.random()<0.08: im=im.point(lambda v:min(255,v+25))
    a=np.asarray(im,dtype=np.float32)*vig+grains[int(tg*FPS)%6]
    fl=0.93 if random.random()<0.05 else 1.0
    a=np.clip(a*fl,0,255).astype(np.uint8)
    im=Image.fromarray(a).convert('RGBA')
    if cap_img is not None:
        if ti<0.12: c=cap_img.copy(); c.putalpha(c.getchannel('A').point(lambda v:int(v*ti/0.12))); im.alpha_composite(c)
        else: im.alpha_composite(cap_img)
    return im.convert('RGB').tobytes()
lst=[]
for n,(scene,cap,a,b) in enumerate(segs):
    nf=round(b*FPS)-round(a*FPS); cap_img=endcard() if cap=='__END__' else caption(cap)
    tmp=f'parts/p{n:02d}.tmp.mp4'; out=f'parts/p{n:02d}.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    for f in range(nf): p.stdin.write(frame(scene,cap_img,a+f/FPS,f/FPS))
    p.stdin.close()
    if p.wait()==0: os.rename(tmp,out)
    lst.append(f"file 'p{n:02d}.mp4'")
open('parts/list.txt','w').write('\n'.join(lst))
print('done', segs[-1][3])
