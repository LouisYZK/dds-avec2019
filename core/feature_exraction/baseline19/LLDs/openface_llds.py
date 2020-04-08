"""
This file is not relevant to DDS.
Just a attemption of OpenFace Tools

OpenFace are installed as docker container.
"""
import os
from multiprocessing import Process

DOCKER_ID = '52f250c487f3'
folder = '/home/yzk/data/finance_mv'
output_dir = '/home/yzk/data/mv_llds'
docker_cmd = f"docker exec -it {DOCKER_ID} /bin/bash -c "
video_folder_in_ctn = '/home/openface-build/videos'
output_folder_in_ctn = '/home/openface-build/output'
exec_in_ctn = './build/bin/FaceLandmarkVidMulti'


def task(video_id=None):
    if video_id is None:
        video_list = os.listdir(folder)
    else:
        video_list = video_id
    for video in video_list:
        try:
            os.system(f'docker cp {folder}/{video} {DOCKER_ID}:{video_folder_in_ctn}')
            extact_cmd = f'{exec_in_ctn} -f {video_folder_in_ctn}/{video} -out_dir {output_folder_in_ctn}'
            os.system(f"{docker_cmd} '{extact_cmd}' ")

            video_name = video.split('.')[0]
            output_video_dir = f'{output_dir}/{video_name}'
            os.system(f'mkdir {output_video_dir}')

            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.csv {output_video_dir}')
            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.hog {output_video_dir}')
            os.system(f"{docker_cmd} 'rm -rf {output_folder_in_ctn}/*' ")
        
        except Exception:
            continue
        
if __name__ == "__main__":
    # task = Process(target=task)
    # task.start()
    le = ['playlist_eof_092f90545285890788603532709.mp4']
    task(video_id=le)


"""
du -sh | sort -nr
playlist_eof_ce2dbcb05285890789025941333, video should roated and the face appear few time.
right 90.
playlist_eof_092f90545285890788603532709 should roate left 90
playlist_eof_417a64c95285890788719982866 should roate left 90
playlist_eof_4cc268255285890788604121024 left 90
playlist_eof_275ad83a5285890788658530905 right 90 and very dark, face can be seen
playlist_eof_e18a4a605285890788861505598 right 90 and face are in edge
playlist_eof_a21146dc5285890789011402002 left 90
playlist_eof_08fced045285890788518854893 right 90
playlist_eof_4cc268255285890788604121024 left 90
playlist_eof_4abd28d25285890788723064119 left 90
playlist_eof_9fe005825285890788575349673 right 90
playlist_eof_c1b1c7415285890788684953409 left 90
playlist_eof_79b4c45c5285890789136860576 left 90
playlist_eof_b11666585285890788684215544 left 90
playlist_eof_c0d45c7d5285890789405674719 left 90
playlist_eof_308404f65285890789030588651 right 90
playlist_eof_cc12cf5b5285890788752493273 right 90
playlist_eof_73a720a95285890789031111709 right 90
playlist_eof_cf5f01a15285890788942737574 left 90
playlist_eof_884b1a5e5285890788649563471 right 90
playlist_eof_225c095a5285890788974225813 left 90
playlist_eof_d0f4fa325285890788538122183 left 90
playlist_eof_f12ab3235285890788732388658 left 90
playlist_eof_6d21fc355285890788815093163 left 90
"""