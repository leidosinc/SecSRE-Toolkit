#!/usr/bin/python3

from flask import Flask, Response, request
import requests, os, yaml, sys
from OpenSSL import crypto

app = Flask(__name__)
try:
    import grafanaHelper
    app.register_blueprint(grafanaHelper.grafanaBlueprint)
except Exception as e:
    print(e)

config = {}
with open('/etc/flask_auth/flask_config.yml', 'r') as yamlfile:
    config = yaml.load(yamlfile)
    yamlfile.close()

def getConfig():
  return config

def verifyCert(request):
    # Retrieve and sanitize client certificate passed by nginx
    headerCert = request.headers.get('X-SSL-CERT').strip().replace('\t', '')

    try:
        clientCert = crypto.load_certificate(crypto.FILETYPE_PEM, headerCert)
    except Exception as e:
        print(type(e), e)

    # Get the username from the DN
    certDN = clientCert.get_subject()
    print("CN: ", certDN.commonName)
    username = certDN.commonName.lower().split(' ')[-1] 
    print("Username: ", username)

    # Get the name of the certificate authority for the cert
    certAuthority = clientCert.get_issuer()
    issuerName = certAuthority.commonName.lower().replace(' ', '-')

    # Pull the user's cert from the using the issuer's API
    pkiURL = config['pki_api_url'].replace('{ issuerName }', issuerName).replace('{ username }', username)
    response = bytes.decode(requests.get(pkiURL, cert=(config['flask_cert'], config['flask_key']), verify=config['server_cert']).content)
    pkiCert = crypto.load_certificate(crypto.FILETYPE_PEM, response)

    # Verify that the provided client cert is the same as the cert provided by the PKI API
    if pkiCert.digest('sha256') == clientCert.digest('sha256'):
        print('URI: ', request.headers.get('X-Original-URI'))
        print('Port: ', request.headers.get('Port'))
        print('Forwarded: ', request.headers.get('X-Forwarded-For'))

        return True

    return False

# Handle auth requests from nginx
@app.route('/auth')
def authorize():
    if verifyCert(request):
        return Response('authorized', status=200)
    
    return Response('unauthorized', status=401)



if __name__ == '__main__':
    app.run(debug=config['debug_flask_auth'],host=config['flask_auth_host'],port=config['flask_auth_port'])
