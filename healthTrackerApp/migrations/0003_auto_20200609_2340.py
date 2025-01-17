# Generated by Django 3.0.2 on 2020-06-09 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthTrackerApp', '0002_auto_20200608_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupgoals',
            name='goal',
            field=models.ForeignKey(db_column='goalID', on_delete=django.db.models.deletion.CASCADE, to='healthTrackerApp.UserGoals'),
        ),
        migrations.AlterField(
            model_name='groupgoals',
            name='group',
            field=models.ForeignKey(db_column='groupID', on_delete=django.db.models.deletion.CASCADE, to='healthTrackerApp.UserGroups'),
        ),
    ]
