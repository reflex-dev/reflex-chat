from typing import List, Dict
import os
import requests
import json

from openai import OpenAI
import reflex as rx

import asyncio

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class QuestionAnswer(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

TRIGGER_KEYWORD = "SERVICE ORDER INFORMATION"

TEMPERATURE = 0

DEFAULT_CHATS = {
    "Demo Request": [],
}

DEFAULT_REQUEST_HISTORY = {
    "Demo Request": False,
}

ASSISTANT_SYSTEM_PROMPT = """
You are an assistant focused on service management requests from tenants. Your goal is to gather information to put together in a formal service order form for a property manager. 

===========
You will follow these guidelines:
1. If there is not enough suitable information form a tenant you will prompt follow-up questions, if needed, till you have suitable information of the issue / situation. 
2. Try to limit the amount of follow-up questions required. 
3. Ask one follow-up question at a time if needed. 
4. If you do ask follow-up questions you are allowed a MAXIMUM of 3 follow-up questions. 
5. Once you have suitable information start your output message as ***SERVICE ORDER INFORMATION**:
===========

===========
Here is an example of a suitable service order: 
I am reaching out to report a maintenance issue that has recently occurred in my apartment, specifically concerning a broken window in the living room. The damage was caused by a storm, where a fallen tree branch impacted the windowpane, resulting in its shattering. This window is located on the east side of the building, facing the courtyard. Currently, the broken glass presents a significant safety hazard, and the opening has left the apartment vulnerable to environmental elements such as wind and rain. While the glass is extensively fractured, the window frame remains largely undamaged. To mitigate immediate risks, I have temporarily covered the window with plastic sheeting. This measure is intended to prevent further damage from weather conditions and to maintain safety within the apartment.
===========

===========
Here is an example of a non-suitable service order:
I have a broken window. 
===========

FOLLOW THESE GUIDELINES, OR YOU WILL BE FIRED.
"""


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
        self.toggle_modal()
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question
        async for value in model(question):
            yield value

        last_message = self.get_context()

        if TRIGGER_KEYWORD in last_message:
            # await self.process_maintenance()
            self.toggle_form_processing()
            # await asyncio.sleep(10)
            # import time; time.sleep(5)
            self.toggle_modal()
            # self.toggle_form_processing()

    async def process_maintenance(self):
        pass

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
        messages = [{"role": "system", "content": ASSISTANT_SYSTEM_PROMPT}]
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
