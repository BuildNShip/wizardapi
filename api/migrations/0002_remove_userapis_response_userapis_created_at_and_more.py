# Generated by Django 4.1.7 on 2023-03-05 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userapis',
            name='response',
        ),
        migrations.AddField(
            model_name='userapis',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', null=True),
        ),
        migrations.AddField(
            model_name='userapis',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_column='deleted_at', null=True),
        ),
        migrations.AddField(
            model_name='userapis',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'InActive')], default=1),
        ),
        migrations.AddField(
            model_name='userapis',
            name='status_code',
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name='userapis',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='updated_at', null=True),
        ),
        migrations.CreateModel(
            name='UserApiResponses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField(default=200)),
                ('response', models.TextField(db_column='response')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'InActive')], default=1)),
                ('deleted_at', models.DateTimeField(blank=True, db_column='deleted_at', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at')),
                ('user_api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='api.userapis')),
            ],
            options={
                'db_table': 'user_api_responses',
            },
        ),
    ]
