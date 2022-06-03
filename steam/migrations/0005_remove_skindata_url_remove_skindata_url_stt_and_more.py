# Generated by Django 4.0.4 on 2022-06-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0004_alter_skindata_seeds_b_alter_skindata_seeds_g_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skindata',
            name='url',
        ),
        migrations.RemoveField(
            model_name='skindata',
            name='url_stt',
        ),
        migrations.AddField(
            model_name='skindata',
            name='urls',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='urls',
            field=models.JSONField(blank=True, null=True),
        ),
    ]