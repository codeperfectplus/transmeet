from pathlib import Path

def get_audio_size_mb(audio_segment):
    return len(audio_segment.raw_data) / (1024 * 1024)

def export_temp_wav(chunk, prefix, index):
    filename = f"{prefix}_chunk_{index}.wav"
    chunk.export(filename, format="wav")
    return filename

def split_audio_by_target_size(audio, target_mb):
    """Split audio into chunks of approx. target MB without exceeding max size."""
    target_bytes = target_mb * 1024 * 1024
    total_duration_ms = len(audio)
    chunk_duration_ms = (target_bytes / len(audio.raw_data)) * total_duration_ms

    chunks = []
    start = 0
    while start < total_duration_ms:
        end = min(start + int(chunk_duration_ms), total_duration_ms)
        chunk = audio[start:end]

        while len(chunk.raw_data) > target_bytes:
            end -= 1
            chunk = audio[start:end]

        chunks.append(chunk)
        start = end

    return chunks
