import click
from .engine import Engine


@click.group()
@click.option('--profile', '-p', default='default')
@click.pass_context
def cli(context, profile):
    ''' flexible GitHub API interface '''
    context.obj = Engine(profile)


@cli.command()
@click.pass_obj
@click.option('--page', type=int)
@click.option('--per-page', type=int)
@click.argument('uri')
def get(api, page, per_page, uri):
    ''' perform an HTTP GET on the given URI '''
    if page or per_page:
        params = []
        if page:
            params.append('page={}'.format(page))
        if per_page:
            params.append('per_page={}'.format(per_page))
        uri = '{}?{}'.format(uri, '&'.join(params))
    for page in api.get(uri):
        data = page.json()
        names = [item.get('name') for item in data]
        click.echo(names)
