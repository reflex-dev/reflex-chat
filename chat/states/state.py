import os
import reflex as rx

from openai import OpenAI


# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


q1 = QA(
    question="How do I reverse a list in Python?",
    answer="To reverse a list in Python, you can use slicing. The slicing syntax [::-1] allows you to create a reversed copy of the list. For example, if you have a list `my_list = [1, 2, 3, 4, 5]`, `reversed_list = my_list[::-1]` will give you `[5, 4, 3, 2, 1]`. Slicing is efficient and concise for this operation, providing a straightforward way to reverse lists of any size.",
)

q2 = QA(
    question="What is a decorator in Python?",
    answer="A decorator in Python is a design pattern that allows you to dynamically alter the functionality of a function, method, or class without changing its source code. Decorators are implemented as functions themselves and typically take another function as an argument. They are often used to add behavior such as logging, authentication, or caching to existing functions or methods. For example, a decorator can wrap a function with additional functionality before and/or after the original function's execution, enhancing its behavior without modifying its core logic.",
)

q3 = QA(
    question="How do you handle exceptions in Python?",
    answer="In Python, exceptions are handled using try-except blocks. The code that may raise an exception is placed inside the try block. If an exception occurs during the execution of the try block, Python searches for an except block that matches the exception type. If a matching except block is found, its code is executed to handle the exception. You can also have multiple except blocks to handle different types of exceptions. Additionally, you can use a finally block which is executed whether an exception occurred or not, for cleanup actions. Example: \n\n```python\ntry:\n    # Code that may raise an exception\n    result = 10 / 0  # This will raise a ZeroDivisionError\nexcept ZeroDivisionError as e:\n    print('Error:', e)\nexcept Exception as e:\n    print('Other error:', e)\nfinally:\n    print('Cleanup code here')\n```\n",
)

q4 = QA(
    question="What are Python's main data types?",
    answer="Python supports several built-in data types: integers (int), floating-point numbers (float), strings (str), lists (list), tuples (tuple), dictionaries (dict), sets (set), and booleans (bool). These data types are used to store and manipulate different kinds of data. Integers are whole numbers, floats are numbers with decimal points, strings are sequences of characters enclosed in quotes, lists are ordered collections of items, tuples are ordered and immutable collections, dictionaries are unordered collections of key-value pairs, sets are unordered collections of unique items, and booleans represent truth values True or False.",
)

q5 = QA(
    question="How do you iterate over a dictionary in Python?",
    answer="In Python, you can iterate over a dictionary using a for loop. By default, iterating over a dictionary iterates over its keys. You can access both keys and values using the items() method. For example: \n\n```python\nmy_dict = {'a': 1, 'b': 2, 'c': 3}\nfor key in my_dict:\n    print(key, my_dict[key])  # This prints each key-value pair\n\n# Using items() method\nfor key, value in my_dict.items():\n    print(key, value)```",
)

q6 = QA(
    question="What is the difference between state and props in React?",
    answer="In React, both state and props are used to control how components render and behave, but they serve different purposes:\n\n- **Props:** Props are passed down from parent to child components and are immutable (read-only) within the child component. They represent input data that the component can use to render itself.\n\n- **State:** State is managed within the component itself and can be updated using `setState()`. It represents the internal state of the component, such as user input, UI state, or data fetched from an API. Changes to state trigger re-rendering of the component.",
)

q7 = QA(
    question="What is React Router and how do you use it?",
    answer="React Router is a popular routing library for React applications that allows you to handle navigation and routing in a declarative way. It provides components like `<BrowserRouter>`, `<Route>`, `<Switch>`, and `<Link>` to define and navigate between different routes in your application. You can use `<BrowserRouter>` as the root component, `<Route>` to define individual routes, `<Switch>` to render the first matched `<Route>`, and `<Link>` to create links between different routes. React Router enables single-page applications with multiple views and maintains a clean URL structure.",
)

q8 = QA(
    question="How do you handle forms in React?",
    answer="Handling forms in React involves managing form input elements and their state. You can use controlled components where form elements like `<input>`, `<textarea>`, and `<select>` maintain their own state and update it based on user input using onChange event handlers. Alternatively, you can use the `useState` hook to manage form state and `useRef` hook to access form elements directly. Form submission can be handled using onSubmit event handler on the `<form>` element to capture and process user input.",
)

q9 = QA(
    question="What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
    answer="""
Here are five creative ways to preserve and showcase your kids' art while minimizing clutter:

### 1. **Create a Rotating Gallery**
Designate a wall or a bulletin board in your home as a rotating gallery. Use frames, clips, or a wire with clothespins to display their artwork. Regularly rotate the pieces to keep the display fresh and exciting. This way, your kids can see their work being appreciated, and you can easily change out the pieces to reduce clutter.

### 2. **Make a Custom Art Book**
Collect the artwork and create a photo book or a scrapbook. You can scan or photograph each piece and use online services to design and print a professional-looking book. This way, you preserve the memories in a compact, easily storable format that can be revisited and enjoyed over the years.

### 3. **Create Art Collages**
Select a few favorite pieces and cut them into smaller shapes to create a new, collaborative collage. You can frame these collages as unique art pieces that combine multiple works into one. This not only reduces the number of individual items but also creates a special, joint project.

### 4. **Turn Art into Gifts or Keepsakes**
Use the artwork to create personalized gifts or keepsakes. Ideas include:
- **Calendars:** Make a calendar featuring different pieces for each month.
- **Magnets:** Transfer small pieces of art onto magnets for the fridge.
- **Puzzles:** Have a favorite piece turned into a custom puzzle.
- **Tote Bags or T-shirts:** Print the artwork onto fabric items.

### 5. **Digital Archive and Slideshow**
Scan or photograph each piece of art and create a digital archive. You can then use these digital files to create slideshows or digital photo frames that rotate through the images. This allows you to keep and enjoy the art without physical clutter. Additionally, you can easily share these digital collections with family and friends.
    """
)

DEFAULT_CHATS = {
    "Python Questions": [q1, q2, q3, q4, q5],
    "ReactJS Questions": [q6, q7, q8],
    "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.": [q9]
}


class State(rx.State):
    """The app state."""

    # Base vars ...
    title: str = "Reflex AI Chat"
    chats: dict[str, list[QA]] = DEFAULT_CHATS
    current_chat: str

    question: str
    processing: bool = False

    # Drawer/Sidebar vars ...
    is_sidebar_open: bool = False

    is_new_chat_open: bool = False
    new_chat_name: str = ""

    is_rename_chat_open: bool = False
    old_title: str
    new_title: str

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
            form_data: A dict with the current question.
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
