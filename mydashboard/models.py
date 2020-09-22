from django.db import models


# Create your models here.
class GraModel(models.Model):
	date = models.DateField(verbose_name="date de revelé des données")
	nb_owners = models.PositiveSmallIntegerField(verbose_name="nombre de proprios devant stériliser un animal")
	nb_contacted = models.PositiveSmallIntegerField(verbose_name="nombre de proprios déjà contacté")
	nb_to_contact = models.PositiveSmallIntegerField(verbose_name="nombre de proprios à contacter")

	def __str__(self):
		return f"{self.date}({self.nb_owners}, {self.nb_contacted}, {self.nb_to_contact})"

