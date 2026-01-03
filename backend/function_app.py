import sys
import os

sys.path.append(os.path.dirname(__file__))

import azure.functions as func
import datetime
import json
import logging
from src.functions.user.registerFunction import bp as registerFunction
from src.functions.user.deleteUserFunction import bp as deleteUserFunction
from src.functions.user.loginUserFunction import bp as loginUserFunction
from src.functions.user.getAllUsersFunction import bp as getAllUsersFunction
from src.functions.project.createNewProjectFunction import bp as createNewProjectFunction
from src.functions.project.deleteProjectFunction import bp as deleteProjectFunction
from src.functions.project.getUsersProjects import bp as getUsersProjects
from src.functions.project.addUsersToProject import bp as addUsersToProjects
from src.functions.project.removeUserFromProjectFunction import bp as removeUserFromProject
from src.functions.project.editProjectFunction import bp as editProjectFunction
from src.functions.frame.getFrameURLFunction import bp as getFrameURLFunction
from src.functions.frame.uploadFrameFunction import bp as uploadFrameFunction
from src.functions.frame.addFrameFunction import bp as addFrameToProjectFunction
from src.functions.frame.loadFrameByNameFunction import bp as loadFrameByName
from src.functions.frame.deleteFrameByNameFunction import bp as deleteFrameByName
from src.functions.frame.updateFrameFunction import bp as updateFrameFunction
app = func.FunctionApp()

app.register_blueprint(registerFunction)
app.register_blueprint(deleteUserFunction)
app.register_blueprint(loginUserFunction)
app.register_blueprint(createNewProjectFunction)
app.register_blueprint(deleteProjectFunction)
app.register_blueprint(getUsersProjects)
app.register_blueprint(addUsersToProjects)
app.register_blueprint(removeUserFromProject)
app.register_blueprint(getAllUsersFunction)
app.register_blueprint(editProjectFunction)
app.register_blueprint(getFrameURLFunction)
app.register_blueprint(uploadFrameFunction)
app.register_blueprint(addFrameToProjectFunction)
app.register_blueprint(loadFrameByName)
app.register_blueprint(deleteFrameByName)
app.register_blueprint(updateFrameFunction)