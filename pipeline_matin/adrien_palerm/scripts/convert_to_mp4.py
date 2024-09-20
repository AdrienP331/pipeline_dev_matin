"""
This script converts the input image sequence into a mp4 file
Youtube has good guidelines for encoding h264 files
https://support.google.com/youtube/answer/1722171?hl=en#zippy=%2Ccontainer-mp%2Caudio-codec-aac-lc%2Cvideo-codec-h%2Cframe-rate%2Cbitrate
"""

import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

import subprocess
import re
import json
import logging
from pathlib import Path
from typing import List
from glob import glob
from settings import get_settings


class ImgSequenceToMp4():
    """
    This class is used to transcode an image sequence into a mp4 file using ffmpeg
    An audio file may also be passed as an argument.
    """
    def __init__(self, input_path: str, audio_path:str=None) -> None:
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(
                "The input file does not exist : {}".format(self.input_path)
            )
        self.settings = get_settings()
        self.encoding_profile = self.get_encoding_profile()
        self.separator = self.get_separator()
        self.input_img_sequence = self.get_input_image_sequence()
        self.first_frame = self.get_first_frame()
        self.audio_path = Path(audio_path) if audio_path else None

    def parse_input_path(self) -> re.Match:
        """Analyses the input path to get the different parts of it"""
        path = self.input_path.as_posix()
        regex_pattern = re.compile(r"(?P<stem>^.+?)(?P<separator_before>\.|_)(?P<frame_number>\d+)\.(?P<extension>.+)")
        match = re.match(regex_pattern, path)
        if not match:
            raise Exception('File did not match the patern "path/to/file(.|_)<frame_number>.<extension>"')
        return match

    def get_separator(self) -> str:
        """Returns the input path, formatted as an image sequence"""
        match = self.parse_input_path()
        return match.group("separator_before")

    def get_input_image_sequence(self) -> Path:
        """Returns the input path, formatted as an image sequence with the "%<2digits>d" notation"""
        match = self.parse_input_path()
        padding = len(match.group("frame_number"))
        frame_pattern = "%{}d".format(str(padding).zfill(2))
        path = (
            match.group("stem")
            + match.group("separator_before")
            + frame_pattern
            + "."
            + match.group("extension")
        )
        return Path(path)

    @property
    def output_path(self) -> Path:
        """Returns the path of the mp4 file to render out"""
        path = self.input_img_sequence.as_posix()
        path = path.split("%")[0]  # Split before frame pattern
        path = path[:-1]  # Remove separator
        path = Path(path).with_suffix(".mp4")
        path = path.parent.joinpath("mp4", path.parts[-1])
        return path

    def get_encoding_profile(self) -> dict:
        """
        Returns the contents of the profile.json file
        used as settings for the encoding
        """
        path = Path(__file__).parent.parent.joinpath("ffmpeg/mp4_profile.json")
        with path.open('r') as f:
            content = json.loads(f.read())
        return content

    @property
    def ffmpeg_path(self) -> Path:
        return Path(__file__).parent.parent.joinpath("ffmpeg/ffmpeg.exe")

    @property
    def ffmpeg_command(self) -> List[str]:
        """returns the ffmpeg command to run"""
        command = [self.ffmpeg_path.as_posix(), "-y"]

        framerate = self.settings["fps"]
        width = self.encoding_profile.get("width")
        height = self.encoding_profile.get("height")
        quality = self.encoding_profile.get("quality") # On a scale of 0-100
        video_bitrate = self.encoding_profile.get("video_bitrate")
            
        # Add inputs
        command += ["-framerate", framerate]
        command += ["-start_number", self.first_frame]
        command += ["-i", self.input_img_sequence.as_posix()]
        command += ["-r", framerate]

        if self.audio_path:
            command += ["-i", self.audio_path.as_posix()]

        # Configure video codec
        command += ["-vcodec", self.encoding_profile["video_codec"]]
        command += ["-pix_fmt", self.encoding_profile["pix_fmt"]]
        if quality != None:
            crf = 50 - (quality/2)
            command += ["-crf", crf]
        elif video_bitrate:
            command += ["-b:v", video_bitrate]
        
        # Configure audio codec
        command += ["-acodec", self.encoding_profile["audio_codec"]]
        command += ["-ar", self.encoding_profile["audio_sample_rate"]]

        # Configure output
        if width:
            command += ["-s", f"{width}x{height}"]
        
        # Output options
        command += ["-movflags", "+faststart"]
        command += ["-bf", "0"] # b_frames
        command += ["-video_track_timescale", int(framerate)*1000]

        # Set output path
        command += [self.output_path.as_posix()]
        return [str(c) for c in command]

    def transcode(self) -> Path:
        """Runs the transcoding of the input file using an ffmpeg subprocess"""
        # Remove existing output
        if self.output_path.exists():
            os.remove(self.output_path)
        
        # Create folder
        self.output_path.parent.mkdir(exist_ok=True, parents=True)

        # Run ffmpeg command
        logging.info("Executing command : \n%s", self.ffmpeg_command)
        subprocess.check_call(self.ffmpeg_command)
        return self.output_path

    def get_first_frame(self) -> int:
        """Returns the first frame of the image sequence as an integer"""
        pattern = self.input_img_sequence.as_posix().replace(r"%04d", "*")
        first_frame = sorted(glob(pattern))[0]
        first_frame = first_frame.rsplit(".", 1)[0].rsplit(self.separator, 1)[-1]
        return int(first_frame)

