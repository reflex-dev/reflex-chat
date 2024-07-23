from ..states.state import State, DEFAULT_CHATS


class Drawer(State):

    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    def toggle_new_chat(self):
        self.is_new_chat_open = not self.is_new_chat_open

    def toggle_rename(self, data: str):
        self.is_rename_chat_open = not self.is_rename_chat_open
        self.new_title = data
        self.old_title = data

    async def update_renaming_chat_input(self, value: str):
        self.new_title = value
        self.title = value

    async def create_new_chat(self):
        if self.new_chat_name:
            self.current_chat = self.new_chat_name
            self.chats[self.new_chat_name] = []

            self.toggle_new_chat()

    async def select_chat(self, data: str):
        self.current_chat = data
        self.title = self.current_chat


class SidebarOption(State):

    async def delete_chat(self, data: str):
        try:
            del self.chats[data]

            if len(self.chats) == 0:
                self.chats = DEFAULT_CHATS
                self.current_chat = list(self.chats.keys())[0]

            else:
                self.current_chat = list(self.chats.keys())[0]

        except KeyError:
            ...

    async def rename_chat(self):
        self.chats[self.new_title] = self.chats.pop(self.old_title)
        self.current_chat = self.new_title
        self.is_rename_chat_open = not self.is_rename_chat_open
