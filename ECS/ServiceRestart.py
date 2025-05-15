import boto3
import os
import time
from botocore.exceptions import WaiterError

class ServiceRestart:
    def __init__(self, ClusterName, Servicearn, awsRegion):
        """
        Initializes the ChangeType class with the ECS cluster name, service ARN, and AWS region.

        Args:
            ClusterName (str): The name of the ECS cluster.
            Servicearn (str): The ARN of the ECS service to restart.
            awsRegion (str): The AWS region where the ECS service is located.
        """
        self.ClusterName = ClusterName
        self.Servicearn = Servicearn
        self.awsRegion = awsRegion
        self.ecs_client = boto3.client('ecs', region_name=self.awsRegion)

    def RestartService(self):
        """
        Restarts the ECS service by forcing a new deployment and waits for the service to become stable.

        This method uses the ECS `update_service` API to force a new deployment of the service and 
        then waits for the service to reach a stable state using the `services_stable` waiter.

        Raises:
            WaiterError: If the waiter fails to confirm that the service is stable.
        """
        response = self.ecs_client.update_service(
            cluster=self.ClusterName,
            service=self.Servicearn,
            forceNewDeployment=True
        )
        print(f"Requested service restart for {self.Servicearn}")
        #Wait for the service to be stable
        try:
            waiter = self.ecs_client.get_waiter('services_stable')
            waiter.wait(
                cluster=self.ClusterName,
                services=[self.Servicearn],
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': 20
                }
            )
            print(f"Service {self.Servicearn} is stable now.")
        except WaiterError as e:
            print(f"Waiter failed: {e}")
        