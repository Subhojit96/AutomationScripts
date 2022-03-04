from tracemalloc import Snapshot
from urllib import response
import json
import boto3
from botocore.exceptions import ClientError

def db_snapshot(event,context):
    db_client = boto3.client('rds', region_name ='us-east-2')
    dbcluster = db_client.describe_db_clusters(
    MaxRecords=100,
    IncludeShared= False
    )
    db_identifiers=[]
    for identifiers in range (len(dbcluster['DBClusters'])):
        db_identifiers.append(dbcluster['DBClusters'][identifiers]['DBClusterIdentifier'])
    #print (db_identifiers)
    db_automated_snapshots=[]
    db_automated_snapshots_status = []
    db_automated_snapshots_arn = []
    for snapshots in range (len(db_identifiers)):
        dbsnapshot = db_client.describe_db_cluster_snapshots(
            DBClusterIdentifier = db_identifiers[snapshots],
            SnapshotType='automated',
            IncludeShared=False,
            IncludePublic=False,
        )
        db_automated_snapshots.append(dbsnapshot['DBClusterSnapshots'][snapshots]['DBClusterSnapshotIdentifier'])
        db_automated_snapshots_status.append(dbsnapshot['DBClusterSnapshots'][snapshots]['Status'])
        db_automated_snapshots_arn.append(dbsnapshot['DBClusterSnapshots'][snapshots]['DBClusterSnapshotArn'])
        print (db_automated_snapshots,db_automated_snapshots_status)
    #S3Bucket='static-content-cognito'
    #S3Prefix='dbsnapshots'
    for status in range (len(db_automated_snapshots_status)):
        if (db_automated_snapshots_status[status]!='available'):
            return{
                'body':json.dumps('Status of Snapshot '+db_automated_snapshots[status]+ ' is: '+db_automated_snapshots_status[status])
            }
        elif (db_automated_snapshots_status[status]=='available'):
            exp_tasks = db_client.copy_db_cluster_snapshot(
                SourceDBClusterSnapshotIdentifier= db_automated_snapshots_arn[status],
                TargetDBClusterSnapshotIdentifier='rds-primaryregionauroradb-2022-01-23-03-19',
                KmsKeyId='arn:aws:kms:us-east-2:048420978968:key/mrk-a7053ecad1ad46d78f4fc174daa105df',
                CopyTags=True,
                SourceRegion='us-east-2'
            )
            return{
                'body':json.dumps('Task to export snapshot in S3 bucket started.')
            }
        else:
            S3URL= S3Bucket
            return{
                'body':json.dumps('Either a Export Task is In-Progress or Snapshot name may already exists in S3 Bucket: '+S3URL)
            }