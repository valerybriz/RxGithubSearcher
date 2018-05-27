"""
RxPy Github repository searcher
This lists the repositories that contains the keywords or language provided by the user
To make it asynchronous I'm using Reactivex, tornado and the github API
"""
import json
import os
import config as conf

from rx import Observable
from rx.subjects import Subject
from tornado import ioloop
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Application, RequestHandler, StaticFileHandler, url
from tornado.websocket import WebSocketHandler

headers = conf.headers
GIT_ORG = conf.GITHUB_API_URL+"/orgs"
# Configure the Httpclient as a curlAsyncHttpClient
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

class WSHandler(WebSocketHandler):
    orgs = conf.orgs
    def get_org_repos(self,org):
        """request the repos to the Github API"""
        http_client = AsyncHTTPClient()
        # Asynchronous request for contet
        response = http_client.fetch(GIT_ORG + org, headers=headers, method="GET")
        return response

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        self.write_message("connection opened")

        def send_response(x):
            self.write_message(json.dumps(x))

        def on_error(ex):
            print(ex)

        # A Subject is both an observable and observer, so we can both subscribe
        # to it and also feed (on_next) it with new values
        self.subject = Subject()

        user_input = self.subject.throttle_last(
            1000  # Given the last value in a given time interval
        ).start_with(
            ''  # Immediately after the subscription sends the default value
        ).filter(
            lambda text: not text or len(text) > 2
        )

        interval_obs = Observable.interval(
            60000  #refresh the value every 60 Seconds for periodic updates
        ).start_with(0)

        self.combine_latest_sbs = user_input.combine_latest(
            interval_obs, lambda input_val, i: input_val
        ).do_action(
            lambda x: send_response('clear')
        ).flat_map(
            self.get_data
        ).subscribe(send_response, on_error)

    def on_message(self, message):
        obj = json_decode(message)
        self.subject.on_next(obj['term'])

    def on_close(self):
        # Unsubscribe from observable
        #  will stop the work of all observable
        self.combine_latest_sbs.dispose()
        print("WebSocket closed")

    def get_info(self,req):
        """managing error codes and returning a list of json with content"""
        if req.code ==200:
            jsresponse = json.loads(req.body.decode("utf-8"))
            return jsresponse
        elif req.code == 403:
            print("403 error")
            jsresponse = json.loads(req.body.decode("utf-8"))
            return json.dumps("clear")
        else:
            return json.dumps("failed")

    def get_data(self,query):
        """ query the data to the API and return the contet filtered"""
        return Observable.from_list(
            self.orgs
        ).flat_map(
            lambda name: Observable.from_future(self.get_org_repos(name))
        ).flat_map(

            lambda x: Observable.from_list(

                    self.get_info(x) #transform the response to a json list

            ).filter(

                lambda val: (val.get("description") is not None and (val.get("description").lower()).find(query.lower())!= -1)
                            or (val.get("language") is not None and (val.get("language").lower()).find(query.lower())!= -1)
            ).take(10)  #just take 10 repos from each org

        ).map(lambda x: {'name': x.get("name"), 'stars': str(x.get("stargazers_count")),
                         'link': x.get("svn_url"),'description': x.get("description"), 'language': x.get("language")})


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html")

def main():
    port = os.environ.get("PORT", 8080)
    app = Application([
        url(r"/", MainHandler),
        (r'/ws', WSHandler),
        (r'/static/(.*)', StaticFileHandler, {'path': "."})
    ])
    print("Starting server at port: %s" % port)
    app.listen(port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
