from typing import List, Dict, Any
import os
import requests
import json

from pydantic import BaseModel
from openai import OpenAI
import reflex as rx

from webui.services import transform_maintenance_request
from .constants import (
    MODEL,
    TRIGGER_KEYWORD,
    TEMPERATURE,
    DEFAULT_CHATS,
    DEFAULT_REQUEST_HISTORY,
    SYSTEM_PROMPT,
    DEFAULT_MAINTENANCE_REQUEST,
)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class QuestionAnswer(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

class State(rx.State):
    """The app state."""

    # A Dict from the chat name to the list of questions and answers.
    chats: Dict[str, List[QuestionAnswer]] = DEFAULT_CHATS

    # Request history
    request_history: Dict[str, bool] = DEFAULT_REQUEST_HISTORY

    # The current chat name.
    current_chat = "Demo Request"

    # The current question.
    question: str

    # Whether we are processing the question.
    question_processing: bool = False

    # Whether we are processing the maintenace request.
    form_processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    api_type: str = "openai"

    maintenance_request_submitted: bool = False

    img: list[str]

    maintenance_request_data: Dict[Any, Any] = DEFAULT_MAINTENANCE_REQUEST

    def set_category(self, category: str):
        self.maintenance_request_data["CategoryId"] = category
    
    def set_subject(self, subject: str):
        self.maintenance_request_data["Subject"] = subject
        
    def set_description(self, description: str):
        self.maintenance_request_data["Description"] = description
    
    def set_priority(self, priority: str):
        self.maintenance_request_data["TaskPriority"] = priority
    
    @rx.var
    def priority(self) -> str:
        return self.maintenance_request_data["TaskPriority"]
    
    @rx.var
    def description(self) -> str:
        return self.maintenance_request_data["Description"]
    
    @rx.var
    def subject(self) -> str:
        return self.maintenance_request_data["Subject"]
    
    @rx.var
    def category(self) -> str:
        return self.maintenance_request_data["CategoryId"]
    
    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # FIX THE BELOW
        self.request_history[self.current_chat] = False
        self.maintenance_request_submitted = False

        # Toggle the modal.
        self.modal_open = False

    def set_maintenance_request_history(self, maintenance_request_submitted: bool):
        self.maintenance_request_submitted = maintenance_request_submitted
        self.request_history[self.current_chat] = maintenance_request_submitted

    def submit_maintenance_request(self):
        self.set_maintenance_request_history(True)
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_form_processing(self):
        """Toggle the new chat modal."""
        self.form_processing = not self.form_processing

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()
        self.set_maintenance_request_history(self.request_history.get(chat_name))

    @rx.var
    def chat_titles(self) -> List[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = f".web/public/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)

    async def process_question(self, form_data: Dict[str, str]):
        # Get the question from the form
        # if len(self.img) > 0:
        #     self.handle_upload()
        # self.toggle_modal()
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question
        async for value in model(question):
            yield value

    async def process_form(self):
        last_message = self.get_context()
        if TRIGGER_KEYWORD in last_message:
            self.form_processing = True
            await self.process_maintenance(last_message)
            self.toggle_modal()
            self.form_processing = False

    async def process(self, form_data: Dict[str, str]):
        async for response in self.process_question(form_data):
            yield response
        await self.process_form()

    @rx.var
    def maintenance_request(self): # -> MaintenanceRequest:
        return self.maintenance_request_data
        # return MaintenanceRequest(**self.maintenance_request_data)

    async def process_maintenance(self, form_data: str):
        maintenance_request = await transform_maintenance_request(form_data)
        maintenance_request = maintenance_request["data"]
        self.maintenance_request_data = maintenance_request
        return maintenance_request

    def get_context(self):
        """Get the combined context of question and answer from the current chat."""
        context = ""
        for qa in self.chats[self.current_chat]:
            context += qa.answer
        return context

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A Dict with the current question.
        """

        # Add the question to the list of questions.
        question_answer = QuestionAnswer(question=question, answer="")
        self.chats[self.current_chat].append(question_answer)

        # Clear the input and start the processing.
        self.question_processing = True
        yield

        # Build the messages.
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for question_answer in self.chats[self.current_chat]:
            messages.extend(
                (
                    {"role": "user", "content": question_answer.question},
                    {"role": "assistant", "content": question_answer.answer},
                )
            )
        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=TEMPERATURE, stream=True
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if answer_text := item.choices[0].delta.content:
                    self.chats[self.current_chat][-1].answer += answer_text
                yield

        # Toggle the processing flag.
        self.question_processing = False
