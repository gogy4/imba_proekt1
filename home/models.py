from django.db import models

class Home(models.Model):
    c_plot = models.ImageField(blank=True, null=True, verbose_name='Логотип C')
    cplusplus_plot = models.ImageField(blank=True, null=True, verbose_name='Логотип C++')

    class Meta:
        verbose_name = 'Логотипы C/C++ языков программирования'
        verbose_name_plural = 'Логотипы C/C++ языков программирования'
