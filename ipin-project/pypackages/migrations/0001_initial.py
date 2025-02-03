# Generated by Django 4.2.18 on 2025-02-03 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wheel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('version', models.CharField(max_length=20)),
                ('file_path', models.FileField(blank=True, null=True, upload_to='upload/')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('license', models.CharField(blank=True, max_length=50, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
