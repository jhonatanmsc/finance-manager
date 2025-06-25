## Finance Manager

finance manager like it's name says a finance manager implemented using django admin only

### Requirements
- Python 3.12 or higher
- postgresql

### How to install and run
First create a virtual environment and activate it
```bash
  virtualenv venv
```
So activate it (Linux example)
```bash
  source venv/bin/activate
```
So activate it (Windows example)
```bash
  source venv/Scripts/activate.bat
```
And install the deps
```bash
  pip install -r requirements.txt
```
Apply the migrations
```bash
  python manage.py migrate
```
Last but not least, run it
```bash
  python manage.py runserver 0.0.0.0
```