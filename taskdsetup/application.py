
import click
import taskdsetup.init
import taskdsetup.keys
import taskdsetup.user
import taskdsetup.user_keys
import taskdsetup.config

@click.group()
@click.option('--taskddata', default='/tmp/var/taskd')
@click.pass_context
def cli(ctx, taskddata, obj={}):
    ctx.obj['TASKDDATA'] = taskddata

@cli.command()
@click.option('--source')
@click.option('--cn', default='localhost')
@click.option('--server', default='localhost')
@click.pass_context
def init(ctx, source, cn, server):
    taskdsetup.init.main(ctx.obj['TASKDDATA'], source, cn, server)

@cli.command()
@click.pass_context
def keys(ctx):
    taskdsetup.keys.main(ctx.obj['TASKDDATA'])

@cli.command()
@click.option('--org', default='Public')
@click.option('--full-name', default='Testing')
@click.pass_context
def user(ctx, org, full_name):
    taskdsetup.user.main(ctx.obj['TASKDDATA'], org, full_name)

@cli.command()
@click.option('--user-name', default='testing')
@click.pass_context
def userkeys(ctx, user_name):
    taskdsetup.user_keys.main(ctx.obj['TASKDDATA'], user_name)

@cli.command()
@click.option('--site', default='localhost')
@click.option('--port', default='53589')
@click.option('--dot-task', default='/tmp/.task')
@click.pass_context
def config(ctx, site, port, dot_task):
    taskdsetup.config.main(ctx.obj['TASKDDATA'], site, port, dot_task)

def main():
    cli(obj={})

if __name__ == '__main__':
    main()
