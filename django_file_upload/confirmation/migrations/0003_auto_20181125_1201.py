# Generated by Django 2.0.3 on 2018-11-25 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation', '0002_auto_20181125_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerWiseTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('unit', models.IntegerField(choices=[(0, 'Semi-Auto'), (1, 'Auto'), (2, 'Total')])),
                ('session', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec'), (13, 'Q1'), (14, 'Q2'), (15, 'Q3'), (16, 'Q4'), (17, 'H1'), (18, 'H2')])),
                ('year', models.PositiveSmallIntegerField()),
                ('total', models.FloatField(blank=True, null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyerwise_total', to='confirmation.Buyer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='buyerwisecon',
            name='total',
        ),
    ]