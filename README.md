# Tinyblog-Api

Backend for lightweight blogging application.

## Installation instructions
### Local installation
1. Clone the repository.
```
git clone https://github.com/lymagics/tinyblog-api.git
```
2. Create .env file and fill in with .env.example variables.
3. Run local server.
```
docker-compose -f development.yml up -d
```
4. Apply database migrations.
```
docker-compose -f development.yml exec api python manage.py migrate
```
5. Populate database with fake values.
```
docker-compose -f development.yml exec api python manage.py add_users 10
docker-compose -f development.yml exec api python manage.py add_posts 100
```

### Production installation
1. Clone the repository
```
git clone https://github.com/lymagics/tinyblog-api.git
```
2. Create .env.api and .env.db files and fill in with .env.api.example and .env.db.example.
3. Run production server.
```
docker-compose -f production.yml up -d
```
4. Apply database migrations.
```
docker-compose -f production.yml exec api python manage.py migrate
```