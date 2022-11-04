from json import loads
from urllib.request import urlopen, Request

from app.about import UPDATE_NUMBER


def check_last_update():
    output = [False]
    req = Request(url=f"https://mrmrm.ir/update/Home%20Server.php?v={UPDATE_NUMBER}",
                  headers={'User-Agent': 'Mozilla/5.0'})
    data = loads(urlopen(req).read())
    if data['changes'] == '':
        return output
    else:
        message = "New version available, do you want to download? \nabout this update: \n"
        changes = data['changes'].split('\\n')
        message += '\n'.join(changes)
        output[0] = True
        output.append(message)
        output.append(data['link'])
        return output
