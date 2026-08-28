import os
import argparse
from typing import Dict, Any
import traceback

from piper import PiperVoice
from sfp import Poller
from tts_common import load_model, tts_to_file, tts_args


SUPPORTED_EXTS = [".txt"]
""" supported file extensions (lower case). """


def process_text(fname, output_dir, poller):
    """
    Method for processing a text file.

    :param fname: the text to generate audio from
    :type fname: str
    :param output_dir: the directory to write the audio to
    :type output_dir: str
    :param poller: the Poller instance that called the method
    :type poller: Poller
    :return: the list of generated output files
    :rtype: list
    """
    result = []

    try:
        with open(fname, "r") as fp:
            lines = fp.readlines()
        text = "\n".join(lines).strip()
        fname_out = os.path.join(output_dir, os.path.splitext(os.path.basename(fname))[0] + ".wav")
        fname_out = tts_to_file(poller.params.voice, poller.params.synth_args, text, fname_out)
        result.append(fname_out)
    except KeyboardInterrupt:
        poller.keyboard_interrupt()
    except:
        poller.error("Failed to process text: %s\n%s" % (fname, traceback.format_exc()))
    return result


def tts_from_files(voice: PiperVoice, synth_args: Dict[str, Any], input_dir, output_dir, tmp_dir,
                   poll_wait=1.0, continuous=False, use_watchdog=False, watchdog_check_interval=10.0,
                   delete_input=False, verbose=False, quiet=False):
    """
    Method for generating audio from text files.

    :param voice: the piper voice model
    :type voice: PiperVoice
    :param synth_args: the arguments for the speech synthesis
    :type synth_args: dict
    :param input_dir: the directory with the text files
    :type input_dir: str
    :param output_dir: the output directory to move the text files to and store the predictions
    :type output_dir: str
    :param tmp_dir: the temporary directory to store the predictions until finished, use None if not to use
    :type tmp_dir: str
    :param poll_wait: the amount of seconds between polls when not in watchdog mode
    :type poll_wait: float
    :param continuous: whether to poll continuously
    :type continuous: bool
    :param use_watchdog: whether to react to file creation events rather than use fixed-interval polling
    :type use_watchdog: bool
    :param watchdog_check_interval: the interval for the watchdog process to check for files that were missed due to potential race conditions
    :type watchdog_check_interval: float
    :param delete_input: whether to delete the input text files rather than moving them to the output directory
    :type delete_input: bool
    :param verbose: whether to output more logging information
    :type verbose: bool
    :param quiet: whether to suppress output
    :type quiet: bool
    """

    poller = Poller()
    poller.input_dir = input_dir
    poller.output_dir = output_dir
    poller.tmp_dir = tmp_dir
    poller.extensions = SUPPORTED_EXTS
    poller.delete_input = delete_input
    poller.progress = not quiet
    poller.verbose = verbose
    poller.process_file = process_text
    poller.poll_wait = poll_wait
    poller.continuous = continuous
    poller.use_watchdog = use_watchdog
    poller.watchdog_check_interval = watchdog_check_interval
    poller.params.voice = voice
    poller.params.synth_args = synth_args
    poller.poll()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Piper - TTS", prog="piper_tts_poll", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='Path to the trained model (.onnx file)', required=True, default=None)
    parser.add_argument('--config', help='Path to the config file', required=True, default=None)
    parser.add_argument('--use_cuda', action='store_true', help='Whether to use the CUDA backend', required=False)
    parser.add_argument('--speaker_id', type=int, help='The speaker ID to use, None for single-speaker', required=False, default=None)
    parser.add_argument('--length_scale', type=float, help='The phoneme length', required=False, default=None)
    parser.add_argument('--noise_scale', type=float, help='The generator noise', required=False, default=None)
    parser.add_argument('--noise_w', type=float, help='The phoneme width noise', required=False, default=None)
    parser.add_argument('--prediction_in', help='Path to the text files to process', required=True, default=None)
    parser.add_argument('--prediction_out', help='Path to the output csv files folder', required=True, default=None)
    parser.add_argument('--prediction_tmp', help='Path to the temporary csv files folder', required=False, default=None)
    parser.add_argument('--poll_wait', type=float, help='poll interval in seconds when not using watchdog mode', required=False, default=1.0)
    parser.add_argument('--continuous', action='store_true', help='Whether to continuously load text files and perform prediction', required=False, default=False)
    parser.add_argument('--use_watchdog', action='store_true', help='Whether to react to file creation events rather than performing fixed-interval polling', required=False, default=False)
    parser.add_argument('--watchdog_check_interval', type=float, help='check interval in seconds for the watchdog', required=False, default=10.0)
    parser.add_argument('--delete_input', action='store_true', help='Whether to delete the input text files rather than move them to --prediction_out directory', required=False, default=False)
    parser.add_argument('--verbose', action='store_true', help='Whether to output more logging info', required=False, default=False)
    parser.add_argument('--quiet', action='store_true', help='Whether to suppress output', required=False, default=False)
    parsed = parser.parse_args()

    try:
        voice = load_model(parsed.model, parsed.config, use_cuda=parsed.use_cuda)
        synth_args = tts_args(speaker_id=parsed.speaker_id, length_scale=parsed.length_scale,
                              noise_scale=parsed.noise_scale, noise_w=parsed.noise_w)

        # Performing the prediction and producing the predictions files
        tts_from_files(voice, synth_args, parsed.prediction_in, parsed.prediction_out, parsed.prediction_tmp,
                       continuous=parsed.continuous, use_watchdog=parsed.use_watchdog,
                       watchdog_check_interval=parsed.watchdog_check_interval, delete_input=parsed.delete_input,
                       verbose=parsed.verbose, quiet=parsed.quiet)

    except Exception as e:
        print(traceback.format_exc())
