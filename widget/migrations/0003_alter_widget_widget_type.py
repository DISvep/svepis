# Generated by Django 5.1.4 on 2025-02-23 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0002_widget_height_widget_width_widget_z_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('text', 'Text'), ('image', 'Image')], max_length=50),
        ),
    ]
