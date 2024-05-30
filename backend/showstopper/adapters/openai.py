from typing import List
import os

from transformers import (
    CLIPImageProcessor,
    CLIPVisionModelWithProjection,
    CLIPTokenizer,
    CLIPTextModelWithProjection,
)
from PIL import Image
import openai
import torch

from showstopper.audio.ports import AudioTranscriber, TextGenerator
from showstopper.images.ports import ImageEmbedder


class CLIPImageTextEmbedder(ImageEmbedder):
    def __init__(self) -> None:
        model_path = "/models/clip-vit-base-patch32"

        model_name = (
            model_path if os.path.exists(model_path) else "openai/clip-vit-base-patch32"
        )

        # TODO: figure out how to load models on instance
        self.vision_processor = CLIPImageProcessor.from_pretrained(model_name)
        self.vision_model = CLIPVisionModelWithProjection.from_pretrained(model_name)

        self.tokenizer = CLIPTokenizer.from_pretrained(model_name)
        self.text_model = CLIPTextModelWithProjection.from_pretrained(model_name)

    def embed_images(self, images: List[str]) -> List[List[float]]:
        files = [Image.open(image) for image in images]

        encoded_image_input = self.vision_processor(images=files, return_tensors="pt")

        for file in files:
            file.close()

        with torch.no_grad():
            image_outputs = self.vision_model(**encoded_image_input)

        return image_outputs.image_embeds.detach().numpy()

    def embed_text(self, text: List[str]) -> List[List[float]]:
        with torch.no_grad():
            encoded_text_input = self.tokenizer(text, return_tensors="pt", padding=True)
            text_output = self.text_model(**encoded_text_input)

        return text_output.text_embeds.detach().numpy()


class OpenAIAdapter(AudioTranscriber, TextGenerator):
    def __init__(self, open_ai_key: str) -> None:
        self.client = openai.OpenAI(
            api_key=open_ai_key,
        )

    def generate_text_with_content(self, prompt: str, content: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    # "content": "You are a helpful video transcriber. You will be given the subtitles of a video and you need to convert it into text. Don't make things up. Just write what you hear. The user will provide you with the subtitles. Generate a summary of what is being said in the subtitles. The summary should not acknowledge the subtitles. Make sure to write in your own words and understand the context and meaning of the subtitles. Give out minimum 6 sentences.",
                    "content": prompt,
                },
                {"role": "user", "content": content},
            ],
        )

        response = completion.choices[0].message.content

        if response is None:
            raise ValueError("Failed to generate text response")

        return response

    def generate_audio_transcript(self, audio_filepath: str) -> str:
        with open(audio_filepath, "rb") as fp:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", file=fp, response_format="srt"
            )

            return transcription
