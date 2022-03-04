import boto3
from botocore.exceptions import ClientError
import json

def lambda_handler(event, context):
    client = boto3.client('ses',region_name='us-east-1')
    body_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <p>
            Primary region in AWS is down. Please deploy infrastructure in Secondary Region.
        </p>
        <h3>Please select your action</h3>
        <a href="https://cloudbeez.auth.us-east-1.amazoncognito.com/login?client_id=1irjf0fhtr3lfm96imp56j0brq&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://3ury8w8tp6.execute-api.us-east-1.amazonaws.com/Test_Stage">
            <input type="submit" value="Approve"/>
        </a>
        <a href="https://skribbl.io/">
            <input type="submit" value="Deny"/>
        </a>
    </body>
    </html>
    """
    try:
        response = client.send_email(
        Source='subhojit1025@gmail.com', #email address
        Destination={
            'ToAddresses': ['subdas@deloitte.com',
            #'string',
            ],
            'CcAddresses': ['subhojit96@outlook.com',
            #'string',
            ],
        },
        Message={
            'Subject': {
                'Data': 'AWS Primary Region is down',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                'Data': body_html,
                }
            }
        },
        ReplyToAddresses=[
        'subhojit1025@gmail.com',
        #'string',
        ],
        ReturnPath='subhojit1025@gmail.com',
        SourceArn='arn:aws:ses:us-east-1:048420978968:identity/subhojit1025@gmail.com',
        ReturnPathArn='arn:aws:ses:us-east-1:048420978968:identity/subhojit1025@gmail.com',
        Tags=[
            {
                'Name': 'Name', 
                'Value': 'Failover'
            },
        ],
        ConfigurationSetName='Send_Ses_email'
        #'string'
    )
    except ClientError as e:
        print(e)

    return {
        'statusCode': 200,
    }