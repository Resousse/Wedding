from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from threading import Thread
import requests
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
  def do_POST(self):
    status = False
    try:
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length)
        url = 'https://api.trello.com/1/cards?key=c2d06be31329a6038f5e296a9759bd50&token=31609cd6094852d16850a30962bf8516f9f40b01fda773fa6f3a99d1eb72dc89&idList=5fbd68c43cd0dc77f36dcd50&name={}&desc={}'

        js = json.loads(body)
        nom = "Famille {} {}".format(js['Prenom'], js['Nom'])
        
        description = "{}\n{}\n\n\nDate réponse : {}".format(js['Prenom']+" " + js['Nom'], js['Invités'], js['Date'])
        url = url.format(urllib.parse.quote_plus(nom), urllib.parse.quote_plus(description))
        r = requests.post(url)
        if r:
            rep = json.loads(r.text)
            urllab = 'https://api.trello.com/1/cards/{}/idLabels?key=c2d06be31329a6038f5e296a9759bd50&token=31609cd6094852d16850a30962bf8516f9f40b01fda773fa6f3a99d1eb72dc89&value={}'
            stat = '5fbd66ce1258da48af20be7f'
            if js['Statut'] == 'Viennent':
                stat = '5fbd66ce1258da48af20be79'
            urllab = urllab.format(rep['id'], stat)
            s = requests.post(urllab)
            if s:
                status = True
    except:
        pass
    
   
    if status:
        self.send_response(200)
    else:
        self.send_response(404)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    if status:
        self.wfile.write(str("OK").encode("utf-8"))
    else:
        self.wfile.write(str("KO").encode("utf-8"))
    
if __name__ == "__main__":
    server = HTTPServer(('', 8001), handler)
    server.url = 'http://localhost:{}'.format(server.server_port)
    server.serve_forever() 
