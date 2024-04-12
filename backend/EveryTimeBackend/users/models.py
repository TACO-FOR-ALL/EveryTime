from django.db import models

class SendMail(models.Model):
    email = models.EmailField(unique=True, verbose = 'Mail Address')
    
    def __str__(self):
        return self.email