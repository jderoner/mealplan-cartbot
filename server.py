from flask import Flask
from flask import Response
from flask import request

import json
import freshdirect

from mechanize import Browser
from bs4 import BeautifulSoup as BS
import urllib

app = Flask(__name__)

@app.route("/addtocart", methods=['POST'])
def add_to_cart():
    """
    """

    data = request.json
    resp = Response(u'%s')
    
    uid = data[ "uid" ]
    pwd = data[ "pwd" ]
    items = data[ "items" ]

    params = { "items": items }
    params = urllib.quote( json.dumps( params ) ).replace( '%27', '%22' ).replace( '%20', '' )
    
    #print params
    
    br = Browser()
    br.addheaders = [('User-agent', 'Firefox')]
    br.set_handle_robots(False)
    br.open('https://www.freshdirect.com/login/login.jsp')
    br.select_form(name="fd_login")
    br['userid'] = uid
    br['password'] = pwd
    br.submit()
    
    #items = data[ "items" ]

    br.addheaders = [
        ('Content-Type', 'application/x-www-form-urlencoded'), 
        ('User-agent', 'Firefox') ]

    # encoding the dict is producing single quote (%27) when it should do double (%22)
    #br.open( "https://www.freshdirect.com/api/addtocart", "data=%7B%22items%22%3A%5B%7B%22salesUnit%22%3A%22EA%22%2C%22quantity%22%3A%223%22%2C%22skuCode%22%3A%22FRU0069115%22%2C%22pageType%22%3A%22BROWSE%22%7D%5D%7D")
    br.open( "https://www.freshdirect.com/api/addtocart", "data=" + params )
    
    soup = BS(br.response().read())
    
    
    #resp = Response(u'%s' % json_output)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'

    return resp


def validate_input(input):
    """
    Check if the user's
    :param str input: the user's input
    :return bool:
        - True if the input is OK, otherwise False.
        - A response if the input is illegal, otherwise None.
    """
    if input is None:
        resp = Response(u'Missing parameter')
        resp.status_code = 400
        return False, resp

    return True, None


if __name__ == '__main__':
    app.run(host='0.0.0.0')
