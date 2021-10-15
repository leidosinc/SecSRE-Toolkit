from flask import Blueprint, request, Response
import requests, yaml

grafanaBlueprint = Blueprint('grafanaAuth', __name__,)

import flask_auth

@grafanaBlueprint.route('/grafanaAuth')
def handleTeams():
    if not flask_auth.verifyCert(request):
      return Response('unauthorized', status=401)

    config = flask_auth.getConfig()

    username = request.headers.get('X-Client-DN-CN').lower().split(' ')[-1]

    # Check that the user exists in Grafana and get its user id
    grafanaSession = requests.Session()
    grafanaSession.auth = (config['grafana_admin'], config['grafana_admin_pass'])

    userId = -1
    userResp = grafanaSession.get(config['grafana_base_url'] + f'/api/users/lookup?loginOrEmail={username}')
    if 'id' not in userResp.json():
        # Create new user
        newUser = grafanaSession.post(config['grafana_base_url'] + '/api/admin/users', json={
            'name': username,
            'login': username,
            'password': config['grafana_default_password']
        })

        print(newUser.json())
        userId = newUser.json()['id']
    else:
        userId = userResp.json()['id']

    teamsUrl = config['teams_api_url'].replace('{ username }', username)
    userTeams = requests.get(teamsUrl, cert=(config['flask_cert'], config['flask_key']), verify=config['server_cert']).json()[config['teams_path']]
    for team in userTeams:
       # Check if the team exists
       teamId = -1
       grafanaTeam = grafanaSession.get(config['grafana_base_url'] + f'/api/teams/search?name={team}').json()
       if grafanaTeam['totalCount'] == 0:
           # Create new team
           newTeam = grafanaSession.post(config['grafana_base_url'] + f'/api/teams', json={
               'name': team,
            })

           teamId = newTeam.json()['teamId']
       else:
           teamId = grafanaTeam['teams'][0]['id']

       # Verify that the user is in the team
       teamUsers = grafanaSession.get(config['grafana_base_url'] + f'/api/teams/{teamId}/members').json()
       foundUser = False
       for user in teamUsers:
           if user['userId'] == userId:
               foundUser == True
               break

       if not foundUser:
           # Add user to team
           grafanaSession.post(config['grafana_base_url'] + f'/api/teams/{teamId}/members', json={
               'userId': userId
           })

    return Response('authorized', status=200)
