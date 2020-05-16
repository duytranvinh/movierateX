# MovieRateX

MovieRateX is an app that allows users to browse movies from the [The Movie Database API](http://docs.themoviedb.apiary.io/#)

## Deploy

The app is automatically deploy through [Heroku](https://www.heroku.com/)

Here is the link to the website: https://movieratex.herokuapp.com/

## Getting Started

Make sure you have Python version 3.6 with pip installed on your computer to setup a localhost web server for development purpose.

More information can be found here:

[How do you set up a local testing server?]( https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)

### Prerequisites

Python 3.6 with pip

Required packages: 
1.	Flask
2.	Flask-Heroku
3.	Flask-Login
4.	Flask-SQLAlchemy
5.	Flask-WTF
6.	Gunicorn (only required on Heroku)
7.	psycopg2 binary (only required on Heroku)
8.	SQLAlchemy
9. ...

See the most updated complete list [requirements.txt](https://github.com/vinhthaiduytran/movierateX/blob/master/requirements.txt)

### Installation

Clone this git repo then install the required packages. 
Use the terminal: *(For Window, make sure to “Run as administrator”)*
```
git clone git@github.com:vinhthaiduytran/movierateX.git
```

Example of installing individual package:

```
pip install Flask
```
For Mac:
```
pip3 install Flask
```
All packages listed in the requirements text file are required to run the application.


## Deployment

This repo is built with Heroku package and is ready for deployment. Please see Heroku official website for more information.
[GitHub Integration (Heroku GitHub Deploys)]( https://devcenter.heroku.com/articles/github-integration)


## Built With

* [Python](https://www.python.org/) - An interpreted, high-level, general-purpose programming language.
* [JQuery](https://www.jquery.com) - A fast, small, and feature-rich JavaScript library.
* [MaterializeCSS](https://materializecss.com/) - A modern responsive front-end framework based on Material Design.



## Authors

* **Duy Tran Vinh Thai**
* **Grace To**
* **Sachin Shah**

## License

    Copyright [2020] [Duy Tran Vinh Thai]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
