from django.db import models

class Inspection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    supervisor = models.IntegerField(null=False)
    members = models.ManyToManyField(User)

    def __str__(self):
        # return '%s' % self.title
        return self.name
