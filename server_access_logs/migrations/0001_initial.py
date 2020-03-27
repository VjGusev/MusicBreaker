# Generated by Django 2.2 on 2020-03-27 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLogsModel',
            fields=[
                ('sys_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_key', models.CharField(blank=True, max_length=1024)),
                ('request_path', models.CharField(blank=True, max_length=1024)),
                ('request_method', models.CharField(blank=True, max_length=8)),
                ('request_data', models.TextField(blank=True, null=True)),
                ('request_ip_address', models.CharField(blank=True, max_length=45)),
                ('request_referrer', models.CharField(blank=True, max_length=512, null=True)),
                ('request_timestamp', models.DateTimeField(blank=True)),
                ('response_status', models.CharField(blank=True, max_length=8)),
                ('response_timestamp', models.DateTimeField(blank=True)),
                ('processed_time', models.CharField(blank=True, max_length=8)),
            ],
            options={
                'db_table': 'access_logs',
            },
        ),
    ]
