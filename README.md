<h1 align="center">
  <br>

  
  EmprendeAdvisor
  <p align="center">
  <img src="https://img.shields.io/github/v/release/renatogm24/emprendeadvisor?label=%20%F0%9F%93%A3%20Latest%20release&style=flat&logoColor=b0c0c0&labelColor=363D44)">
  <a href="https://www.emprendeadvisor.com/">
      <img src="https://img.shields.io/website?url=https%3A%2F%2Fwww.emprendeadvisor.com%2F">
  </a>
    <a href="https://github.com/renatogm24/readmetest">
      <img src="https://img.shields.io/github/last-commit/renatogm24/emprendeadvisor">
  </a>
  <img src="https://img.shields.io/github/pipenv/locked/python-version/renatogm24/emprendeadvisor">
    <img src="https://img.shields.io/badge/flask-2.0.2-yellowgreen">
    <img src="https://gpvc.arturio.dev/renatogm24">
</p>

</h1>
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#development">Development</a> •
  <a href="#built-with">Built with</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>
<p align="center">
  <a href="https://www.emprendeadvisor.com/" target="_blank">
    <img src="https://github.com/renatogm24/emprendeadvisor/blob/master/flask_app/static/images/EmprendeAdvisor_meta.png"
         alt="Logo banner" width="700px">
  </a>
  </p>

## Key Features

* Responsive design
* Register/Login users with encrypted passwords
* Profile page:
  - Edit or delete profile picture
  - Edit personal information
  - Change password
* Reset the password by sending an email with a url
* Request the creation of a new category for a business
* Filter businesses by rating, reviews and followers
* Order businesses by rating, reviews and followers
* Search and get information directly to instagram by @username
* Use Cache (images, data) in order to load faster
* Write your review about the business (must be logged)
* Reviews allow image(s) upload
* You can report an abuse
* Admin features:
  - Block/Unblock users
  - Delete reported reviews/businesses
  - Accept new categories

## How To Use

In order to configure the environment variables, it is necessary to create a .env file

```bash
secret_key='secret key'
db_user='user_db'
db_password='password_db'
AWS_ACCESS_KEY='AWS_KEY'
AWS_ACCESS_SECRET='AWS_ACCESS_SECRET'
GOOGLE_APPLICATION_CREDENTIALS='/path/to/file/config.json'
YOUR_GMAIL='mail@domain.com'
YOUR_PASSWORD='mail_password'
```

You need to create a schema in your database with this [model](https://github.com/renatogm24/emprendeadvisor/blob/master/emprendeadvisor.mwb)

To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/renatogm24/emprendeadvisor.git
# Go into the repository
$ cd emprendeadvisor
# Install virtual environment, must have python 3.9
# For Windows
$ pip install pipenv
# For Linux
$ apt install pipenv
# Activate virtualenv
$ pipenv shell
# Install dependencies (with sudo on Linux)
$ pipenv install -r requirement.txt
# Run the app
$ python server.py
```

Note: If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.


## Development

Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request 

#### Bug / Feature Request

If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue [here](https://github.com/renatogm24/emprendeadvisor/issues/new) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/renatogm24/emprendeadvisor/issues/new). Please include sample queries and their corresponding results.

## Built with

This web app uses the following libraries:

- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Boto3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Bootstrap](https://getbootstrap.com/)
- [Flask-assets (SASS Compiler)](https://flask-assets.readthedocs.io/en/latest/)
- [Flask-cors](https://flask-cors.readthedocs.io/en/latest/)
- [Google translator API](https://cloud.google.com/translate/docs/setup)
- [Redis client](https://github.com/redis/redis-py)
- [Flask-bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [Flask-mail](https://pythonhosted.org/Flask-Mail/)
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)

## Related

[emprendeadvisor-web](https://www.emprendeadvisor.com/) - Web of EmprendeAdvisor

## Support

<a href="https://www.buymeacoffee.com/renatogaray" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## License

MIT

[![Webpage](https://img.shields.io/badge/web-renatogaray.dev-orange)](https://renatogaray.dev) 
[![Follow me on GitHub](https://img.shields.io/badge/github-renatogm24-%23121011.svg?style=flat&logo=github&logoColor=white)](https://github.com/renatogm24) 
[![Follow me on LinkedIn](https://img.shields.io/badge/LinkedIn-renatogaray-blue?style=flat&logo=linkedin&logoColor=b0c0c0&labelColor=363D44)](https://www.linkedin.com/in/renatogaray) 
