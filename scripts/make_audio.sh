#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-output}"
mkdir -p "$OUT"
ffmpeg -y -f lavfi -i "sine=frequency=110:sample_rate=48000:duration=10" -f lavfi -i "sine=frequency=164.81:sample_rate=48000:duration=10" -filter_complex "[0:a]volume=0.035,afade=t=in:st=0:d=1,afade=t=out:st=8.5:d=1.5[a0];[1:a]volume=0.018,afade=t=in:st=0:d=1,afade=t=out:st=8.5:d=1.5[a1];[a0][a1]amix=inputs=2:normalize=0,alimiter=limit=0.8[a]" -map "[a]" -c:a aac -b:a 128k "$OUT/ambient_bed.m4a"
ffmpeg -y -i "$OUT/dreamotion_3d_silent.mp4" -i "$OUT/ambient_bed.m4a" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest -movflags +faststart "$OUT/Dreamotion_3D_Prototype_10s.mp4"
ffprobe -v error -show_entries format=duration,size -of json "$OUT/Dreamotion_3D_Prototype_10s.mp4" > "$OUT/validation.json"
cat "$OUT/validation.json"
