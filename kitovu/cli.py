import json
import sys
import click
from .api import Api


@click.group()
@click.option('--profile', '-p', default='default')
@click.pass_context
def cli(context, profile):
    ''' flexible GitHub API interface '''
    context.obj = Api(profile)


@cli.command()
@click.pass_obj
@click.option('--page', type=int, help='define the starting page')
@click.option('--per-page', type=int, help='define the items per page')
@click.option('--summary', '-s', is_flag=True,
              help='only output the the "name" property of each item')
@click.option('--bulk', '-b', is_flag=True,
              help='group all results together into one list')
@click.argument('uri')
def get(api, page, per_page, summary, bulk, uri):
    ''' perform an HTTP GET on the given URI '''
    if page or per_page:
        params = []
        if page:
            params.append('page={}'.format(page))
        if per_page:
            params.append('per_page={}'.format(per_page))
        uri = '{}?{}'.format(uri, '&'.join(params))
    if bulk:
        if summary:
            data = [item['name'] for page in api.get(uri) for item in page.json()]
        else:
            data = [item for page in api.get(uri) for item in page.json()]
        click.echo(json.dumps(data, sort_keys=True))
    else:
        for page in api.get(uri):
            if summary:
                click.echo([item.get('name') for item in page.json()])
            else:
                click.echo(page.json())


@cli.command()
@click.pass_obj
@click.argument('uri')
def put(api, uri):
    ''' perform an HTTP PUT on the given URI '''
    if sys.stdin.isatty():
        r = api.put(uri)
    else:
        r = api.put(uri, json=json.load(sys.stdin))
    click.echo(r.text)


@cli.command()
@click.pass_obj
@click.argument('uri')
def delete(api, uri):
    ''' perform an HTTP DELETE on the given URI '''
    if sys.stdin.isatty():
        r = api.delete(uri)
    else:
        r = api.delete(uri, json=json.load(sys.stdin))
    click.echo(r.text)
