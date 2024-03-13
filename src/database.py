from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

# Model Declarations

class MessageHistory(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)

    # Chat ID and message ID are unique together

    chat_id = Column(String)
    message_id = Column(String)

    # Message metadata we need to store
    
    # Who sent the message
    from_user = Column(String)
    # If the message is a reply, who is it replying to. Otherwise, None
    is_reply_to = Column(String)
    # The message text itself
    text = Column(String)

    # When the message was sent. Set to the current time when the message is stored, not when it was sent
    timestamp = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('chat_id', 'message_id', name='uix_chat_id_message_id'),
    )


# Database Initialization and helpers

class Database:
    def __init__(self, database_url):
        print(database_url)
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_message(self, chat_id, message_id, from_user, is_reply_to, text, timestamp):
        # Synchronous method to add a message
        pass

    def query_messages(self, chat_id):
        # Synchronous method to query messages
        pass

'''
import json
from typing import List

from config import AppConfig
from telebot import types

# TODO: find a way to get around having this in memory the whole time
# TODO: implement a way to break up chat histories so we can selectively load / dump them

# Where to read / write the chat history on disk
HISTORY_FILE = "history.json"

# Let's air on the side of verbose and opinionated for chat ids
ChatId = str


# NOTE: telegram groups optionally have 'topics'.
#  These are not given unqiue ids so we interpret chat_ids
#   as strs and append the topic if necessary to provide a unqiue key 
#    in the bot's history
def chat_id_from_message(message: types.Message) -> ChatId:
    """
    Get our internal representation of a message's chat identifier
    from its metadata
    """

    # TODO: messgae thread ids are only for supergroups i think, while topic_messages are for any group
    # but i would think you'd want to include the topic in this!
    # make sure we're doing this correctly
    if message.is_topic_message:
        return str(message.chat.id) + "_" + str(message.message_thread_id)
    else:
        return str(message.chat.id)

class History():
    """
    An in-memory representation of a chat bot history.
    Tracks total history of all chats connected to the bot.
    """

    # Where to read / write the chat history on disk
    file_path: str
    # Map of chat_id to chat history
    # Dict[ChatId, List[types.Message]]
    history = {}

    def __init__(self, appConfig: AppConfig):
        self.file_path = appConfig.get_config()['history']['file']
        self.load()

    def dump(self):
        """Writes the chat history to a file.
        """
        to_write = {}
        for chat_id, history in self.history.items():
            to_write[chat_id] = [msg.json for msg in history]
        with open(self.file_path, "w") as f:
            json.dump(to_write, f)

    def load(self):
        """Reads the chat history from a file.
        """
        try:
            history = {}
            with open(self.file_path, "r") as f:
                history = json.load(f)
            for chat_id in history.keys():
                self.history[chat_id] = [
                    types.Message.de_json(item) for item in history[chat_id]
                ]
        except FileNotFoundError:
            self.history = {}

    def get_chat_last_message(self, chat_id: ChatId) -> types.Message:
        """Gets the most recent message in the history this message belongs to

        Args:
            message (telebot.types.Message): The message for which we want to get the chat history

        Returns:
            types.Message: the most recent message in the history if available. None if otherwise
        """
        # TODO: all of a sudden this is demanding that chat_id is a str! Somethin'g wrong here
        chat_id = str(chat_id)
        if chat_id in self.history:
            return self.history[chat_id][-1]
        else:
            return None

    def get_chat_nth_last_message(self, chat_id: ChatId, nth: int) -> List[types.Message]:
        """Gets the nth most recent message preceeding the history this message belongs to

        Args:
            message (telebot.types.Message): The message for which we want to get the chat history
            nth (int): integer representing how far back to go

        Returns:
            types.Message: the nth most recent message in the history if available. None if otherwise
        """
        # TODO: all of a sudden this is demanding that chat_id is a str! Somethin'g wrong here
        chat_id = str(chat_id)
        # Check if the history is big enough -- avoid wrapping back around
        if nth > len(self.history[chat_id]):
            return None

        # Invert the index to index backwards
        return self.history[chat_id][-nth]

    def clear_chat_history(self, chat_id: ChatId):
        """Clear the chat history preceeding the given message

        Args:
            message (telebot.types.Message): The message for which we want to clear the preceeding chat history
        """
        # TODO: all of a sudden this is demanding that chat_id is a str! Somethin'g wrong here
        chat_id = str(chat_id)
        if chat_id in self.history:
            self.history[chat_id] = []
        self.dump()

    def add_message(self, message: types.Message):
        """Adds a message to its chat's history
        Saves the result to disk

        Args:
            message (types.Message): The message to add to the chat history.
        """
        chat_id = chat_id_from_message(message)
        # TODO: all of a sudden this is demanding that chat_id is a str! Somethin'g wrong here
        chat_id = str(chat_id)
        if chat_id not in self.history:
            self.history[chat_id] = []
        self.history[chat_id].append(message)
        self.dump()
        return chat_id

    def update_message(self, message: types.Message):
        """Updates a message in its chat's history
        Saves the result to disk

        Args:
            message (types.Message): The message to add to the chat history.
        """
        chat_id = chat_id_from_message(message)
        # TODO: all of a sudden this is demanding that chat_id is a str! Somethin'g wrong here
        chat_id = str(chat_id)
        if chat_id in self.history:
            for i, msg in enumerate(self.history[chat_id]):
                if msg.message_id == message.message_id:
                    self.history[chat_id][i] = message
                    self.dump()
                    return None
        return None
'''