# SPDX-License-Identifier: AGPL-3.0-or-later
# Hand-authored initial migration (NetBox disables makemigrations in production). Verify with:
#   python manage.py makemigrations netbox_data_link --check --dry-run   (on a dev/ephemeral NetBox)
#
# The per-PORT child models (STPInterface, LLDPInterface, DHCPSnoopingInterface) are OneToOne to
# dcim.Interface, so the DB enforces "one override row per port" via the OneToOne unique index;
# the per-device singletons are OneToOne to dcim.Device the same way. Both depend on dcim's initial
# migration (Device + Interface both ship there).
import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("dcim", "0001_initial"),
        ("extras", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="STPConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("mode", models.CharField(default="rstp", max_length=8)),
                (
                    "priority",
                    models.PositiveIntegerField(
                        default=32768,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(61440),
                        ],
                    ),
                ),
                (
                    "device",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stp_config",
                        to="dcim.device",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "STP Config", "ordering": ["device"]},
        ),
        migrations.CreateModel(
            name="STPInterface",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                (
                    "priority",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(240),
                        ],
                    ),
                ),
                ("edge_port", models.BooleanField(default=False)),
                ("bpdu_guard", models.BooleanField(default=False)),
                ("root_guard", models.BooleanField(default=False)),
                (
                    "interface",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stp_interface",
                        to="dcim.interface",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "STP Interface", "ordering": ["interface"]},
        ),
        migrations.CreateModel(
            name="LLDPConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("admin_status", models.CharField(default="enabled", max_length=8)),
                (
                    "transmit_interval",
                    models.PositiveIntegerField(
                        default=30, validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "hold_multiplier",
                    models.PositiveIntegerField(
                        default=4, validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "device",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lldp_config",
                        to="dcim.device",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "LLDP Config", "ordering": ["device"]},
        ),
        migrations.CreateModel(
            name="LLDPInterface",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("admin_status", models.CharField(max_length=8)),
                (
                    "interface",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lldp_interface",
                        to="dcim.interface",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "LLDP Interface", "ordering": ["interface"]},
        ),
        migrations.CreateModel(
            name="DHCPSnoopingConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("enabled", models.BooleanField(default=False)),
                (
                    "vlans",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(
                            validators=[
                                django.core.validators.MinValueValidator(1),
                                django.core.validators.MaxValueValidator(4094),
                            ]
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "device",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dhcp_snooping_config",
                        to="dcim.device",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "DHCP Snooping Config", "ordering": ["device"]},
        ),
        migrations.CreateModel(
            name="DHCPSnoopingInterface",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("trusted", models.BooleanField(default=False)),
                (
                    "interface",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dhcp_snooping_interface",
                        to="dcim.interface",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={"verbose_name": "DHCP Snooping Interface", "ordering": ["interface"]},
        ),
    ]
