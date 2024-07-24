# Order stream #

### Project Description ###
Allows you to get json with sales data and save it in Google Bin Query. The data is validated against fields and data types and then converted into a dataset for recording. The json received at the endpoint is saved in the database (sqlite) for logging.

### Technologies:
- Python
- Flask
- Pydantic
- SQLAlchemy
- Google Cloud Bigquery

### Author:
- [Mikhail Priselkov](https://github.com/BaronFAS)
- [Telegram](https://t.me/def_misha_work)

### How to run a project on a server: ###

**Clone the project from the repository and run the command from the project's root folder.**

**Move the .env and json file with the GBQ password to the root folder**
*Example .env file in the root folder*

```bash
sudo docker compose up --build -d
```

### How to run a project locally: ###

**Clone the project from the repository and run the commands from the project's root folder.**

```bash
# Create a virtual environment
python -m venv .venv
```

```bash
# Activate the virtual environment
source .venv/Scripts/activate
```

```bash
# Update pip
python -m pip install --upgrade pip
```

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Add the application name to your environment variables
export FLASK_APP=order_app
```

```bash
# Go to folder "flask_app"
cd flask_app
```

```bash
# Create the database and update the tables
flask db init
flask db migrate
flask db upgrade
```

```bash
# Run app
flask run
```

### How to access the database with logs ###

```bash
sqlite3
```

```bash
.open db.sqlite3
```

```bash
# Example request
SELECT * FROM "order" LIMIT 10;
```