# FastTask

- Navigation:
    - [About](https://github.com/ZeroNiki/FastTask/blob/main/README.md#about) 
        - [Features](https://github.com/ZeroNiki/FastTask/blob/main/README.md#features)
            - [Components](https://github.com/ZeroNiki/FastTask/blob/main/README.md#components)
    - [Install and usage](https://github.com/ZeroNiki/FastTask/blob/main/README.md#install-and-usage)


<b>[RU README](https://github.com/ZeroNiki/FastTask/blob/main/README_RUS.md)</b>

## About
This project is a Task Management Bot using the Aiogram framework for Telegram bot interaction and FastAPI for backend operations. It integrates a SQLite database via SQLAlchemy ORM to manage users and tasks. The bot allows users to create, view, update, and delete tasks with seamless interaction and error handling.

### Features
- <b>User Management:</b> Automatic registration of users on their first interaction with the bot.
- <b>Task Management:</b> Create, view, update, and delete tasks. Tasks are stored in the database and associated with specific users.
- <b>Error Handling:</b> Logs and replies to users in case of errors during API calls.
- <b>Interactive Telegram Interface:</b> Rich text formatting and custom keyboards for easy user interaction.

#### Components
##### Telegram Bot
- <b>Aiogram</b> framework handles bot commands and messages.
- <b>Command Handlers</b> for starting the bot, registering users, and viewing tasks.
- <b>Interactive Keyboard</b> options for task management.

##### FastAPI Backend
- Exposes API endpoints for managing users and tasks:
    - POST `/operations/users:` Create a new user.
    - POST `/operations/tasks:` Create a task.
    - GET `/operations/tasks/{user_id}:` Retrieve tasks for a user.
    - PATCH `/operations/tasks/{task_id}:` Mark task as done.
    - DELETE `/operations/tasks/{task_id}:` Delete a task.


## Install and usage

Clone repo:
```sh
git clone https://github.com/ZeroNiki/FastTask.git

cd FastTask
```

Install requirements:
```
pip install -r requirements.txt 
```

in `.env` file paste you telegram bot `TOKEN`:
```
TOKEN=you bot token
```

Start `api` and `bot`:
```sh
python3 start_api.py 

python3 start_bot.py 
```

Done!
