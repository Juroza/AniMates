from azure.cosmos import ContainerProxy
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
from src.domains.User import User
import datetime
class CosmosProjectRepository(ProjectRepository):
    def __init__(self,container:ContainerProxy):
        self.container=container
    def createNewProject(self, project):
        self.container.create_item(project.to_dict(),enable_automatic_id_generation=True)
        return True
    def deleteProject(self, project):
        results = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.name='{project.projectName}'",
        enable_cross_partition_query=True
        ))
        if(len(results)==0):
            return False
        for r in results:
            self.container.delete_item(r["id"], r["id"])
        return True
    def setFPS(self, project, fps):
        readProject=self.container.read_item(item=project.id,partition_key=project.id)
        if(readProject["name"]==None):
            return False
        readProject["fps"]=fps
        self.container.replace_item(readProject["id"],readProject)
    def setUsers(self, project, user):
        readProject=self.container.read_item(item=project.id,partition_key=project.id)
        if(readProject["name"]==None):
            return False
        userRep=[]
        for user in project.users:
            userRep.append(user.to_dict())

        readProject["users"]=userRep
        self.container.replace_item(readProject["id"],readProject)
    def getProject(self, id):
        readProj=self.container.read_item(item=id,partition_key=id)
        if(readProj["name"]==None):
            return None
        project=Project(readProj["name"],readProj["owner"],readProj["private"],readProj["users"],readProj["width"],readProj["height"],readProj["fps"],datetime.datetime.strptime(readProj["datetime_created"],"%Y-%m-%dT%H:%M:%S.%f"),datetime.datetime.strptime(readProj["datetime_modified"],"%Y-%m-%dT%H:%M:%S.%f"),readProj["frameCount"],readProj["frames"])
        project.setID(readProj['id'])
        return project
    def getProjectByName(self,name):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.name='{name}'",
        enable_cross_partition_query=True
        ))
        if(len(query_result)==0):
            return None
        readProj=query_result[0]
        project=Project(readProj["name"],readProj["owner"],readProj["private"],readProj["users"],readProj["width"],readProj["height"],readProj["fps"],datetime.datetime.strptime(readProj["datetime_created"],"%Y-%m-%dT%H:%M:%S.%f"),datetime.datetime.strptime(readProj["datetime_modified"],"%Y-%m-%dT%H:%M:%S.%f"),readProj["frameCount"],readProj["frames"])
        project.setID(readProj['id'])
        return project
    def getProjectsByUserName(self, name):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.owner='{name}'",
        enable_cross_partition_query=True
        ))
        myProjects=[]
        for readProj in query_result:
            project=Project(readProj["name"],readProj["owner"],readProj["private"],readProj["users"],readProj["width"],readProj["height"],readProj["fps"],datetime.datetime.strptime(readProj["datetime_created"],"%Y-%m-%dT%H:%M:%S.%f"),datetime.datetime.strptime(readProj["datetime_modified"],"%Y-%m-%dT%H:%M:%S.%f"),readProj["frameCount"],readProj["frames"])
            project.setID(readProj['id'])
            myProjects.append(project)
        query_collab_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE (ARRAY_CONTAINS(c.users,'{name}') AND c.owner!='{name}') OR (NOT c.private)",
        enable_cross_partition_query=True
        ))
        collabProjects=[]
        for readProj in query_collab_result:
            project=Project(readProj["name"],readProj["owner"],readProj["private"],readProj["users"],readProj["width"],readProj["height"],readProj["fps"],datetime.datetime.strptime(readProj["datetime_created"],"%Y-%m-%dT%H:%M:%S.%f"),datetime.datetime.strptime(readProj["datetime_modified"],"%Y-%m-%dT%H:%M:%S.%f"),readProj["frameCount"],readProj["frames"])
            project.setID(readProj['id'])
            collabProjects.append(project)
        return [myProjects,collabProjects]
    def updateProjectSettings(self, project):
        print("a2")
        readProject=self.container.read_item(item=project.id,partition_key=project.id)
        if(readProject["name"]==None):
            print("a1")
            return False
        userRep=[]
        for user in project.users:
            userRep.append(user)
        print("a3")
        print(project.projectName)
        readProject["users"]=userRep
        readProject['fps']= project.FPS
        readProject['owner']= project.owner
        readProject['name']=project.projectName
        readProject['private']=project.private
        readProject['width']=project.width
        readProject['height']=project.height
        readProject['frameCount']=project.frameCount
        readProject['frames']= project.frames
        self.container.replace_item(readProject["id"],readProject)
        print("a4")
        return True
    