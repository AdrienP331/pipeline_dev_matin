"""
This script converts the input image sequence into a mov file (codec prores4444)
"""

import sys
import os
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

import subprocess
import re
import logging
from pathlib import Path
from typing import List
from glob import glob
from settings import get_settings

class ImgSequenceToProres4444():
    """
    This class is used to transcode an image sequence into a mov file using ffmpeg
    An audio file may also be passed as an argument.
    """
    def __init__(self, input_path: str, audio_path:str=None) -> None:
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(
                "The input file does not exist : {}".format(self.input_path)
            )
        self.settings = get_settings()
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
        """Returns the path of the mov file to render out"""
        path = self.input_img_sequence.as_posix()
        path = path.split("%0")[0]  # Split before frame pattern
        path = path[:-1]  # Remove separator
        path = path + ".mov"
        path = Path(path)
        path = path.parent.joinpath("Prores4444", path.name)
        return path

    @property
    def ffmpeg_path(self) -> Path:
        return Path(__file__).parent.parent.joinpath("ffmpeg/ffmpeg.exe")

    @property
    def ffmpeg_command(self) -> List[str]:
        """returns the ffmpeg command to run"""
        framerate = self.settings["fps"]
        command = ["ffmpeg", "-y"]
        
        # Configure video input
        command += ["-framerate", framerate]
        command += ["-start_number", self.first_frame]
        command += ["-i", self.input_img_sequence.as_posix()]
        command += ["-r", framerate]

        # Configure audio input
        if self.audio_path:
            command += ["-i {}".format(self.audio_path)]

        # Configure video codec
        command += ["-vcodec", "prores_ks"]  # Default prores encoder
        command += ["-profile:v", "4"]  # Profile 4444
        command += ["-pix_fmt", "yuv444p10le"]  # 10 bits 4444 Subsampling
        command += ["-vendor", "apl0"]
        command += ["-movflags", "faststart"]

        # Configure audio codec
        if self.audio_path:
            command += ["-c:a", "pcm_s16le"]
            command += ["-map", "0:0"]
            command += ["-map", "1:0"]
            command += ["-ar", "48000"]  # Audio sampling rate
            command += ["-sample_fmt", "s16"]  # Audio sample size

        # Set output path
        command.append(self.output_path.as_posix())
        return [str(part) for part in command]

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


class VideoToProres4444():
    """
    This class is used to transcode an video into a mov file using ffmpeg
    An audio file may also be passed as an argument.
    """
    def __init__(self, input_path: str, audio_path:str=None) -> None:
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(
                "The input file does not exist : {}".format(self.input_path)
            )
        self.settings = get_settings()
        self.audio_path = Path(audio_path) if audio_path else None

    @property
    def output_path(self) -> Path:
        """Returns the path of the mov file to render out"""
        path = input_path.with_suffix(".mov")
        path = path.parent.joinpath("Prores4444", path.name)
        return Path(path)

    @property
    def ffmpeg_path(self) -> Path:
        return Path(__file__).parent.parent.joinpath("ffmpeg/ffmpeg.exe")

    @property
    def ffmpeg_command(self) -> str:
        """returns the ffmpeg command to run"""
        command = ["ffmpeg", "-y"]
        
        # Configure video input
        command += ["-i", self.input_path.as_posix()]

        # Configure audio input
        if self.audio_path:
            command += ["-i {}".format(self.audio_path)]

        # Configure video codec
        command += ["-vcodec", "prores_ks"] # Default prores encoder
        command += ["-profile:v", "4"] # Profile 4444
        command += ["-pix_fmt", "yuv444p10le"] # 10 bits 4444 Subsampling
        command += ["-vendor", "apl0"]
        command += ["-movflags", "faststart"]

        # Configure audio codec
        if self.audio_path:
            command += ["-c:a", "pcm_s16le"]
            command += ["-map", "0:0"]
            command += ["-map", "1:0"]
            command += ["-ar", "48000"] # Audio sampling rate
            command += ["-sample_fmt", "s16"] # Audio sample size

        # Set output path
        command.append(self.output_path.as_posix())
        return [str(part) for part in command]

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
            transcoder = ImgSequenceToProres4444(input_path=input_path)
        else:
            transcoder = VideoToProres4444(input_path=input_path)
        transcoder.transcode()        
