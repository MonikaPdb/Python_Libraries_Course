import requests
import click
import configparser

config = configparser.ConfigParser()
config.read("auth.cfg")
token = config.get('github', 'token')


# Authentication
session = requests.Session()
session.get('http://httpbin.org/cookies/set/mipyt/best')
session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}

@click.group()
def main():
    print('I do not the hell know what I am doing')
    pass



@main.command()
@click.option('--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to check star status.')
def show(repos):
    '''Simple program, that will show me if I have already given a star to the selected repository'''
    
    # Star show
    response = session.get('https://api.github.com/user')
    if response.status_code == 200:
        print('Authentication successfull')
    status = session.get('https://api.github.com/user/starred/'+repos)
    if status.status_code == 204:
        print('The repository has a star: * ', repos)
    if status.status_code == 404:
        print('The repository does not have a star: ', repos)



@main.command()
@click.option('--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to have star added.')
def add(repos):
    '''Simple program, that will give a star to the selected repository'''
    
    # Star add
    response = session.get('https://api.github.com/user')
    if response.status_code == 200:
        print('Authentication successfull')
    status = session.get('https://api.github.com/user/starred/'+repos)
    if status.status_code == 204:
        print('There is a star already')
    if status.status_code == 404:
        session.put('https://api.github.com/user/starred/'+repos)
        check = session.get('https://api.github.com/user/starred/'+repos)
        if check.status_code == 204:
            print('The star was added to the repository')
    

@main.command()
@click.option('--repos', default='pyvec/naucse.python.cz', help='Repository of which you want to have the star removed.')
def remove(repos):
    ''' A simple program, that will delete a star from the selected repository'''
    
    #Star delete
    status = session.get('https://api.github.com/user/starred/'+repos)
    if status.status_code == 204:
        session.delete('https://api.github.com/user/starred/'+repos)
        check = session.get('https://api.github.com/user/starred/'+repos)
        if check.status_code == 404:
            print('The star was deleted')  
    if status.status_code == 404:
        print('There is no star in the repository')  
        

    
main()
