# Generated by Django 4.0.4 on 2022-06-02 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0008_alter_url_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skindata',
            name='seeds_b',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skindata',
            name='seeds_g',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skindata',
            name='urls',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='seeds_b',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='seeds_g',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skinlog',
            name='urls',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Url',
        ),
    ]