# Generated by Django 4.1.2 on 2025-01-27 15:42

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("active", models.BooleanField(default=True)),
                ("born_health_score", models.IntegerField()),
                ("born_skill_score", models.IntegerField()),
                ("born_growth_score", models.IntegerField()),
                ("born_relationship_score", models.IntegerField()),
                ("born_money", models.IntegerField()),
                ("born_academic_level", models.IntegerField()),
                ("born_steps", models.IntegerField()),
                (
                    "born_defect",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "inactive_reason",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InstructorScore",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(10),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                ("comments", models.TextField(blank=True, max_length=1000, null=True)),
                (
                    "record_time",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2025,
                            1,
                            27,
                            15,
                            42,
                            34,
                            370440,
                            tzinfo=datetime.timezone.utc,
                        ),
                    ),
                ),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="player.player"
                    ),
                ),
            ],
        ),
    ]
