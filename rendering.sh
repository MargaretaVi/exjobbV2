#! /bin/bash
start_time="$(date -u +%s)"

for file in /home/xmreality/Documents/exjobbV2/ikea/*; do
	if [[ $file = *.blend ]]; then 
		blender $file --background --python /home/xmreality/Documents/exjobbV2/Rendering_v2.py -- /home/xmreality/Desktop/ikea/background /home/xmreality/Desktop/ikea/texture ~/Desktop/ikea_img/ $file
	fi
done	
end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
