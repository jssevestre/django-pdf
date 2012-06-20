==========
django-pdf
==========

A django MiddleWare to converte on-the-fly views' HTML output to PDF
**without modifying your views.**

-----
About
-----

Django-pdf use xhtml2pdf to tranform the HtmlResponce object to pdf.

It's still under development and need testing ,bug report, feature request, coding, ...

-----
Usage
-----

Simply add `?format=pdf` to your url to get the pdf version of the page

------------
Install
------------

get sources
-----------

git clone https://github.com/jssevestre/django-pdf
cd django-pdf
cp django_pdf to your project or in your PYTHON_PATH

** pip install will come **

requirement
------------

http://github.com/chrisglass/xhtml2pdf/

settings.py
-----------

1. add 'django_pdf' to INSTALLED_APPS

2. add 'django_pdf.middleware.PdfMiddleware' to MIDDLEWARE_CLASSES

3. check that TEMPLATE_CONTEXT_PROCESSORS content is

::

 ("django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request")

4. and add  "django_pdf.context_processors.check_format",before )

Configuration
-------------

You can customize in your settings.py

* REQUEST_FORMAT_NAME (default is 'format')
* REQUEST_FORMAT_PDF_VALUE (default is 'pdf')    
* TEMPLATE_PDF_CHECK (default is 'DJANGO_PDF_OUTPUT')


---------------------------
Template tags and variables
---------------------------

pdf or not pdf ?
----------------

You may ask: "Wait! what if I don't want to include some parts of the HTML page in the PDF output? (like a menu)"
You'd be right, and the answer is easy:
Use the variable DJANGO_PDF_OUTPUT in your template which will be set to True if
the PDF is requested and to False otherwise.

Example:

::

 {% if not DJANGO_PDF_OUTPUT %}
        <ul id="menu">
            <li>menu item</li>
            <li>menu item</li>
            <li>menu item</li>
        </ul>
 {% endif %}

Also, you can use {% if DJANGO_PDF_OUTPUT %} to include some parts only in the PDF output.


direct link
-----------

You have a new template tag {{ pdf_link }} which will generate a link to the PDF version of the current page. :)

