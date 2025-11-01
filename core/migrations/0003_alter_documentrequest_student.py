# Generated migration to convert DocumentRequest.student from ManyToMany to ForeignKey

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_notificationrecipient_deliveredat'),
    ]

    operations = [
        # Step 1: Remove the ManyToMany field (this will drop the M2M table)
        migrations.RemoveField(
            model_name='documentrequest',
            name='student',
        ),
        # Step 2: Add ForeignKey field (nullable=True initially, then we'll make it non-null)
        migrations.AddField(
            model_name='documentrequest',
            name='student',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='document_requests',
                to='core.student'
            ),
        ),
        # Step 3: Since there's no existing data, we can make it non-null now
        # But we need to do this in a separate operation
        migrations.AlterField(
            model_name='documentrequest',
            name='student',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='document_requests',
                to='core.student'
            ),
        ),
    ]

