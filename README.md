pyJucks
=======

Started playing with Python, Flask, Jinja2 and Nunjucks 

http://mozilla.github.io/nunjucks/

Then started playing with pdfs for adding and extracting data

Requirements
============

linux packages : 
    python imagemagick nodejs npm

python modules :
    pip install flask pdfminer pdfquery pypdf reportlab

node modules :
    npm install nunjucks


------------

Before first run and after alteration, the templates must be compiled for use by nunjucks-slim on the front end using :

    node nunjucks-compile app/templates/ > app/static/js/templates.js
