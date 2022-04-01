import click

import src.api.documents_service as documents_service
import src.cli.utils as cli_utils

@click.group(help = 'Commands related to documents (the postbox).')
def documents():
    pass


@click.command(help = 'List all documents.')
def documents_list():
    session = cli_utils.get_session_from_cache()
    if not session:
        click.echo(
            'No session cached. Please login via `pycomdir login`', err=True)
        return
    service = documents_service.DocumentsService(session)
    try:
        res = service.list_documents(session)
        print(res)
    except RuntimeError as err:
        cli_utils.handle_error(err)

documents.add_command(documents_list)
