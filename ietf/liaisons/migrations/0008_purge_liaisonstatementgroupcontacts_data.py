# Generated by Django 2.2.17 on 2020-12-10 06:21

from django.db import migrations

from ietf.person.name import plain_name


def forward(apps, schema_editor):
    """Delete LiaisonStatementGroupContacts records"""
    LiaisonStatementGroupContacts = apps.get_model('liaisons', 'LiaisonStatementGroupContacts')
    LiaisonStatementGroupContacts.objects.all().delete()


def contacts_from_roles(roles):
    """Create contacts string from Role queryset"""
    emails = []
    for r in roles:
        if not r.person.plain and r.person.name == r.email.address:
            # Person was just a stand-in for a bare email address, so just return a bare email address
            emails.append(r.email.address)
        else:
            # Person had a name of some sort, use that as the friendly name
            person_name = r.person.plain if r.person.plain else plain_name(r.person.name)
            emails.append('{} <{}>'.format(person_name,r.email.address))
    return ','.join(emails)

def reverse(apps, schema_editor):
    """Recreate LiaisonStatementGroupContacts records
    
    Note that this does not exactly reproduce the original contents. In particular, email addresses
    in contacts or cc_contacts may have had different real names than those in the corresponding
    email.person.name field. In this case, the record will be reconstructed with the name from
    the Person model. The email addresses should be unchanged, though. 
    """
    LiaisonStatementGroupContacts = apps.get_model('liaisons', 'LiaisonStatementGroupContacts')
    Group = apps.get_model('group', 'Group')
    Role = apps.get_model('group', 'Role')
    RoleName=apps.get_model('name', 'RoleName')
    
    contact_role_name = RoleName.objects.get(slug='liaison_contact')
    cc_contact_role_name = RoleName.objects.get(slug='liaison_cc_contact')
    
    for group in Group.objects.all():
        contacts = Role.objects.filter(name=contact_role_name, group=group)
        cc_contacts = Role.objects.filter(name=cc_contact_role_name, group=group)
        if contacts.exists() or cc_contacts.exists():
            LiaisonStatementGroupContacts.objects.create(
                group_id=group.pk,
                contacts=contacts_from_roles(contacts),
                cc_contacts=contacts_from_roles(cc_contacts),
            )

class Migration(migrations.Migration):

    dependencies = [
        ('liaisons', '0007_auto_20201109_0439'),
        ('group', '0041_create_liaison_contact_roles'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]