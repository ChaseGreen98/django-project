This application requires two installs in order to run. 

FIRST - INSTALL DAPHNE
pip install daphne

SECOND - INSTALL WHITENOISE
pip install whitenoise

THIRD - RUN WITH
daphne -p 8000 config.asgi:application
