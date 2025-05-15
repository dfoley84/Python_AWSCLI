import boto3
import os
import time
from botocore.exceptions import WaiterError

class ChangeEngine:
    """
    A class to modify the engine version of an AWS RDS database instance.

    This class handles changing the engine version of an Amazon RDS database
    instance and can optionally wait for the modification to complete.

    Attributes:
        InstanceName (str): The identifier of the RDS instance to modify.
        EngineVersion (str): The target engine version to change to.
        awsRegion (str): The AWS region where the RDS instance is located.
        rds: Boto3 RDS client instance.
    """
    
    def __init__(self, InstanceName, EngineVersion, awsRegion):
        """
        Initialize the ChangeEngine class with instance details.

        Args:
            InstanceName (str): The identifier of the RDS instance.
            EngineVersion (str): The target engine version.
            awsRegion (str): The AWS region of the RDS instance.
        """
        self.InstanceName = InstanceName
        self.EngineVersion = EngineVersion
        self.awsRegion = awsRegion
        self.rds = boto3.client('rds', region_name=self.awsRegion)
    
    def ChangeEngine(self, apply_immediately=False, wait=False):
        """
        Change the engine version of the specified RDS instance.

        Args:
            apply_immediately (bool): Whether to apply changes immediately or during
                                      the next maintenance window. Default is False.
            wait (bool): Whether to wait for the modification to complete. Default is False.

        Returns:
            dict: Response from the modify_db_instance API call.

        Raises:
            WaiterError: If the waiter times out waiting for the instance to become available.
        """
        response = self.rds.modify_db_instance(
             DBInstanceIdentifier=self.InstanceName, 
             EngineVersion=self.EngineVersion,
             ApplyImmediately=apply_immediately
        )
        
        print(f"Requested instance engine version change for {self.InstanceName} to {self.EngineVersion}")
        
        if wait:
            print(f"Waiting for the instance to become available...")
            try:
                waiter = self.rds.get_waiter('db_instance_available')
                waiter.wait(
                    DBInstanceIdentifier=self.InstanceName,
                    WaiterConfig={
                        'Delay': 60, 
                        'MaxAttempts': 30
                    }
                )
                print(f"Instance {self.InstanceName} is now available with Engine Version {self.EngineVersion}")
            except WaiterError as e:
                print(f"Waiter timeout or error: {str(e)}")
                raise
                
        return response