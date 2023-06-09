# Generated by Django 4.2.1 on 2023-05-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store_app", "0003_tag_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filter_price",
            name="price",
            field=models.CharField(
                choices=[
                    ("1 TO 10", "1 TO 10"),
                    ("10 TO 20", "10 TO 20"),
                    ("20 TO 30", "20 TO 30"),
                    ("30 TO 40", "30 TO 40"),
                    ("40 TO 50", "40 TO 50"),
                    ("50 TO 60", "50 TO 60"),
                    ("60 TO 70", "60 TO 70"),
                    ("70 TO 80", "70 TO 80"),
                    ("80 TO 90", "80 TO 90"),
                    ("90 TO 100", "90 TO 100"),
                ],
                max_length=60,
            ),
        ),
    ]
