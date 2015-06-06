import json
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
@click.option('--minimal', '-m', is_flag=True)
@click.option('--bulk', '-b', is_flag=True)
@click.argument('uri')
def get(api, page, per_page, minimal, bulk, uri):
    ''' perform an HTTP GET on the given URI '''
    if page or per_page:
        params = []
        if page:
            params.append('page={}'.format(page))
        if per_page:
            params.append('per_page={}'.format(per_page))
        uri = '{}?{}'.format(uri, '&'.join(params))
    if bulk:
        data = []
        for page in api.get(uri):
            if minimal:
                data.extend([item.get('name') for item in page.json()])
            else:
                data.extend(page.json())
        click.echo(json.dumps(data, sort_keys=True))
    else:
        for page in api.get(uri):
            if minimal:
                click.echo([item.get('name') for item in page.json()])
            else:
                click.echo(page.json())
