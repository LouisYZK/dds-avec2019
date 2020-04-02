python start.py --mode extract --feature boaw_mfcc &
python start.py --mode extract --feature boaw_egemaps &
python start.py --mode extract --feature bovw_pose_gaze_faus &

ps -ef |grep start.py | awk '{print $2}' | xargs kill