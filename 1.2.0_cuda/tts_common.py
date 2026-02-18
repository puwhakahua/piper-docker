import io
from typing import Dict, Any

from piper import PiperVoice
import wave


def load_model(model: str, config: str, use_cuda: bool = False) -> PiperVoice:
    """
    Loads the model from disk.

    :param model: the path to the ONNX model
    :type model: str
    :param config: the path to the JSON configuration file
    :type config: str
    :param use_cuda: whether to use CUDA or not
    :type use_cuda: bool
    :return: the voice model
    :rtype: PiperVoice
    """
    return PiperVoice.load(model, config_path=config, use_cuda=use_cuda)


def tts_args(speaker_id: int = None, length_scale: float = None, noise_scale: float = None,
             noise_w: float = None, sentence_silence: float = 0.0) -> Dict[str, Any]:
    """
    Assembles the TTS arguments

    :param speaker_id: the speaker ID to use, None for single-speaker
    :type speaker_id: int
    :param length_scale: the phoneme length
    :type length_scale: float or None
    :param noise_scale: the generator noise
    :type noise_scale: float or None
    :param noise_w: the phoneme width noise
    :type noise_w: float
    :param sentence_silence: the number of seconds of silence after each sentence
    :type sentence_silence: float
    """
    return {
        "speaker_id": speaker_id,
        "length_scale": length_scale,
        "noise_scale": noise_scale,
        "noise_w": noise_w,
        "sentence_silence": sentence_silence,
    }


def tts_to_file(voice: PiperVoice, synthesize_args: Dict[str, Any], text: str, output: str) -> str:
    """
    Generates a WAV from the text input.

    :param voice: the voice model to use
    :type voice: PiperVoice
    :param synthesize_args: the arguments for the speech generation
    :type synthesize_args: dict
    :param text: the text to generate audio from
    :type text: str
    :param output: the WAV file to write to
    :type output: str
    :return: the file that was generated
    :rtype: str
    """
    with wave.open(output, "wb") as fp:
        voice.synthesize(text, fp, **synthesize_args)
    return output


def tts_to_data(voice: PiperVoice, synthesize_args: Dict[str, Any], text: str) -> bytes:
    """
    Generates a WAV as a bytes data structure from the text input.

    :param voice: the voice model to use
    :type voice: PiperVoice
    :param synthesize_args: the arguments for the speech generation
    :type synthesize_args: dict
    :param text: the text to generate audio from
    :type text: str
    :return: the bytes of the WAV
    :rtype: bytes
    """
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as fp:
        voice.synthesize(text, fp, **synthesize_args)
    return buffer.getvalue()
