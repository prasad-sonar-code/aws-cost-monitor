import boto3
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime, timedelta

console = Console()

@click.group()
def cli():
    """AWS Cost Monitor - Track your AWS spending"""
    pass

@cli.command()
def instances():
    """List all running EC2 instances"""
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    table = Table(title="Running EC2 Instances")
    table.add_column("Instance ID", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Launch Time", style="magenta")

    count = 0
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            table.add_row(
                instance['InstanceId'],
                instance['InstanceType'],
                instance['State']['Name'],
                str(instance['LaunchTime'].strftime('%Y-%m-%d %H:%M'))
            )
            count += 1

    console.print(table)
    console.print(f"\n[bold green]Total running instances: {count}[/bold green]")

@cli.command()
def costs():
    """Show AWS costs for current month"""
    ce = boto3.client('ce', region_name='us-east-1')

    today = datetime.today()
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    table = Table(title=f"AWS Costs ({start} to {end})")
    table.add_column("Service", style="cyan")
    table.add_column("Cost (USD)", style="green")

    total = 0
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        if amount > 0:
            table.add_row(service, f"${amount:.4f}")
            total += amount

    console.print(table)
    console.print(f"\n[bold red]Total this month: ${total:.2f}[/bold red]")

@cli.command()
def buckets():
    """List all S3 buckets"""
    s3 = boto3.client('s3', region_name='ap-south-1')
    response = s3.list_buckets()

    table = Table(title="S3 Buckets")
    table.add_column("Bucket Name", style="cyan")
    table.add_column("Created", style="green")

    for bucket in response['Buckets']:
        table.add_row(
            bucket['Name'],
            str(bucket['CreationDate'].strftime('%Y-%m-%d'))
        )

    console.print(table)
    console.print(f"\n[bold green]Total buckets: {len(response['Buckets'])}[/bold green]")

if __name__ == '__main__':
    cli()
