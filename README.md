# kitovu

#### _flexible GitHub API interface_

## About

Kitovu is a thin layer around the GitHub API.  You still have to construct URI
paths yourself.  The primary benefit is automatically setting your
`Authorization` header based on a token in a config file.  There is also a
useful `get_all` method that automatically handles pagination.

## Setup

Kitovu can be used in several different ways.

### No Configuration

You can use kitovu with no configuration file.  The calls are unauthenticated,
which limits which calls you can make as well as imposing stricter rate limits.

```
>>> api = kitovu.Api()
```

### Configuration File

Kitovu can read a yaml configuration file where you can define your [personal
access token][0].  Users of GitHub Enterprise will also need to set a custom
[api endpoint][1].

```
token: 0101010101010101010101010101010101010101
```
```
hub: https://github.example.com/api/v3
```

This configuration file can be defined in one of two ways.

#### Explicit Path

```
>>> api = kitovu.Api(config='/etc/public.yaml')
```

#### Profile Name

You can tell kitovu to search for a profile in a standard location on your
system, which is determined by the [appdirs][2] module.  For example, the
profile "public" will cause kitovu to try to load the file
`/home/username/.config/kitovu/public.yaml`.

```
>>> api = kitovu.Api(profile='public')
```

## Usage

Once you setup your api object, all API calls should be available to you.

```
>>> api.get('/user/repos')
```
```
>>> payload = {'tag_name': 'v1.0.0'}
>>> api.post('/repos/username/myrepo/releases', payload)
```



[0]: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
[1]: https://developer.github.com/v3/#schema
[2]: https://github.com/ActiveState/appdirs
