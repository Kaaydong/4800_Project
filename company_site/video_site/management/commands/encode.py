import subprocess
import os
import json
from django.core.management.base import BaseCommand, CommandError

# https://www.youtube.com/watch?v=5q1ElZh90QQ

class Command(BaseCommand):
    help = 'Optimize Video'

    def handle(self, *args, **kwargs):
        try:
            input_video_path = r"C:\Users\gippy\Desktop\mov\you-know-im-from.mp4"
            output_directory = os.path.join(os.path.dirname(input_video_path), 'hls_output')
            os.makedirs(output_directory, exist_ok=True)
            output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
            output_hls_path = os.path.join(output_directory, output_filename)

            # getting video duration/length

            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                
                input_video_path
            ]

            # Use ffmpeg to create HLS segments
            cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-c:v', 'h264',
                '-c:a', 'aac',
                '-hls_time', '5',
                '-hls_list_size', '0',
                "-hls_base_url", "{{ dynamic_path }}/",
                "-movflags", "+faststart",
                '-y',
                output_hls_path
            ]
            subprocess.run(cmd, check=True)


        except Exception as e:
            raise CommandError(e)
