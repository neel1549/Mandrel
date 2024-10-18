from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from asgiref.wsgi import WsgiToAsgi
import os


app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

# Load environment variables from .env file
load_dotenv()

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize MongoClient to connect to Atlas(Mongo Cloud)
mongodb_client = MongoClient(os.getenv("MONGO_URI"))
users_collection = mongodb_client["neelkk"]["Users"]


# In-memory user list
users = {}

# Handle Slack webhooks
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    # Check if we have a challenge  - this is for Slack to verify the endpoint
    if "challenge" in data: 
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event_type = data["event"]["type"]
        print(event_type)

        # Handle user events where we have a new slack user joining
        if event_type == "team_join":
            user = data["event"]["user"]
            user_name = user["profile"]["real_name"]

            if "email" in user["profile"]:
                user_email = user["profile"]["email"]
            else:
                user_email = "N/A"

            user_document = { 
                "_id": user["id"],  # Using the Slack user ID as the document ID
                "name": user_name, 
                "email": user_email 
            }

            result = users_collection.insert_one(user)
            if result.inserted_id:
                print(f"User {user_name} added with id {user['id']}")

            print(f"User {user['name']} has been inserted")
            
        # Handle user events where we have a slack user update their profile.
        elif event_type == "user_change":
            user = data["event"]["user"]
            user_id = user["id"]
            query_filter = {'_id' : user_id}

            # Handle user events where we have a slack user being deactivated or deleted.
            if user["deleted"]:
                result = users_collection.delete_one(query_filter)
                if result.deleted_count == 0:
                    print(f"No user found with id {user_id}")
                    return

                print(f"User with id {user_id} was deleted")

            else:
                update_operation = { '$set' : 
                        { 'name' : user["real_name"], 'email' : user["profile"]["email"] }
                    }
                query_filter = {'_id' : user_id}
                result = users_collection.update_one(query_filter, update_operation, upsert=True)

        users = users_collection.find()
        users_data = [{"_id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]
        socketio.emit("update_slack_users", users_data)


    return jsonify({"status": "ok"})

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    # Send initial data when frontend connects
    users = users_collection.find()
    users_data = [{"_id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]
    emit("initial_slack_users", users_data)

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port = int(os.environ.get("PORT", 5000)), allow_unsafe_werkzeug=True)

