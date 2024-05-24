from abc import ABC, abstractmethod


class AudioTranscriber(ABC):
    @abstractmethod
    def generate_audio_transcript(self, audio_filepath: str) -> str:
        raise NotImplementedError


class TextGenerator(ABC):
    @abstractmethod
    def generate_text_with_content(self, prompt: str, content: str) -> str:
        raise NotImplementedError
