from datetime import datetime
import numpy as np
import traceback

from rdh import Container, MessageContainer, create_parser, configure_redis, run_harness, log
from tts_common import load_model, tts_to_data, tts_args


def process_text(msg_cont):
    """
    Processes the message container, loads the text from the message and forwarding the generated WAV.

    :param msg_cont: the message container to process
    :type msg_cont: MessageContainer
    """
    config = msg_cont.params.config

    try:
        start_time = datetime.now()

        text = msg_cont.message['data'].decode("utf-8")
        out_data = tts_to_data(config.voice, config.synth_args, text)
        msg_cont.params.redis.publish(msg_cont.params.channel_out, out_data)

        if config.verbose:
            log("process_text - generated WAV published: %s" % msg_cont.params.channel_out)
            end_time = datetime.now()
            processing_time = end_time - start_time
            processing_time = int(processing_time.total_seconds() * 1000)
            log("process_text - finished processing text: %d ms" % processing_time)

    except KeyboardInterrupt:
        msg_cont.params.stopped = True
    except:
        log("process_text - failed to process: %s" % traceback.format_exc())


if __name__ == '__main__':
    parser = create_parser('Piper - TTS (Redis)', prog="piper_tts_redis", prefix="redis_")
    parser.add_argument('--model', help='Path to the trained model (.onnx file)', required=True, default=None)
    parser.add_argument('--config', help='Path to the config file', required=True, default=None)
    parser.add_argument('--use_cuda', action='store_true', help='Whether to use the CUDA backend', required=False)
    parser.add_argument('--speaker_id', type=int, help='The speaker ID to use, None for single-speaker', required=False, default=None)
    parser.add_argument('--length_scale', type=float, help='The phoneme length', required=False, default=None)
    parser.add_argument('--noise_scale', type=float, help='The generator noise', required=False, default=None)
    parser.add_argument('--noise_w', type=float, help='The phoneme width noise', required=False, default=None)
    parser.add_argument('--verbose', action='store_true', help='Whether to output more logging info', required=False, default=False)
    parsed = parser.parse_args()

    try:
        voice = load_model(parsed.model, parsed.config, use_cuda=parsed.use_cuda)
        synth_args = tts_args(speaker_id=parsed.speaker_id, length_scale=parsed.length_scale,
                              noise_scale=parsed.noise_scale, noise_w=parsed.noise_w)

        config = Container()
        config.voice = voice
        config.synth_args = synth_args
        config.verbose = parsed.verbose

        params = configure_redis(parsed, config=config)
        run_harness(params, process_text)

    except Exception as e:
        print(traceback.format_exc())
