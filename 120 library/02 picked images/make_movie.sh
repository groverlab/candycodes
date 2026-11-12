#!/bin/bash
i=1; for f in *.pdf; do pdftoppm -png -r 300 "$f" $(printf "frame_%04d" $i); i=$((i+1)); done
ffmpeg -framerate 10 -pattern_type glob -i 'frame_*.png' -c:v libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -pix_fmt yuv420p out.mp4
