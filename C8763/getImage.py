import io

import urllib.request
import numpy as np
from PIL import Image

from NCUAI_LineBot import settings

def getImage(messageID):
    url = "https://api.line.me/v2/bot/{}/13084614743228/content".format(messageID)
    headers = {'Authorization': "Bearer {}".format(settings.LINE_CHANNEL_ACCESS_TOKEN)}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        f = io.BytesIO(response.read())

    img = Image.open(f)
    pix = np.array(img)

    print(pix)