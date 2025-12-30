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
from src.functions.project.createNewProjectFunction import bp as createNewProjectFunction
from src.functions.project.deleteProjectFunction import bp as deleteProjectFunction
from src.functions.project.getUsersProjects import bp as getUsersProjects
from src.functions.project.addUsersToProject import bp as addUsersToProjects
from src.functions.project.removeUserFromProjectFunction import bp as removeUserFromProject
app = func.FunctionApp()

app.register_blueprint(registerFunction)
app.register_blueprint(deleteUserFunction)
app.register_blueprint(loginUserFunction)
app.register_blueprint(createNewProjectFunction)
app.register_blueprint(deleteProjectFunction)
app.register_blueprint(getUsersProjects)
app.register_blueprint(addUsersToProjects)
app.register_blueprint(removeUserFromProject)