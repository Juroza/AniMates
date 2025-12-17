import azure.functions as func
import datetime
import json
import logging
from src.functions.registerFunction import bp as registerFunction
from src.functions.deleteUserFunction import bp as deleteUserFunction
from src.functions.loginUserFunction import bp as loginUserFunction

app = func.FunctionApp()

app.register_blueprint(registerFunction)
app.register_blueprint(deleteUserFunction)
app.register_blueprint(loginUserFunction)
