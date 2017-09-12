import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

portfolio_bucket = s3.Bucket('portfolio.jasonsmith.rocks')
build_bucket = s3.Bucket('portfoliobuild.jasonsmith.rocks')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for filename in myzip.namelist():
        obj = myzip.open(filename)
        portfolio_bucket.upload_fileobj(obj, filename, ExtraArgs={
            'ContentType': mimetypes.guess_type(filename)[0]
        })
        portfolio_bucket.Object(filename).Acl().put(ACL='public-read')
