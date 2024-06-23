import os
import reflex as rx
from openai import OpenAI
from dotenv import load_dotenv
from reflex.state import BaseState
import PIL
import requests
import torch
from io import BytesIO
from diffusers import LEditsPPPipelineStableDiffusion
from diffusers.utils import load_image
from leditspp.scheduling_dpmsolver_multistep_inject import DPMSolverMultistepSchedulerInject
from leditspp import StableDiffusionPipeline_LEDITS
from typing import Union
import numpy as np


load_dotenv()  # This loads the environment variables from the .env file

# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}


def load_image_fromurl(image: Union[str, PIL.Image.Image]):
    """
    Loads `image` to a PIL Image.

    Args:
        image (`str` or `PIL.Image.Image`):
            The image to convert to the PIL Image format.
    Returns:
        `PIL.Image.Image`:
            A PIL Image.
    """
    if isinstance(image, str):
        if image.startswith("http://") or image.startswith("https://"):
            image = PIL.Image.open(requests.get(image, stream=True).raw)
        elif os.path.isfile(image):
            image = PIL.Image.open(image)
        else:
            raise ValueError(
                f"Incorrect path or url, URLs must start with `http://` or `https://`, and {image} is not a valid path"
            )
    elif isinstance(image, PIL.Image.Image):
        image = image
    else:
        raise ValueError(
            "Incorrect format used for image. Should be an url linking to an image, a local path, or a PIL image."
        )
    image = PIL.ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    return image


def image_grid(imgs, rows, cols, spacing = 20):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size

    grid = PIL.Image.new('RGBA', size=(cols * w + (cols-1)*spacing, rows * h + (rows-1)*spacing ), color=(255,255,255,0))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=( i // rows * (w+spacing), i % rows * (h+spacing)))
        #print(( i // rows * w, i % rows * h))
    return grid


class ImageGenerator:
    def __init__(self):
        #self.model_name = "stabilityai/stable-diffusion-3-medium-diffusers"  # Model name
        self.model_name = "runwayml/stable-diffusion-v1-5"  # Model name
        self.pipe = StableDiffusionPipeline_LEDITS.from_pretrained(self.model_name,safety_checker = None,)
        self.pipe.scheduler = DPMSolverMultistepSchedulerInject.from_pretrained(self.model_name, subfolder="scheduler"
                                                             , algorithm_type="sde-dpmsolver++", solver_order=2)
        self.pipe = self.pipe.to("mps")  # TODO: CHANGE THIS DEPENDING ON HARDWARE (mps, cuda, intel)
        self.image = None  # Placeholder for your initial image

    async def generate_new_image(self, prompt: str):
        """
        Input: prompt (str) - Text prompt for generating the new image.
        Result: Generates a new image based on the prompt and sets it to the global image.
        Output: The new image
        """
        if self.image is None:
            raise ValueError("No initial image is set.")

        im = np.array(self.image)[:, :, :3]

        gen = torch.manual_seed(42)
        with torch.no_grad():
            _ = self.pipe.invert(im, num_inversion_steps=50, generator=gen, verbose=True, skip=0.15)
            edited_image = self.pipe(editing_prompt=[prompt],
                                        edit_threshold=[.7, .9],
                                        edit_guidance_scale=[3, 4],
                                        reverse_editing_direction=[False, False],
                                        use_intersect_mask=True, )

            # Update the global image
            self.image = edited_image.images[0]

        return self.image

    def set_initial_image(self, image_path: str = None, image_url: str = None):
        """
        Sets the initial image from a file path or a URL.
        """
        if image_path:
            self.image = PIL.Image.open(image_path).convert("RGB")
        elif image_url:
            self.image = load_image_fromurl(image_url).resize((512, 512))
        else:
            raise ValueError("Either image_path or image_url must be provided.")


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def __init__(
            self,
            *args,
            parent_state: BaseState | None = None,
            init_substates: bool = True,
            _reflex_internal_init: bool = False,
            **kwargs,
    ):
        super().__init__(args, parent_state, init_substates, _reflex_internal_init, kwargs)
        self.image_generator = ImageGenerator()

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            question: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named Reflex. Respond in markdown.",
            }
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                # Ensure answer_text is not None before concatenation
                if answer_text is not None:
                    self.chats[self.current_chat][-1].answer += answer_text
                else:
                    # Handle the case where answer_text is None, perhaps log it or assign a default value
                    # For example, assigning an empty string if answer_text is None
                    answer_text = ""
                    self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False

    async def set_image_context(self, form_data: dict[str, str]):
        """
        Input: Image
        Result: The global image is set to the image provided.
                Other functions using the global image will now use this image.
        Output: None
        """
        image_url = form_data.get("image_url")
        image_path = form_data.get("image_path")

        if image_url:
            self.image_generator.set_initial_image(image_url=image_url)
        elif image_path:
            self.image_generator.set_initial_image(image_path=image_path)
        else:
            raise ValueError("Either image_url or image_path must be provided.")

        yield

    async def generate_new_image(self, prompt: str):
        """
        Input: prompt (str) - Text prompt for generating the new image.
        Result: Based on the prompt, make alterations to the image and set the global image to the new image.
        Output: The new image
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        new_image = await self.image_generator.generate_new_image(prompt)
        yield new_image

