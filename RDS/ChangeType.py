import boto3
import os
import time
from botocore.exceptions import WaiterError

class ChangeType:
    """
    A class to modify AWS RDS instance types.
    
    This class handles changing the instance type of an Amazon RDS database
    instance and can optionally wait for the modification to complete.
    
    Attributes:
        InstanceName (str): The identifier of the RDS instance to modify.
        InstanceType (str): The target instance type to change to.
        awsRegion (str): The AWS region where the RDS instance is located.
        rds: Boto3 RDS client instance.
    """
    
    def __init__(self, InstanceName, InstanceType, awsRegion):
        """
        Initialize the ChangeType class with instance details.
        
        Args:
            InstanceName (str): The identifier of the RDS instance.
            InstanceType (str): The target instance type.
            awsRegion (str): The AWS region of the RDS instance.
        """
        self.InstanceName = InstanceName
        self.InstanceType = InstanceType
        self.awsRegion = awsRegion
        self.rds = boto3.client('rds', region_name=self.awsRegion)
    
    def ChangeType(self, apply_immediately=False, wait=False, timeout=3600):
        """
        Change the instance type of the specified RDS instance.
        Args:
            apply_immediately (bool): Whether to apply changes immediately or during
                                    the next maintenance window. Default is False.
            wait (bool): Whether to wait for the modification to complete. Default is False.
            timeout (int): Maximum time in seconds to wait for modification. Default is 3600.
            
        Returns:
            dict: Response from the modify_db_instance API call.
            
        Raises:
            WaiterError: If the waiter times out waiting for the instance to become available.
        """
        response = self.rds.modify_db_instance(
             DBInstanceIdentifier=self.InstanceName, 
             DBInstanceClass=self.InstanceType,
             ApplyImmediately=apply_immediately
        )
        
        print(f"Requested instance type change for {self.InstanceName} to {self.InstanceType}")
        
        if wait:
            print(f"Waiting for the instance to become available (timeout: {timeout}s)...")
            try:
                waiter = self.rds.get_waiter('db_instance_available')
                waiter.wait(
                    DBInstanceIdentifier=self.InstanceName,
                    WaiterConfig={
                        'Delay': 60, 
                        'MaxAttempts': timeout // 30  
                    }
                )
                print(f"Instance {self.InstanceName} is now available with type {self.InstanceType}")
            except WaiterError as e:
                print(f"Waiter timeout or error: {str(e)}")
                raise
                
        return response