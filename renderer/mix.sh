#!/bin/bash
set -e
EP=$(cat episode.txt)
cd parts && ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy ../video_noaudio.mp4 && cd ..
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 video_noaudio.mp4)
FO=$(python3 -c "print($D-2)")
mkdir -p ../videos
ffmpeg -y -loglevel error -i video_noaudio.mp4 -i voice.wav \
 -f lavfi -i "anoisesrc=color=brown:amplitude=0.25:d=60" -f lavfi -i "sine=f=55:d=60" -f lavfi -i "sine=f=58.3:d=60" \
 -filter_complex "[2]lowpass=f=400,volume=0.35[n];[3][4]amix=2,volume=0.5,tremolo=f=0.2:d=0.6[d];[n][d]amix=2,volume=0.6,afade=t=in:d=2,afade=t=out:st=$FO:d=2[amb];[1]highpass=f=80,equalizer=f=3000:t=q:w=1:g=4,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,aecho=0.8:0.5:40|70:0.18|0.10,apad[v];[v][amb]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
 -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 26 -maxrate 3M -bufsize 6M -pix_fmt yuv420p -c:a aac -b:a 160k -t $D -movflags +faststart ../videos/ep$(printf %02d $EP).mp4
