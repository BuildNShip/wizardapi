from django.db import models

class UserApis(models.Model):
    methods = (("POST", "POST"), ("GET", "GET"), ("PUT", "PUT"), 
    ("PATCH", "PATCH"), ("DELETE", "DELETE"))

    api = models.TextField(db_column='api')
    token = models.TextField(db_column='token')
    params = models.TextField(db_column='request_params')
    response = models.TextField(db_column='response')
    method = models.TextField(db_column='method', choices=methods)

    class Meta:
        db_table = "user_apis"