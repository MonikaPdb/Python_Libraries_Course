
import requests
import click
import configparser
import sys
import time

config = configparser.ConfigParser()
config.read("auth.cfg")
token = config.get('github', 'token')


# Authentication
session = requests.Session()
session.get('http://httpbin.org/cookies/set/mipyt/best')
session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}

@click.group()
def main():
    print('Hello there, I am a little app.')
    pass

@main.command()
@click.option('-r', '--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to check star status.')
@click.option('-v', '--verbose', is_flag=True, help='Will print verbose messages. Can get very annoying.')
@click.option('-a','--show_all', is_flag=True, help='Will show first 100 (or less) repositories of the selected user. You can select the user with --username option.')
@click.option('-u', '--username', default = 'pyvec', help='The username of the user you want to see the repositories of.')
def show(repos, verbose, show_all, username):
    '''Simple program, that will show me if I have already given a star to the selected repository.'''
    
    # ------Star show------
    # Check that the repository exists
    if repos != 'pyvec/naucse.python.cz':
        url_check = requests.get('https://github.com/'+repos)
        if url_check.status_code == 404:
            if verbose == False:
                print('Your selected repository does not exists.','\n','The app will close in 3 seconds.')
                time.sleep(3)
                sys.exit(1)
            else:
                print('The repository you want to access does not exist, maybe you should go and check if you have the right name.','\n','And BTW the app will close in 3 seconds.')
                time.sleep(1)
                print('2 seconds')
                time.sleep(1)
                print('1 second')
                time.sleep(1)
                print('BOOOOM')
                sys.exit(1)
    # Check that the username exists          
    if show_all == True and username != 'pyvec':
        url_check = requests.get('https://api.github.com/users/'+username+'/repos')
        if url_check.status_code == 404:
            if verbose == False:
                print('User with your selected username does not exists.','\n','The app will close in 3 seconds.')
                time.sleep(3)
                sys.exit(1)
            else: 
                print('You selected a non-existent user, please, go and check the name.','\n','And BTW the app will close in 3 seconds.')
                time.sleep(1)
                print('2 seconds')
                time.sleep(1)
                print('1 second')
                time.sleep(1)
                print('BOOOOM')
                sys.exit(1)
    # Checking the star status
    response = session.get('https://api.github.com/user')
    if show_all == False:
        if response.status_code == 200 and verbose == False:
            print('Authentication successfull.')
        if response.status_code == 200 and verbose == True:
            print('Authentication successfull, wonderfully done, my dear! Let the stars shine!')
        status = session.get('https://api.github.com/user/starred/'+repos)
        if status.status_code == 204 and verbose == False:
            print('The repository has a star: * ', repos)
        if status.status_code == 204 and verbose == True:
            print('This wonderful repository has a star already, my dear! You see?: * ', repos)
        if status.status_code == 404 and verbose == False:
            print('The repository does not have a star: ', repos)
        if status.status_code == 404 and verbose == True:
            print('What a shame! This wonderful repository does not have a star: ', repos)
    # Showing top 100 (or less) repositories
    if show_all == True:
        public_repos = session.get('https://api.github.com/users/'+username)
        public_repos_num = public_repos.json()['public_repos']
        print('Number of public repos: ', public_repos_num)
        # Showing top 100
        if public_repos_num >= 100:
            show = session.get('https://api.github.com/users/'+username+'/repos?page=2&per_page=100')
            if verbose == False:
                print('The following is the top 100 of all public repositories:')
            if verbose == True:
                print('The following is the loooong list of top 100 of all public repositories of the selected user {} :'.format(username))
                print('Funny how many ofs can I put in one sentence.')
            diction = show.json()
            number = 1
            for d in diction:
                for keys, values in d.items():
                    if keys == 'name':
                        print('{}. {}'.format(number, values))
                        number = number + 1
        # Showing less then 100
        else: 
            show = session.get('https://api.github.com/users/'+username+'/repos')
            if verbose == False:
                print('The following is a list of all {} public repositories:'.format(public_repos_num))
            if verbose == True:
                print('The following is a list of all {} public repositories:'.format(public_repos_num))
                print('Only {} repositories... hopefully there will be more the next time you ask :P.'.format(public_repos_num))
            diction = show.json()
            number = 1
            for d in diction:
                for keys, values in d.items():
                    if keys == 'name':
                        print('{}. {}'.format(number, values))
                        number = number + 1

@main.command()
@click.option('-r', '--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to have star added.')
def add(repos):
    '''Simple program, that will give a star to the selected repository.'''
    
    # ------Star add------
    # Check that the repository exists
    if repos != 'pyvec/naucse.python.cz':
        url_check = requests.get('https://github.com/'+repos)
        if url_check.status_code == 404:
            print('Your selected repository does not exists.','\n','The app will close in 3 seconds.')
            time.sleep(3)
            sys.exit(1)
    # Checking the the star status and adding a star if applicable
    response = session.get('https://api.github.com/user')
    if response.status_code == 200:
        print('Authentication successfull')
    status = session.get('https://api.github.com/user/starred/'+repos)
    if status.status_code == 204:
        print('There is a star already.')
    if status.status_code == 404:
        session.put('https://api.github.com/user/starred/'+repos)
        check = session.get('https://api.github.com/user/starred/'+repos)
        if check.status_code == 204:
            print('The star was added to the repository.')
    

@main.command()
@click.option('-r','--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to have the star removed.')
def remove(repos):
    ''' A simple program, that will delete a star from the selected repository.'''
    # ------Star delete------
    # Check that the repository exists
    if repos != 'pyvec/naucse.python.cz':
        url_check = requests.get('https://github.com/'+repos)
        if url_check.status_code == 404:
            print('Your selected repository does not exists.','\n','The app will close in 3 seconds.')
            time.sleep(3)
            sys.exit(1)
    
    # Checking the star status and deleting a star if applicable
    status = session.get('https://api.github.com/user/starred/'+repos)
    if status.status_code == 204:
        session.delete('https://api.github.com/user/starred/'+repos)
        check = session.get('https://api.github.com/user/starred/'+repos)
        if check.status_code == 404:
            print('The star was deleted.')  
    if status.status_code == 404:
        print('There is no star in the repository.')  
        

    
main()
