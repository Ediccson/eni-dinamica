from django.db import migrations


OLD_TABLE = 'app_convocatorias_convocatoria'
TARGET_TABLE = 'convocatorias'


def align_convocatorias_table(apps, schema_editor):
    connection = schema_editor.connection
    tables = set(connection.introspection.table_names())
    quote = connection.ops.quote_name

    if TARGET_TABLE in tables and OLD_TABLE not in tables:
        return
    if OLD_TABLE not in tables:
        raise RuntimeError(f'Expected table {OLD_TABLE!r} was not created.')

    if TARGET_TABLE in tables:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM {quote(OLD_TABLE)}')
            old_table_rows = cursor.fetchone()[0]
        if old_table_rows:
            raise RuntimeError(
                f'Cannot replace non-empty table {OLD_TABLE!r} with {TARGET_TABLE!r}.'
            )
        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE {quote(OLD_TABLE)}')
        return

    with connection.cursor() as cursor:
        cursor.execute(
            f'ALTER TABLE {quote(OLD_TABLE)} RENAME TO {quote(TARGET_TABLE)}'
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_convocatorias', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(align_convocatorias_table),
            ],
            state_operations=[
                migrations.AlterModelTable(
                    name='convocatoria',
                    table='convocatorias',
                ),
            ],
        ),
    ]
