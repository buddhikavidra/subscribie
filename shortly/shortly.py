import os
import urlparse
import requests
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

class Shortly(object):
    def __init__(self, config):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/pay', endpoint='pay'),
            Rule('/manifest.json', endpoint='manifest'),
            Rule('/app.js', endpoint='appjs'),
            Rule('/sw.js', endpoint='sw'),
        ])

    def on_appjs(self, template_name, **context):
        return Response(file('app.js'), direct_passthrough=True, mimetype='application/javascript')


    def on_manifest(self, template_name, **context):
        return Response(file('manifest.json'), direct_passthrough=True, mimetype='application/json')

    def on_sw(self, template_name, **context):
        return Response(file('sw.js'), direct_passthrough=True, mimetype='application/javascript')

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')


    def on_pay(self, template_name, **context):
        message = "yolo" 
        if request.method == 'POST':
            return self.render_template('thankyou.html', message=message)
        return self.render_template('pay.html', message=message)


    def on_new_url(self,request):
        error = None
        result = ''
        if request.method == 'POST':
            #url = request.form['url']
            if not is_valid_lookup(request.form):
                error = 'Please enter a valid request'
            else:
                r = requests.post('https://www.dslchecker.bt.com/adsl/ADSLChecker.AddressOutput', 
                                 data = {'buildingnumber': request.form['buildingnumber'],
                                       'PostCode': request.form['PostCode']})
                result = r.text
                soup = BeautifulSoup(r.text, 'html.parser')
                soup.prettify()
                soup.find_all('span')
                result = {}
                result['VDSL Range A'] = {'Downstream': {'high':'', 'low':''},'Upstream': {'high':'', 'low':''}}
                result['WBC ADSL 2+'] = {'Downstream': '','Upstream': ''}

		for span in soup.find_all('span'):
		    if "VDSL Range A (Clean)" in span:
			for index, child in enumerate(span.parent.parent.children):
			    #print index, child
			    if index == 3:
				result['VDSL Range A']['Downstream']['high'] = child.text
			    if index == 5:
				result['VDSL Range A']['Downstream']['low'] = child.text
			    if index == 7:
			       result['VDSL Range A']['Upstream']['high'] = child.text
			    if index == 9:
			       result['VDSL Range A']['Upstream']['low'] = child.text
		    if "WBC ADSL 2+" in span:
			for index, child in enumerate(span.parent.parent.children):
			    print index, child
			    if index == 3:
				result['WBC ADSL 2+']['Downstream'] = child.text
			    if index == 5:
				result['WBC ADSL 2+']['Upstream'] = child.text
                return self.render_template('result.html', result=result)
        return self.render_template('new_url.html', error=error)



    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e


    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Shortly({
        'redis_host': redis_host,
        'redis_port': redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

def is_valid_lookup(form):
    return True

def base36_encode(number):
    assert number >= 0, 'positive integer required'
    if number == 0:
        return '0'
    base36 = []
    while number != 0:
        number, i = divmod(number, 36)
        base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
    return ''.join(reversed(base36))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=False, use_reloader=True)

application = create_app()


