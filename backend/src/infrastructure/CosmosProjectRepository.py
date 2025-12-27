from azure.cosmos import ContainerProxy
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
from src.domains.User import User
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
        project=Project(readProj["name"],readProj["owner"],readProj["private"],readProj["users"],readProj["width"],readProj["height"],readProj["fps"],readProj["datetime_createdd"],readProj["datetime_modified"])
        return project
    