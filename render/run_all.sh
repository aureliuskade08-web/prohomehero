#!/bin/bash
cd /home/claude/prohomehero/render
W=1440; H=900
for v in A B; do
  python3 kitchen.py $v quartz mask out/mask_$v.png $W $H
  for c in quartz granite slate; do
    python3 kitchen.py $v $c beauty out/${v}_$c.png $W $H 96
    echo "done $v $c" >> out/progress.txt
  done
done
echo ALLDONE >> out/progress.txt
