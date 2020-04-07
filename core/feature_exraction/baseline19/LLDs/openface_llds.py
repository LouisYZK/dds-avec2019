"""
This file is not relevant to DDS.
Just a attemption of OpenFace Tools

OpenFace are installed as docker container.
"""
import os

DOCKER_ID = '52f250c487f3'
folder = '/home/yzk/data/finance_mv'
output_dir = '/home/yzk/data/mv_llds'
docker_cmd = f"docker exec -it {DOCKER_ID} /bin/bash -c "
video_folder_in_ctn = '/home/openface-build/videos'
output_folder_in_ctn = '/home/openface-build/output'
exec_in_ctn = './build/bin/FaceLandmarkVidMulti'

for video in os.listdir(folder):
    try:
        os.system(f'docker cp {folder}/{video} {DOCKER_ID}:{video_folder_in_ctn}')
        extact_cmd = f'{exec_in_ctn} -f {video_folder_in_ctn}/{video} -out_dir {output_folder_in_ctn}'
        os.system(f"{docker_cmd} '{extact_cmd}' ")
        output_video_dir = f'{output_dir}/{video}'
        os.system(f'mkdir {output_video_dir}')

        os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video}.csv {output_video_dir}')
        os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video}.hog {output_video_dir}')
        os.system(f"{docker_cmd} 'rm -rf {output_folder_in_ctn}/*' ")
        break
    
    except Exception:
        continue
        