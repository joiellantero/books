<img src="static/images/home-page.png"></a>

# books.

A website demonstrating SQL queries using python and flask; also, demonstrates HTTP status codes, API access, and API calls. A project in CS50W

This website uses the goodreads api to extract information about the books queried then allows uses to rate these books and send their own review. 

> Disclaimer: As of December 8th 2020, Goodreads is no longer issuing new developer keys for our public developer API and plans to retire the current version of these tools. You can find more information [here](https://help.goodreads.com/s/article/Does-Goodreads-support-the-use-of-APIs).

## Usage

- Register or Login

<img src="static/images/registration-page.png" title="books." alt="books-website"></a>

<img src="static/images/login-page.png"></a>

- Use library page to search books by ISBN, title or author

![Library GIF](http://g.recordit.co/fzLFcCSWf3.gif)

- View user ratings or create own rating

![Review GIF](http://g.recordit.co/eBQqkeVLUe.gif)

- API access via GET request

![API GIF](http://g.recordit.co/NI05UgjpvG.gif)

## Local Deployment

- All the `code` required to get started

### Clone

- Clone this repo to your local machine using `https://github.com/joiellantero/books.git`

### Setup

- After cloning, run the following code to get started:

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
