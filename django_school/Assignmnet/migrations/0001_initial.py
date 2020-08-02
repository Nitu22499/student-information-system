# Generated by Django 2.2 on 2020-04-17 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assgn_title', models.CharField(blank=True, max_length=100)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('document', models.FileField(default=True, upload_to='documents/')),
                ('subject', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
