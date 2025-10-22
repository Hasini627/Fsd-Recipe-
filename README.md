# Recipe Suggestor

A web application that suggests recipes based on user-provided ingredients using Django and Spoonacular API.

## Setup Instructions

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Spoonacular API key:
```
SPOONACULAR_API_KEY=your_api_key_here
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Visit http://127.0.0.1:8000/ in your browser
