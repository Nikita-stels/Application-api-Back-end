from flask import Flask, request
from server_in_app import client_wrapper

app = Flask(__name__)


def post_request(command):
    data = request.json
    headers = request.headers
    user_name = headers['UserName']
    user_secret =  headers['UserSecret']

    answer = client_wrapper(user_name, user_secret, command, data=data)
    if answer:
        return {"ok":True}

def get_request(command):
    headers = request.headers
    user_name = headers['UserName']
    user_secret =  headers['UserSecret']

    answer = client_wrapper(user_name, user_secret, command)
    return answer


@app.route('/api/v1/info')
def info():
    with open('read_me.txt') as r:
        message = r.read()
    return message


@app.route('/api/v1/user/list')
def user_list():
    """ GET all user """

    command = 'user_list'
    return get_request(command)


@app.route('/api/v1/board/create', methods=['POST'])
def board_creat():
    """
    request: {
        "title":"Name_board",
        "columns":[names_cards]
    }
    response: {"ok": true}
    """
    command = 'board_creat'
    return post_request(command)


@app.route('/api/v1/board/delete', methods=['POST'])
def board_delete():
    """
    {"title": "Доска разработчика"}
    """

    command = 'board_delete'
    return post_request(command)


@app.route('/api/v1/board/list')
def board_list():
    """ GET all board """

    command = 'board_list'
    return get_request(command)


@app.route('/api/v1/card/create', methods=['POST'])
def card_create():
    """
    {
        "title": "Развернуть PostgreSQL",
        "board": "Доска разработчика",
        "status": "ToDo",
        "description": "Необходимо развернуть базу данных PostgreSQL",
        "assignee": "Username",
        "estimation": "8h"
    }
    """

    command = 'card_create'
    return post_request(command)


@app.route('/api/v1/card/update', methods=['POST'])
def card_update():
    """
    {
        "title": "Развернуть PostgreSQL",
        "board": "Доска разработчика",
        "status": "Done"
    }
    """

    command = 'card_update'
    return post_request(command)


@app.route('/api/v1/report/cards_by_column', methods=['POST'])
def report():
    """ 
    {
        "board": "Доска разработчика",
        "column": "ToDo",
        "assignee": "Username"
    }
    """

    command = 'report_cards'
    return post_request(command)


app.run()

