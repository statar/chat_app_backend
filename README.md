# ChatRoom(https://web-chat-angular.herokuapp.com)

You can register and login to the application. In the chat room you can send, receive messages, view logged in users information from user list, update your profile and see your message mood if you give positive energy to your chat mates.

If you want to change the SERVER URL to a local server;

For web frontend:
web_based_chat_app_frontend/src/environments/environment.ts

// server_url: 'https://boiling-plains-77861.herokuapp.com'

server_url: 'http://localhost:5000',

For web backend heroku db conenction:

web_based_chat_app_backend/config.py Update postgres_local_base ( "postgres://”user_name”:”password”@localhost/web_chat_task").

web_based_chat_app_backend/create_db.py Update engine ( "postgres://”user_name”:”password”@localhost/web_chat_task").


To setup and run Backend locally:

Install Python 3.7

python -m env env cd env/Scripts/activate

pip install -r requirements.txt

python create_db.py

python app.py
