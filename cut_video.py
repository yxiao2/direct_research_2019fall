from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

# ffmpeg_extract_subclip("output_2.mp4", 0,20,targetname="output_3.mp4")
my_clip = VideoFileClip("project_video.mp4")
new_clip = my_clip.subclip(10,20)
new_clip.write_videofile("input_7.mp4")
# new_clip1 = my_clip.subclip(10,20)
# new_clip1.write_videofile("output_4.mp4")
# new_clip2 = my_clip.subclip(20,30)
# new_clip2.write_videofile("output_5.mp4")