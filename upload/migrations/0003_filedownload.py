# Generated by Django 2.0.3 on 2018-03-14 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_file_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_field', models.FileField(upload_to='downloads/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]