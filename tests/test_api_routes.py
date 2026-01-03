import io
import pytest

from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_summarize_success(monkeypatch, client):
    def fake_summarize_text(text, content_type=None):
        return {'content_type': 'general', 'summary': 'short summary', 'metadata': {}, 'success': True}

    monkeypatch.setattr('backend.services.summarization_service.summarize_text', fake_summarize_text)

    resp = client.post('/api/summarize', json={'text': 'Hello world'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert data['data']['summary'] == 'short summary'


def test_summarize_missing_text(client):
    resp = client.post('/api/summarize', json={})
    assert resp.status_code == 400


def test_transcribe_success(monkeypatch, client):
    def fake_transcribe(audio_bytes):
        return ('raw transcript', 'polished transcript')

    monkeypatch.setattr('backend.services.transcription_service.transcribe_audio_bytes', fake_transcribe)

    data = {
        'audio': (io.BytesIO(b'FAKE'), 'test.wav')
    }
    resp = client.post('/api/transcribe', data=data, content_type='multipart/form-data')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert data['data']['raw_transcript'] == 'raw transcript'


def test_transcribe_unsupported_extension(client):
    data = {
        'audio': (io.BytesIO(b'FAKE'), 'test.txt')
    }
    resp = client.post('/api/transcribe', data=data, content_type='multipart/form-data')
    assert resp.status_code == 415
