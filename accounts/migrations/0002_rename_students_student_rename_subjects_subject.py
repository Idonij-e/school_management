# Generated by Django 4.1 on 2022-08-08 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Students',
            new_name='Student',
        ),
        migrations.RenameModel(
            old_name='Subjects',
            new_name='Subject',
        ),
    ]
