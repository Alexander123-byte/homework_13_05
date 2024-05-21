from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название", help_text="Укажите название курса")
    preview_image = models.ImageField(upload_to='materials/course', blank=True, null=True,
                                      verbose_name="Превью (картинка)", help_text="Загрузите картинку")
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Укажите описание курса")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Название", help_text="Укажите название урока")
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Укажите описание урока")
    preview_image = models.ImageField(upload_to='materials/lesson', verbose_name="Превью (картинка)", blank=True,
                                      null=True, help_text="Загрузите картинку")
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True,
                                help_text="Добавьте ссылку на видео")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
