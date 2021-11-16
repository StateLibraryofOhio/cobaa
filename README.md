# COBAA

Title selection application for the Celebrating Ohio Book Awards & Authors (COBAA) grant.

## Description

The Celebrating Ohio Book Awards & Authors (COBAA) grant is an opportunity for Ohio libraries to apply for federal LSTA grant funds to build or expand a collection of books receiving honors and awards in Ohio and by Ohio authors. This title selection application makes applying easier by providing a browsable and searchable interface of eligible titles for the following awards:


* Ansfield-Wolf Book Award
* Buckeye Children's & Teen Book Awards
* Choose to Read Ohio Award Booklists
* Dayton Literary Peace Prize
* Floyd's Pick Book Award
* James Cook Book Award
* Norman A. Sugarman Children’s Biography Award
* Ohioana Book Awards
* Thurber Prize for American Humor


For more information about the grant, [visit this page](https://library.ohio.gov/services-for-libraries/lsta-grants/cobaa-grant/) on the State Library of Ohio website.


# Tools Used

* Django
* PostgreSQL
* Bootstrap 5

# Usage

The title selection app is a Django web application. It can be configured to run on any web server or as a cloud web app (i.e. Azure App Service). To run the application locally, ensure that Python is installed, install the requirements for the app, and run the migrations and collectstatic

```python
python3 -m pip install -r requirements.txt
export SECRET_KEY=INSERT_SECRET_KEY_HERE
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
```

Django expects to find your `SECRET_KEY` as an environment variable, but you can explicitly configure it in the [local.py](/cobaa/settings/local.py) or other settings file. There are also two management commands that have been created to easily import and export book information (title, authors, awards, tags, etc.):


```python3 manage.py import_books filename.txt```  
This will import specified file. Inspect the [import_books.py](/books/management/commands/import_books.py) for an example of the expected format.

```python3 manage.py export_books```  
This will export existing books and related information into an export.csv file. This can be used as a backup.

## License

MIT License

Copyright (c) 2021 State Library of Ohio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
