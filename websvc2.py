#!/usr/bin/env python3
#
# simple webservice to lookup provided GET URI in
# malware database and return OK (not present in
# database) or BAD (present in database) to caller.


from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine


# API URL prefix/version string - don't include leading /
# here to mimic how flask routes URI paths.
API_PREFIX = 'urlinfo/1'


# http://docs.sqlalchemy.org/en/latest/core/engines.html#engine-creation-api
# http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
# add echo=True to see SQL being executed in logs...
engine = create_engine('sqlite:///malware2.db', case_sensitive=False)
# http://flask.pocoo.org
app = Flask(__name__)
# https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(app)


class CheckUrl(Resource):
    """Given URI path, respond accordingly."""

    # handle HTTP GET, receive full URI as path.
    # path will not have a leading /
    @staticmethod
    def get(path):
        """Lookup path in malware database.

        If path == API_PREFIX + URI, parse URI string into
        {host:port} and {uri} and return reputation.
        """

        # Enable access to API_PREFIX constant
        global API_PREFIX
        # Start with empty result dict and no errors
        result = {'error': False}

        if path == API_PREFIX or path == API_PREFIX + '/':
            return result, 400
        if path.startswith(API_PREFIX):
            # lookup specific URL reputation. we receive full URI
            url = path.split('/')
            try:
                # got /prefix/host:port/uri
                host, uri = url[2], '/' + '/'.join(url[3:])
            except IndexError:
                # got /prefix/host:port
                host, uri = url[2], '/'
        else:
            # bad query, return early
            result['error'] = True
            result['message'] = 'bad requst'
            return result, 400

        # Don't use string formatting, avoid sql injection!
        # https://docs.python.org/3/library/sqlite3.html
        sql = "select domain, uri from malware2 where domain=(:host) and uri=(:uri)"

        query = None
        try:
            # Setup database connection and run query
            connection = engine.connect()
            query = connection.execute(sql, (host, uri))
            output = query.cursor.fetchall()
        finally:
            if query:
                query.cursor.close()

        try:
            # in database == malware
            # output[row][column]
            # Columns: host:port|URI
            result['url'] = output[0][0] + output[0][1]
            result['reputation'] = 'BAD'
            result['message'] = 'found in database'
        except IndexError:
            # not in database == OK
            result['url'] = host + uri
            result['reputation'] = 'OK'
            result['message'] = 'not in database'

        return result, 200


# http://flask.pocoo.org/snippets/57/
# TODO: <path:path> passes the full URI, but we could compile a regex
# TODO: to ensure 'path' is really valid else just return HTTP 400.
api.add_resource(CheckUrl, '/<path:path>')


# Run everything if we're not being imported...
if __name__ == '__main__':
    app.run()
