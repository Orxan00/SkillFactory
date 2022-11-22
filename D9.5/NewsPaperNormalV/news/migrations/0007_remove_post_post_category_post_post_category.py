# Generated by Django 4.1 on 2022-09-09 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_categorysubscribe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_category',
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='news.category'),
        ),
    ]