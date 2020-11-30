
import requests
from todo_app.trello.trello_base import TrelloBase

# We should probably cache these id items 
# To save server hops

def get_board_id():
    url = 'https://api.trello.com/1/members/me/boards?fields=id'+TrelloBase.auth_tokens()
    response= requests.get(url)
    jsonResponse = response.json()
    return jsonResponse[0]['id'] # Do not like this does not feel safe

def get_lists():
    board_id = get_board_id()
    url = TrelloBase.base_address+'boards/'+board_id+'/lists?fields=id,name'+TrelloBase.auth_tokens()
    response= requests.get(url)
    return response.json()

def get_todo_list_id():
    jsonResponse = get_lists()
    for item in jsonResponse:
        if item['name'] == 'ToDoList':
            return item['id']
    return 0            

def get_done_list_id():
    jsonResponse = get_lists()
    for item in jsonResponse:
        if item['name'] == 'DoneList':
            return item['id']
    return 0            

# Get all cards from todolist 
def get_items():
    board_id = get_board_id()
    done_list_id = get_done_list_id()
    dolist_id = get_todo_list_id()
    list_items = []
    url = TrelloBase.base_address+'boards/'+board_id+'/cards?fields=id,idList,name'+TrelloBase.auth_tokens()
    response= requests.get(url)
    jsonResponse = response.json()
    ## cycle through and build new list using the list id determine if done or todo yuck yuck yuck why am creating a new list 
    ## surely I can filter in someway .. but I want the status field. 
    ## perhaps if I have time come back to this 
    for item in jsonResponse:
        if item['idList'] == done_list_id:
            list_item = { 'id' : item['id'], 'title' : item['name'] , 'status' : 'Done' }
        elif item['idList'] == dolist_id:
            list_item = { 'id' : item['id'], 'title' : item['name'] , 'status' : 'Not Started' }
        else:
            #list_item = { 'id' : item['id'], 'title' : item['name'] , 'status' : 'Unknown' }
            print('Discarding items from other test list ' + item['id'] + '  ' +item['name'])

        list_items.append(list_item)        
    return list_items

    
### Yeaaaaaaaaaaaaaaaa gods this is slow 
def add_item(title):
    dolist_id = get_todo_list_id()
    url = TrelloBase.base_address+'/cards?'
    data = TrelloBase.auth_tokens_obj()
    data["idList"] = dolist_id
    data["name"] =  title
    requests.post(url, data)

## Move item to the other list 
def mark_item_done(item):
    markid_item_done(item['id'])
    """done_list_id = get_done_list_id()
    url = TrelloBase.base_address+'/cards/'+item['id']+'?'
    data = TrelloBase.auth_tokens_obj()
    data["idList"] = done_list_id
    requests.put(url, data)
"""

def markid_item_done(id):
    done_list_id = get_done_list_id()
    url = TrelloBase.base_address+'/cards/'+id+'?'
    data = TrelloBase.auth_tokens_obj()
    data["idList"] = done_list_id
    requests.put(url, data)

def mark_item_not_done(item):
    markid_item_undone(item['id'])
    """dolist_id = get_todo_list_id()
    url = TrelloBase.base_address+'/cards/'+item['id']+'?'
    data = TrelloBase.auth_tokens_obj()
    data["idList"] = dolist_id
    requests.put(url, data)"""
    
def markid_item_undone(id):
    dolist_id = get_todo_list_id()
    url = TrelloBase.base_address+'/cards/'+id+'?'
    data = TrelloBase.auth_tokens_obj()
    data["idList"] = dolist_id
    requests.put(url, data)
