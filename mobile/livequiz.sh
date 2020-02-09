#!/bin/sh

# kills frida-server already presents
for i in `pgrep frida`; do kill -9 $i; done
# runs frida-servers
/data/local/tmp/frida-android-arm64/bin/frida-server -D
# run livequiz
am start -n com.bendingspoons.live.quiz/com.bendingspoons.live.quiz.MainActivity
# run agent.js
/data/local/tmp/frida-android-arm64/bin/frida-inject -n com.bendingspoons.live.quiz -R v8 -s /data/local/tmp/agent.js
# kills frida-servers
for i in `pgrep frida`; do kill -9 $i; done
