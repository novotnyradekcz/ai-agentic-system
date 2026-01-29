"""
Audio Transcription Module
Transcribes audio files to text using OpenAI Whisper.
"""

import whisper
import torch
from pathlib import Path
from typing import Optional, Dict
import warnings
import tempfile
import os

warnings.filterwarnings("ignore")


class AudioTranscriber:
    """Transcribes audio files using OpenAI Whisper model."""
    
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.mp4']
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the audio transcriber.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       - tiny: fastest, least accurate
                       - base: good balance (default)
                       - small: better accuracy
                       - medium/large: best accuracy, slower
        """
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model '{model_size}' on {self.device}...")
        self.model = whisper.load_model(model_size, device=self.device)
        print("Model loaded successfully!")
    
    def extract_audio_from_video(self, video_path: str) -> str:
        """
        Extract audio from MP4 video file.
        
        Args:
            video_path: Path to the MP4 video file
        
        Returns:
            Path to the extracted audio file (temporary WAV file)
        """
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            raise ImportError(
                "moviepy is required for MP4 support. "
                "Install it with: pip install moviepy"
            )
        
        video_path = Path(video_path)
        print(f"Extracting audio from video: {video_path.name}")
        
        # Create temporary WAV file
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        try:
            # Extract audio
            video = VideoFileClip(str(video_path))
            video.audio.write_audiofile(
                temp_audio_path,
                codec='pcm_s16le',
                verbose=False,
                logger=None
            )
            video.close()
            
            print(f"✓ Audio extracted to temporary file")
            return temp_audio_path
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            raise Exception(f"Failed to extract audio from video: {e}")
    
    def transcribe_audio(
        self, 
        audio_path: str, 
        language: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, any]:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'en' for English). None for auto-detect.
            verbose: Whether to print progress
        
        Returns:
            Dictionary containing transcription results
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if audio_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported audio format: {audio_path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        if verbose:
            print(f"\nTranscribing: {audio_path.name}")
            print(f"Model: {self.model_size}")
        
        # Handle MP4 files by extracting audio first
        temp_audio_path = None
        transcribe_path = str(audio_path)
        
        if audio_path.suffix.lower() == '.mp4':
            temp_audio_path = self.extract_audio_from_video(str(audio_path))
            transcribe_path = temp_audio_path
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(
                transcribe_path,
                language=language,
                verbose=False
            )
            
            if verbose:
                detected_lang = result.get('language', 'unknown')
                print(f"Detected language: {detected_lang}")
                print(f"Transcription length: {len(result['text'])} characters")
            
            return {
                'text': result['text'],
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'source': str(audio_path)
            }
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise
        finally:
            # Clean up temporary audio file if it was created
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    
    def transcribe_with_timestamps(self, audio_path: str) -> list:
        """
        Transcribe audio and return segments with timestamps.
        
        Args:
            audio_path: Path to the audio file
        
        Returns:
            List of dictionaries with text and timestamps
        """
        result = self.transcribe_audio(audio_path, verbose=False)
        
        segments = []
        for segment in result['segments']:
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return segments


if __name__ == "__main__":
    # Example usage
    audio_path = "../data/sample_audio.mp3"
    
    try:
        # Initialize transcriber with 'base' model (good balance of speed/accuracy)
        transcriber = AudioTranscriber(model_size="base")
        
        # Transcribe audio
        result = transcriber.transcribe_audio(audio_path)
        
        print(f"\nTranscription preview (first 500 chars):")
        print(result['text'][:500])
        
    except FileNotFoundError:
        print(f"\nPlease place an audio file at: {audio_path}")
        print("Supported formats: .mp3, .wav, .m4a, .flac, .ogg, .wma, .mp4")
