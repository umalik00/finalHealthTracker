# Generated by Django 3.0.2 on 2020-06-08 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthTrackerApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergoals',
            name='goal',
            field=models.ForeignKey(db_column='goalID', on_delete=django.db.models.deletion.CASCADE, to='healthTrackerApp.Goals'),
        ),
    ]
