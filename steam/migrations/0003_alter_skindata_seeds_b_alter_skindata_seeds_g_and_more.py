# Generated by Django 4.0.4 on 2022-06-02 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0002_rename_skinlogs_skinlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skindata',
            name='seeds_b',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skindata',
            name='seeds_g',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skindata',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skindata',
            name='url_stt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='seeds_b',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='seeds_g',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='urls',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
