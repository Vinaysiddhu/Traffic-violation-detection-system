# Generated by Django 4.2.3 on 2023-08-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trafficapp', '0005_rename_image_tripleride_detection_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalJump_Detection',
            fields=[
                ('SJ_ID', models.AutoField(primary_key=True, serialize=False)),
                ('VIDEO', models.FileField(upload_to='images/')),
            ],
            options={
                'db_table': 'signaljump_detection',
            },
        ),
    ]
