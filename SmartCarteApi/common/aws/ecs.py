import os

from SmartCarteApi.common.aws import get_boto_client



def run_fargate_monolith_task(task):

    client = get_boto_client('ecs')
    response = client.run_task(
        cluster='default',
        count=1,
        enableECSManagedTags=True,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'assignPublicIp': 'ENABLED',
                'securityGroups': [os.environ['FARGATE_MONOLITH_SECURITY_GROUP']],
                'subnets': [
                    os.environ['FARGATE_SUBNET_ID1'],
                    os.environ['FARGATE_SUBNET_ID2'],
                ]
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'sc-monolith',
                'environment': [
                    {
                        'name': 'TASK_UID',
                        'value': str(task.uid)
                    },
                    {
                        'name': 'TASK_TYPE',
                        'value': task.type
                    },
                ],
                
            }]
        },
        taskDefinition=os.environ['FARGATE_MONOLITH_TASK_DEFINITION_NAME'],
    )

    return response

