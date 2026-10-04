from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('complaints', '0010_complaint_resolution_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='assigned_to',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='assigned_complaints',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
