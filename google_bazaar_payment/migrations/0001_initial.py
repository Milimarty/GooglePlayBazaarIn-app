# Generated by Django 3.1.2 on 2020-11-06 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'GooglePlay'), (1, 'Bazaar')], default=0)),
                ('refresh_token', models.CharField(blank=True, max_length=255, null=True)),
                ('scope', models.CharField(blank=True, max_length=255, null=True)),
                ('token_type', models.CharField(blank=True, max_length=255, null=True)),
                ('access_token', models.CharField(blank=True, max_length=255, null=True)),
                ('init_token', models.CharField(blank=True, max_length=255, null=True)),
                ('client_id', models.CharField(blank=True, max_length=255, null=True)),
                ('client_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('redirect_url', models.CharField(blank=True, max_length=255, null=True)),
                ('expires_in', models.BigIntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]