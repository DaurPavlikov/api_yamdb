import csv
import os

from api_yamdb.settings import BASE_DIR
from reviews.models import Comment, Category, Genre, GenreTitle, Title, Review
from users.models import User

path = os.path.join(BASE_DIR, 'static/data/')
os.chdir(path)

# Скрипт для испорта из файла CSV в базу данных User
with open('users.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных Category
with open('category.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных Genre
with open('genre.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных Title
with open('titles.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных GenreTitle
with open('genre_title.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = GenreTitle(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            genre=Genre.objects.get(id=row['genre_id'])
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных Review
with open('review.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Review(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date']
        )
        db.save()

# Скрипт для испорта из файла CSV в базу данных Comment
with open('comments.csv', mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        db = Comment(
            id=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=row['pub_date']
        )
        db.save()
