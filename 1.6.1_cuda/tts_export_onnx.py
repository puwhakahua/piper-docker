# source:
# https://github.com/OHF-Voice/piper1-gpl/issues/148#issuecomment-3711726072

import torch
import torch.serialization
from pathlib import PosixPath

# Fix 1: PyTorch 2.6+ compatibility - Add PosixPath to safe globals
torch.serialization.add_safe_globals([PosixPath])

# Fix 2: Patch torch.onnx.export to use legacy exporter
_original_onnx_export = torch.onnx.export

def _patched_onnx_export(*args, **kwargs):
    kwargs['dynamo'] = False
    return _original_onnx_export(*args, **kwargs)

torch.onnx.export = _patched_onnx_export

# Run piper's export with patches applied
from piper.train.export_onnx import main

if __name__ == "__main__":
    main()

