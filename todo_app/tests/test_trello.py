import pytest
from todo_app.trello.trello_api import TrelloAPI
from todo_app.trello.trello_base  import TrelloBase

# Wish I knew what was loading the environment (.env file) here 

def test_enironment_has_been_read():
        assert TrelloBase.get_board_id() != None
        assert TrelloBase.get_done_list_id() != None
        assert TrelloBase.get_todo_list_id() != None


def test_get_trello_list():
        trello_list = TrelloAPI.get_all_trello_items()
