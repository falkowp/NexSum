import io
import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock

from src.transcription.transcriber import _transcribe_with_whispercpp, convert_to_wav_16k_mono
from pydub import AudioSegment


def make_dummy_audio():
    # create 1 second of silence as AudioSegment
    return AudioSegment.silent(duration=1000).set_frame_rate(16000).set_channels(1)


def test_whispercpp_requires_model_env(tmp_path):
    if 'WHISPER_CPP_MODEL' in os.environ:
        del os.environ['WHISPER_CPP_MODEL']
    with pytest.raises(RuntimeError):
        _transcribe_with_whispercpp(make_dummy_audio())


@patch('subprocess.run')
def test_whispercpp_calls_binary(mock_run, tmp_path):
    os.environ['WHISPER_CPP_MODEL'] = str(tmp_path / 'ggml-small.bin')
    # Create a fake model file
    (tmp_path / 'ggml-small.bin').write_bytes(b'FAKE')

    fake_completed = subprocess.CompletedProcess(args=['main'], returncode=0, stdout='transcribed text')
    mock_run.return_value = fake_completed

    result = _transcribe_with_whispercpp(make_dummy_audio())
    assert 'transcribed text' in result
    # Ensure subprocess was called with expected args
    assert mock_run.called
    called_args = mock_run.call_args[0][0]
    assert '-m' in called_args
    assert '-f' in called_args


@patch('subprocess.run')
def test_whispercpp_handles_errors(mock_run, tmp_path):
    os.environ['WHISPER_CPP_MODEL'] = str(tmp_path / 'ggml-small.bin')
    (tmp_path / 'ggml-small.bin').write_bytes(b'FAKE')

    mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd=['main'], stderr='error')
    with pytest.raises(RuntimeError):
        _transcribe_with_whispercpp(make_dummy_audio())
