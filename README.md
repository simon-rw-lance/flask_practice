# flask_practice
Practice repo for learning web development using Flask.

To run:
(note the following terminal commands are for Bash)

1) Initialise flask by first telling it where to find the application with "export FLASK_APP=flaskr"
2) Declare environment with one of the following options
  a) "export FLASK_ENV=product"
  b) "export FLASK_ENV=testing"
  c) "export FLASK_ENV=development"
3) Initialise the SQL database with "flask init-db"
4) Lastly run the application with "flask run"
5) The terminal should display something along the lines of:

 * Serving Flask app "flaskr"
 * Environment: product
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Simply navigate to http://127.0.0.1:5000/ in a browser of your choice to explore the application. If another program is already using port 5000 you'll recieve an OSError. Instructions to circumvent this can be found here https://flask.palletsprojects.com/en/2.1.x/server/#address-already-in-use

Note that step 3) only needs to be done once. Running this later will wipe and reinitialise the SQL database resulting in a reset of all users and posts.
