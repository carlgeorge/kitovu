import json
import sys
import click
from .api import Api


@click.group()
@click.option('--no-auth', '-n', is_flag=True)
@click.option('--config', '-c')
@click.option('--profile', '-p', default='default')
@click.pass_context
def cli(context, no_auth, profile, config):
    ''' flexible GitHub API interface '''
    if no_auth:
        context.obj = Api()
    elif config:
        context.obj = Api(config=config)
    else:
        context.obj = Api(profile=profile)


@cli.command()
@click.pass_obj
@click.option('--page-number', '-p', type=int, help='define the starting page')
@click.option('--per-page', '-P', type=int, help='define the items per page')
@click.option('--all-pages', '-a', is_flag=True,
              help='get results from all pages')
@click.option('--summary', '-s', is_flag=True,
              help='only output the "name" property of each item')
@click.argument('uri')
def get(api, page_number, per_page, all_pages, summary, uri):
    ''' perform an HTTP GET on the given URI '''
    # setup the query parameters
    if page_number or per_page:
        params = []
        if page_number:
            params.append('page={}'.format(page_number))
        if per_page:
            params.append('per_page={}'.format(per_page))
        uri = '{}?{}'.format(uri, '&'.join(params))
    # make the call
    if all_pages:
        data = []
        for response in api.get_all(uri):
            for item in response.json():
                if summary:
                    data.append(item['name'])
                else:
                    data.append(item)
    else:
        response = api.get(uri)
        if summary:
            data = [item['name'] for item in response.json()]
        else:
            data = response.json()
    click.echo(json.dumps(data, sort_keys=True))


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
