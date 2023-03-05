from django.db import models


class UserApis(models.Model):
    INACTIVE, ACTIVE = 0, 1
    methods = (("POST", "POST"), ("GET", "GET"), ("PUT", "PUT"),
               ("PATCH", "PATCH"), ("DELETE", "DELETE"))
    statuses = ((ACTIVE, "Active"), (INACTIVE, "InActive"))

    api = models.TextField(db_column='api')
    token = models.TextField(db_column='token')
    params = models.TextField(db_column='request_params')
    method = models.TextField(db_column='method', choices=methods)
    status_code = models.IntegerField(default=200)
    status = models.IntegerField(default=ACTIVE, choices=statuses)
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at", blank=True, null=True)

    class Meta:
        db_table = "user_apis"


class UserApiResponses(models.Model):
    INACTIVE, ACTIVE = 0, 1
    statuses = ((ACTIVE, "Active"), (INACTIVE, "InActive"))

    user_api = models.ForeignKey(UserApis, on_delete=models.CASCADE, related_name='responses')
    status_code = models.IntegerField(default=200)
    response = models.TextField(db_column='response')
    status = models.IntegerField(default=ACTIVE, choices=statuses)
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "user_api_responses"
