# -*- coding: utf-8 -*-

"""Console script for rps."""

import click
from .log import get_log
from .asyncmongo import AsyncMongo
from .check_link import CheckLink
from .api import Api
import asyncio


def validate_url(ctx, param, value):
    try:
        return value
    except ValueError:
        raise click.BadParameter('url need to be format: tcp://ipv4:port')


@click.command()
@click.option('--svc_uri', default='http://localhost:18088/v2/system',
              envvar='SVC_URI',
              help='Segments subcell, default: http://localhost:18088/v2/system')
@click.option('--db_uri', default='mongodb://mongo:27017/mean',
              callback=validate_url,
              envvar='DB_URI',
              help='DB URI, ENV: DB_URI, default: mongodb://mongo:27017/mean')
@click.option('--port', default=80,
              envvar='SVC_PORT',
              help='Api port, default=80, ENV: SVC_PORT')
@click.option('--debug', is_flag=True)
def main(svc_uri, db_uri, port, debug):
    """Publisher for PM-1 with IPP protocol"""

    click.echo("See more documentation at http://www.mingvale.com")

    info = {
        'svc_uri': svc_uri,
        'db_uri': db_uri,
        'api_port': port
    }
    log = get_log(debug)
    log.info('Basic Information: {}'.format(info))

    loop = asyncio.get_event_loop()
    loop.set_debug(0)

    # main process
    try:
        db = AsyncMongo(db_uri)
        db_task = loop.create_task(db.reconnector())
        site = CheckLink(loop, svc_uri, db)
        api = Api(loop=loop, port=port, site=site)
        site.start()
        api.start()
        loop.run_forever()
    except KeyboardInterrupt:
        if amqp_task:
            amqp_task.cancel()
            loop.run_until_complete(amqp_task)
        if db_task:
            db_task.cancel()
            loop.run_until_complete(db_task)
        site.stop()
    finally:
        loop.stop()
        loop.close()
