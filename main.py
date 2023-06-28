# import requirements needed
from flask import Flask, render_template, request
from utils import get_base_url
import requests
import os
import logging

logging.basicConfig(filename='app.log',
                    level=logging.DEBUG)  # Set the log file and log level
# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
  app = Flask(__name__)
else:
  app = Flask(__name__, static_url_path=base_url + 'static')


# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
  return render_template('index.html')


#Bird-Or-Not model
API_URL = "https://api-inference.huggingface.co/models/Samrita/Bird-Or-Not"
headers = {"Authorization": f"Bearer {os.environ['Samritas_API_Key']}"}


def query(filename):
  with open(filename, "rb") as f:
    data = f.read()
  response = requests.post(API_URL, headers=headers, data=data)
  return response.json()


#FL-Invasive-Bird-Detector Model
API_URL1 = "https://api-inference.huggingface.co/models/Samrita/FL-Invasive-Bird-Detector"
headers1 = {"Authorization": f"Bearer {os.environ['Samritas_API_Key']}"}


def query1(filename):
  with open(filename, "rb") as f:
    data = f.read()
  response = requests.post(API_URL1, headers=headers1, data=data)
  return response.json()


possible = {
  'bulbul': 'a Red-Whiskered Bulbul',
  'peacock': 'an Indian Peacock',
  'Non-invasive': 'a non-invasive species',
  'European%20Starling%20-%20Invasive': 'a European Starling',
  'Muscovy%20Duck': 'a Muscovy Duck',
  'House%20sparrow%20%28Passer%20domesticus%29': 'a House Sparrow',
  "Feral_pigeon%20%281%29": "a Feral Pigeon"
}


@app.route('/DetectorResult', methods=['POST'])
def DetectorResult():
  for i in os.listdir('static/temp'):
    filepath=os.path.join('static', 'temp', i)
    if os.path.isfile(filepath):
      os.remove(filepath)
  if not request.files['file']:
      Flask.abort(403)
  file = request.files['file']
  file_name = file.filename
  temp_path = 'static/temp/' + file_name
  file.save(temp_path)
  isBird = query(temp_path)
  Bird = query1(temp_path)
  try:
      isbird=isBird[0]['label'] == 'Bird'
      b = possible[Bird[0]['label']]
      print(isbird)
      return render_template('result.html',
                             image_path=temp_path,
                             image_class=(b if isbird else 'not a bird'))
      
  except KeyError:
      logging.debug(isBird)
      return render_template('result.html', image_path=temp_path,image_class='Hugging Face Error: Try Again')


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
  # IMPORTANT: change url to the site where you are editing this file.
  website_url = 'https://diamond-dragons.2023-summer-computer-vision.repl.co'

  print(f'Try to open\n\n    {website_url}' + base_url + '\n\n')
  app.run(host='0.0.0.0', port=port, debug=True)
