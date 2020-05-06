<img src="https://lh3.googleusercontent.com/25C4x-YcoQfXO2U7SSgPHoQvBpCfBPE4KtQ5VhgBjYByA8NqPGo36osRZ-rJVwjviBPrx63ZkEd2KM9NTSiXT7GrYo4JWAAFja75Se8jxgPNGHxq6A67YrKKDJxzSQAgOGF4CZGprzyk0mAiKAVLe5QFSf3RHwiZGg8uiimzXgTcprQXK3Xta64OvOXOiLP7Hgbn3HBLLXvt7RfgGL2I-LRAmReRwtCt6pGulwUuy6oDgoh1RNxNtwsuuNCitqrcibWYWOzOLKNKkPfRs1TQg8C4zc5bHFZpX_o2FFUPEnq0mrfKu9s-2NGiE69sHtXW5ZGQarhBCkWkfhH6cZUbY7h_CftPXW9Na3fRsze1S2GusN2FmHLNOZvDfwLyC8c6ssgI442f21z0cRVcJgo4k32j29MJJfy--1QsYvGJwOUowuaujpAkDhx2bGmB6N6LgquWP8Oz-0uhlh1HcsdRuGC04kw1STBLI9UQZGcEKwaTJyp-1VRhMLgfFXhnMrKzxxiAdLgiXEIwQjuJjcWMZthBKn1gt3o0-gbP2EkEn3m6Gvy7gsuSbcnG3XNpKqADgDnBHHKbBDZHP7wRB3ktkVvYKkA4UHKE2ZvJeF-zIZOBcMeTOU3enhsqBBnywlG5nus3dCxss2aJRcDAJhKjq2BTas4kXfMaF0G5k_SLD6O09-47qWhGpSgW1HQf=w2852-h1398-no" title="books." alt="books-website"></a>

# books.

> A website demonstrating SQL queries using python and flask; also, demonstrates HTTP status codes, API access, and API calls.

## Usage

- Register or Login
- Use library page to search books by ISBN, title or author
- View user ratings or create own rating
- API access via GET request

## Local Deployment

- All the `code` required to get started

### Clone

- Clone this repo to your local machine using `https://github.com/joiellantero/books.git`

### Setup

- After cloning run the following code to get started:

> Open terminal and navigate to the directory of the cloned repo

```shell
$ cd books-<branchname>

# example - if on branch master
$ cd books-master
```

> Install the required modules

```shell
$ pip3 install -r requirements.txt
```

> Setup flask and database

```shell
$ export FLASK_APP=application.py
$ export DATABASE_KEY=<URI>
$ export GOODREADS_KEY=<key>
```

- Obtain URI and key from author

### Run

> Run flask

```shell
$ flask run
```

### Resources

- Images from Freepik.com
- Bootstrap v4.4.1
- Font Awesome Pro 5.13.0
