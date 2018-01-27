from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, primary_key=True)
    primary = models.CharField(max_length=255)
    secondary = models.CharField(max_length=255)
    stars = models.IntegerField(null=True)

    def __str__(self):
        return (
            ',\n\t'.join([
                'name: ' + self.name,
                'key: ' + self.key,
                'primary: ' + self.primary,
                'secondary: ' + self.secondary,
                'stars: ' + str(self.stars or 0)]))
