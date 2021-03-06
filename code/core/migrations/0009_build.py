# Generated by Django 2.0.6 on 2018-06-27 17:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_repository'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('commit_id', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=200)),
                ('committer', models.CharField(max_length=200)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('failed', 'Failed'), ('queued', 'Queued'), ('running', 'Running'), ('success', 'Success')], default='queued', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='core.Repository')),
            ],
        ),
    ]
