Interactive Web Page that is essentially a music app that is accessible from the browser. The music app will provide a social login to allow users to easily identify themselves, and allow users to scroll through songs and find music they like in a more simplified, streamlined process. The simpler UI will eliminate some of the hassle of searching for songs, by using a machine learning model to predict songs that app users will enjoy.

- Visit My Heroku App URL Here: [Heroku App](https://cherry-pie-58273.herokuapp.com/login)
- Raw URL: [https://cherry-pie-58273.herokuapp.com/login]

## Setup Instructions
1. `pip3 install -r requirements.txt`
2. Create a `.env` file in the top-level directory and enter the following as its contents:
```
export DATABASE_URL="<YOUR POSTGRESQL DB URL>"
```

## To run the app
1. Run `python3 routes.py`

We aim to deliver a music app that is accessible from the browser. While on the login page, the user would be able to click on signin to create an account in case they do not already have one created. They would then be redirected to the signup page where they would be asked to fill in your first name, last name, username, email, and password to create your account. Once logged in, the app allow users to scroll through songs and find music they like in a more simplified, streamlined process.The user should also be able to search an artist, and pictures of the artist should pop up, along with genre of music he plays, with other related names. The simpler UI will eliminate some of the hassle of searching for songs, by using a machine learning model to predict songs that app users will enjoy. the app will be using Spotify API 

We built a web app using Flask in the backend and React/JS in the frontend. The app will allow its user to create their login credential as it these information will be saved in the database.

In order to run the files contained in this folder, a few python libraries to be set up in the environment. Some of the libraries used are python in-built so there's no need to install them once python itself has been installed. Besides those, the dotenv, flask, and requests libraries need to be installed. Particularly, dotenv needs to installed with the command pip python-dotenv in the terminal whereas the other can be installed with the command pip install followed by the name of the correspondent python library. Finally, in the terminal, navigate to the directory containing routes.py then type in the terminal, python3 routes.py. You should see a link to view in your browser. click on the link, and you have successfully run the program.

We had to utilize PostgreSQL database management system for saving user's login credentials. We also have an .env file throughout this project, but I did not push it as required. In the .env file, we included the DATAbase_URL, and key which was acquired through the heroku account under setting after creating the application. Usage of Flask-SQLAlchemy is also required to provide an object-relatioanl mapping between Postgres database and python logic. SQLAlchemy, and flask_login was also used. 
Finally, on this project, we also made use of javascript files. We utilized python linting (pylint) to format the python code. 

Also, we encountered some troubles as far as error messages popping up everywhere on my code despite using pylint to fix all errors. It seems that pylint was wrong  in some cases, so we relied on my best jugedment instead. However, here are some errors messages that we encountered while running the python codes; notable, routes.py, spotify_model.py, and models.py, along with the reasons for each error message:

#1. spotify_model.py errors:
# pylint: disable=anomalous-backslash-in-string,E1101
Reason: interaction with pandas where an error is raised with .dropna() and .get_dummies(), Stackoverflow answers say it is best to ignore.

#2. routes.py errors: 
# pylint: disable=E1101, W1508, C0116
Reason for E1101: Instance of 'scoped_session' has no 'commit' member error being raised for db.commit
Reason for W1508: os.getenv default type is builtins.int. Expected str or None. error when casting port to int
Reason for C0116: Route names are self-explanatory, no need for docstrings

#3. models.py errors:
# pylint: disable=C0114, E1101, C0103, R0903
Reason for C0114: docstring not neccessary 
Reason for E1101: weird SQLAlchemy errors when making columns
Reason for C0103: table not in Pascal Naming convention
Reason for R0903: too few public methods which is fine for a db.model


One of the hardest parts of the project came when we begin unit testing our codes. Then after we got through all the tests and checked to make sure everything was running well, from there, everything began wrapping up fast. So far, this group project with this first Sprint has been a great experience as well as practicing being able to work in a group enrivronment while being remotely. It was highly beneficial and useful for the group's learning as we were to utilized all the tools at our disposal including Github, email, Discord, Google meet, and calendar to plan, distribute tasks, and meet to discuss changes needed to implement, set meetings among us team members, or even with our assigned Industry mentor, and check on each other's evolution. Thanks to everyone's cordinated efforts, we have successfully created and deployed through heroku. Also, Implementing each portion of the application was fullfilling to see the result being displayed.



## Setup Instructions
1. `pip3 install -r requirements.txt`
2. Create a `.env` file in the top-level directory and enter the following as its contents:
```
export SPOTIFY_API_KEY="<OUR API KEY>"
export DATABASE_URL="<YOUR POSTGRESQL DB URL>"
```

# Getting Started with  Create React App
This was bootstrapped  with [Create React App]

## Available Scripts
In the directory, you can run:

### 'npm start'
It runs the app in the development mode.
The page reloads when you make changes.
You can also see any lint errors in the console.

### 'npm run build'
Builds the app for production to the 'build' folder.
It bundles React in production mode and optimes the build for the best performance.
The build is minified and the filenames include the hashes. Then the app is ready to be deployed.

