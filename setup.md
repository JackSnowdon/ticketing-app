# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies after pulling changes
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Run tests
pytest

# 5. Run Django
python manage.py runserver
