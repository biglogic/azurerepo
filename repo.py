from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
import csv

# Fill in with your personal access token and org URL
personal_access_token = 'access_token'
organization_url = 'organization_url'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
#core_client = connection.clients.get_core_client()

core_client_git = connection.clients.get_git_client()
get_projects_response = core_client_git.get_repositories()

core_client_build = connection.clients.get_build_client()
project_list = []

print("########## Repos #############")
for project in get_projects_response:
    list1 = [project.project.name, project.name]
    project_list.append(list1)

print(project_list)

print("######### Pipeline ###########")
dumylist = []
list2 = []
querylist = project_list

for list_value in project_list:
    for pipeline in core_client_build.get_builds(list_value[0]).value:
        if pipeline.definition.id not in dumylist:
            dumylist.append(pipeline.definition.id)
            list3=[list_value[0] , pipeline.repository.name , pipeline.definition.name]
            list2.append(list3)     


print(list2)
                
complete_list = []

for list_value in project_list:
    is_pipeline = 0
    for mylist in list2:
        if list_value[1] == mylist[1]:
            is_pipeline = 1
            complete_list.append([list_value[0], list_value[1], mylist[2]])
    if is_pipeline == 0:
        complete_list.append([list_value[0], list_value[1], ""])


                 
with open('azure.csv', 'w', newline='') as file:
   for repolist in complete_list: 
      print(repolist) 
      writer = csv.writer(file , delimiter="," )
      writer.writerow(repolist)