class VideoToMp4():
    """
    This class is used to transcode a video into a mp4 file using ffmpeg
    An audio file may also be passed as an argument.
    """
    def __init__(self, input_path: str, audio_path:str=None) -> None:
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(
                "The input file does not exist : {}".format(self.input_path)
            )
        self.settings = get_settings()
        self.encoding_profile = self.get_encoding_profile()
        self.audio_path = Path(audio_path) if audio_path else None

    @property
    def output_path(self) -> Path:
        """Returns the path of the mp4 file to render out"""
        path = self.input_path.as_posix()
        path = Path(path).with_suffix(".mp4")
        path = path.parent.joinpath("mp4", path.parts[-1])
        return path

    def get_encoding_profile(self) -> dict:
        """
        Returns the contents of the profile.json file
        used as settings for the encoding
        """
        path = Path(__file__).parent.parent.joinpath("ffmpeg/mp4_profile.json")
        with path.open('r') as f:
            content = json.loads(f.read())
        return content

    @property
    def ffmpeg_path(self) -> Path:
        return Path(__file__).parent.parent.joinpath("ffmpeg/ffmpeg.exe")

    @property
    def ffmpeg_command(self) -> List[str]:
        """returns the ffmpeg command to run"""
        command = [self.ffmpeg_path.as_posix(), "-y"]
        framerate = self.settings["fps"]
        width = self.encoding_profile.get("width")
        height = self.encoding_profile.get("height")
        quality = self.encoding_profile.get("quality") # On a scale of 0-100
        video_bitrate = self.encoding_profile.get("video_bitrate")
            
        # Add inputs
        command += ["-i", self.input_path.as_posix()]
        command += ["-r", framerate]

        if self.audio_path:
            command += ["-i", self.audio_path.as_posix()]

        # Configure video codec
        command += ["-vcodec", self.encoding_profile["video_codec"]]
        command += ["-pix_fmt", self.encoding_profile["pix_fmt"]]
        if quality != None:
            crf = 50 - (quality/2)
            command += ["-crf", crf]
        elif video_bitrate:
            command += ["-b:v", video_bitrate]
        
        # Configure audio codec
        command += ["-acodec", self.encoding_profile["audio_codec"]]
        command += ["-ar", self.encoding_profile["audio_sample_rate"]]

        # Configure output
        if width:
            command += ["-s", f"{width}x{height}"]
        
        # Output options
        command += ["-movflags", "+faststart"]
        command += ["-bf", "0"] # b_frames
        command += ["-video_track_timescale", int(framerate)*1000]

        # Set output path
        command += [self.output_path.as_posix()]
        return [str(c) for c in command]

    def transcode(self) -> Path:
        """Runs the transcoding of the input file using an ffmpeg subprocess"""
        # Remove existing output
        if self.output_path.exists():
            os.remove(self.output_path)
        
        # Create folder
        self.output_path.parent.mkdir(exist_ok=True, parents=True)

        # Run ffmpeg command
        logging.info("Executing command : \n%s", self.ffmpeg_command)
        subprocess.check_call(self.ffmpeg_command)
        return self.output_path

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    if len(sys.argv) == 1:
        raise Exception("This script takes at least one argument : the input's path")

    for input_path in sys.argv[1:]:
        input_path = Path(input_path)
        if input_path.suffix.lower() in [".png", ".jpeg", ".jpg", ".exr", ".tiff", ".tif", ".tga"]:
            transcoder = ImgSequenceToMp4(input_path=input_path)
        else:
            transcoder = VideoToMp4(input_path=input_path)
        transcoder.transcode()        
