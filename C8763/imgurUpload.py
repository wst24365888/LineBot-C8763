from imgurpython import ImgurClient

client_id = 'a0ebd7916adaffe'
client_secret = 'a98512f44c8960c1e0f35134891de43e1961b26a'
access_token = '682473edde4f19584dec103a58efc91d639c1d91'
refresh_token = '42644a63e3cd88011d05e7fde864756b65cf0298'

def getauthorize():

    client = ImgurClient(client_id, client_secret)

    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    pin = input("Enter pin code: ")

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print("Access token:  {0}".format(credentials['access_token']))
    print("Refresh token: {0}".format(credentials['refresh_token']))
    return client


def setauthorize():
    return ImgurClient(client_id, client_secret, access_token, refresh_token)


def upload(client, path, config):
    image = client.upload_from_path(path, config=config, anon=False)
    return image

# getauthorize()
