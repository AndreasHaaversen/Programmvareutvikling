# Nigiri Falls Takeaway
Handle takeaway orders with ease - Nigiri Falls Takeaway is a feature complete online takeaway ordering system for both employees and customers.

This project had been configured with Continous Deployment, and is available [here](https://nigirifallsdev.herokuapp.com/).

## Motivation
This project was started to create a complete takeaway ordering system for the sushi restaurant Nigiri Falls. It is meant to be user friendly, international and universally adaptable.

## Build status
[![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-51/badges/master/pipeline.svg)](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-51/commits/master) [![coverage report](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-51/badges/master/coverage.svg)](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-51/commits/master)

## Code style
This project follows the PEP8 style guide for Python code, except [E501](https://lintlyci.github.io/Flake8Rules/rules/E501.html). No specific style is used for HTML and CSS, but common sense applies. 😉

## Screenshots
![alt text](https://imgur.com/xXtI9jw "Home page")
## Tech/framework used

**Built with**
- [Django](https://www.djangoproject.com/)
- [Whitenoise](http://whitenoise.evans.io/en/stable/)
- [AWS S3](https://aws.amazon.com/s3/)
- [Bootstrap](https://getbootstrap.com/)
- [Weasyprint](https://weasyprint.org/)
- [Django-Watson](https://github.com/etianen/django-watson)
- [Heroku](https://www.heroku.com/)

## Installation
1. Fork the repository.
2. Clone into it with ``git clone``.
3. Go to ``/nigirifalls`` in your terminal of choice and run ``pip3 install -r requirements.txt`` to install dependencies.
4. Run ``python3 manage.py makemigrations`` and ``python3 manage.py migrate`` to create the database.
5. Run ``python3 manage.py runserver``. A local instance of the website should be running at ``localhost:8000``.

## Tests
Run the unit tests by running ``python3 manage.py test``.
If you want a test report, ensure that you have [Coverage](https://coverage.readthedocs.io/en/v4.5.x/) installed, and run:
``coverage run --source='.' manage.py test``
``coverage report``

## How to use?
See our wiki on [GitLab](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-51/wikis/home)!
It contains a user guide, code overview, "How to contribute", product road map and documentation (In _Norwegian_).

## License
No license is provided.