# Generated by Django 3.1.4 on 2021-04-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('nickname', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('transcode_pid', models.IntegerField(default=0)),
                ('hitting_count', models.IntegerField(default=0)),
            ],
        ),
    ]
