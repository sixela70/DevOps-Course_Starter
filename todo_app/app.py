import os
from todo_app.data.mongodb import MongoDb
from flask.globals import request
from flask import Flask, render_template, redirect

from todo_app.view_models.view_model import ViewModel 

def create_app():
    app = Flask(__name__, template_folder="templates")

    @app.route("/", methods=['GET', 'POST'])
    def index():
        item_view_model = ViewModel(MongoDb.get_all_items())  
        return render_template('index.html', view_model=item_view_model)

    @app.route("/complete_item/<string:id>")
    def complete_item(id):
        MongoDb.markid_item_done(id)
        return redirect('/')

    @app.route("/doing_item/<string:id>")
    def doing_item(id):
        MongoDb.markid_item_doing(id)
        return redirect('/')

    @app.route("/uncomplete_item/<string:id>")
    def uncomplete_item(id):
        MongoDb.markid_item_undone(id)
        return redirect('/')

    @app.route("/add_todo_item", methods=['GET', 'POST'])
    def add_todo_item():
        new_todo_item = request.form.get('new_todo_item')
        if isvalid(new_todo_item):
            MongoDb.add_item(new_todo_item)
        return redirect('/')

    def isvalid(new_todo_item):
        return len(new_todo_item) != 0

    return app

if __name__ == '__main__':
    app = create_app().run(host='0.0.0.0', debug=True)
