Dependencies:
  GeoDjango and its dependencies (http://geodjango.org/docs/install.html)
  A suitable spatial database that supports distance lookup (http://geodjango.org/docs/db-api.html#id38) - right now that means only PostgreSQL / PostGIS and Oracle
  Metar - from http://homepage.mac.com/wtpollard/Software/FileSharing4.html
  DateUtil

Notes:
  You can without too much pain an suffering comment out the bits that require GeoDjango, but I personally will always be using those bits so my "official" distribution will include them.

To install / use:
  - Put the "weathertracking" directory somewhere on your $PYTHONPATH
  - Add 'weathertracking' to your INSTALLED_APPS, and run syncdb
    NOTE: Your database (if existing) will need the scripts mentioned in http://geodjango.org/docs/install.html#creating-a-spatial-database-template run against it for the models to work
