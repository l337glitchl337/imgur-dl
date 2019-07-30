import requests
import json
import os
from multiprocessing.pool import ThreadPool

class Imgur:

  def __init__(self, clientid):
    self.clientid = clientid
    self.session = requests.session()
    self.headers = headers = {"Authorization" : f"Client-ID {self.clientid}"}

  def fetch(self, url):
    data = self.session.get(url).content
    filename = f"{os.getcwd()}/MyImages/{os.path.basename(url)}"
    with open(filename, "wb") as f:
      f.write(data)
    print(f"Downloaded {os.path.basename(url)}")

  def fetch_links(self, url, threads=10):
    result = json.loads(self.session.get(url, headers=self.headers).content)
    imagelist = []
    for x in result["data"]["images"]:
      imagelist.append(x["link"])
    print(f"Found {len(imagelist)} images from {url}")
    r = input("Download images?(y/n): ")
    if r.lower() == "y":
      ThreadPool(threads).map(self.fetch, imagelist)
    else:
      pass

if __name__ == "__main__":
  if os.path.exists("MyImages") == False:
    try:
      os.mkdir(f"{os.getcwd()}/MyImages")
    except:
      print("Error creating directory")
  else:
    pass
  albumhash = os.path.basename(input("Link to album: "))
  url = f"https://api.imgur.com/3/album/{albumhash}"
  imgur = Imgur("a7396fe5d5d27da")
  imgur.fetch_links(url)
