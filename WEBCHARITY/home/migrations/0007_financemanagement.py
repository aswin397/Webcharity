# Generated by Django 4.2.5 on 2023-09-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_remove_requestdetailstbl_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="FinanceManagement",
            fields=[
                ("FinID", models.AutoField(primary_key=True, serialize=False)),
                ("DetailsId", models.IntegerField()),
                ("FromID", models.CharField(max_length=10)),
                ("ToID", models.CharField(max_length=10)),
                ("CrAmount", models.CharField(max_length=20)),
                ("DataAndTime", models.DateTimeField()),
                ("Status", models.IntegerField()),
            ],
        ),
    ]
