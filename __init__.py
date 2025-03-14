import json
import os 
import requests
from flask import render_template, Blueprint, url_for, request
from CTFd.models import Users
from CTFd.utils.decorators import admins_only

PLUGIN_PATH = os.path.dirname(__file__)
CONFIG = json.load(open("{}/config.json".format(PLUGIN_PATH)))
bp = Blueprint("email_all", __name__, template_folder="templates")

def load(app):
    app.db.create_all() # Create all DB entities      
    bp = load_bp(CONFIG["route"]) # Load blueprint
    app.register_blueprint(bp) # Register blueprint to the Flask app

def load_bp(plugin_route):
    @bp.route(plugin_route, methods=["GET"])
    @admins_only
    def show():
        return render_template("test.html")  
        
    @bp.route(plugin_route, methods=["POST"])
    @admins_only
    def send():
        text = request.form.to_dict()['message']
        #Send email to all registered users
        users = Users.query.all()
        for user in users:
            # TODO: send email
            response = requests.post(url_for(
                'api.users_user_emails', 
                user_id=user.id, 
                _external=True), 
                json={
                    "text": text
                },
                headers={
                    'Authorization': 'Token ctfd_828444f2afca7f50b7afce399d6f261df331aeaee3af1c08af4650659f3cf0fc',
                    'Content-Type':'application/json'
                })
            
            message = "Errors:\n"
            
            if(response.status_code >= 400):
                errors = response.json()['errors']
                for error in errors.values():
                    for e in error:
                        message+=e
                        message+="\n"
                message = errors
            else:
                message="Email sent to all users"

        return render_template("test.html", message=message)    

    @bp.route('/test', methods=['POST'])
    def test():
        return {"message": "Test route success!"}, 200
 
    return bp
