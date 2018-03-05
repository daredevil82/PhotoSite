from __future__ import absolute_import

import argparse
from botocore.exceptions import ClientError, BotoCoreError
import logging
import os
import sys


try:
    import boto3
    import botocore
except ImportError as e:
    print("Error importing boto -- resolve by installing Boto3 python package")
    sys.exit(1)


class S3Upload:
    def __init__(self):
        self.s3_bucket = 'jasonjohns-photosite'
        self.client_id = None
        self.file_name = None

    def _validate_path(self, file_path):
        """
        Check that the provided file or file path is valid
        :param file_path:
        :return: True or False based on return of os.path.isfile
        """
        if os.path.isfile(file_path):
            return True
        else:
            print('File path [{}] is not a valid file.  Exiting'.format(file_path))
            return False

    def upload_to_s3(self, file_path, client_id):
        """
        Upload a provided file path to S3.  If a successful upload occurs, a HTTP POST request is executed.
        :param file_path:  Path to file to be uploaded
        :param client_id: Client ID for which this file is associated with
        :return: None
        """
        self.client_id = client_id

        if self._validate_path(file_path):
            try:
                s3_client = boto3.client('s3')
                with open(file_path, 'rb') as f:
                    self.file_name = f.name
                    s3_client.upload_fileobj(f, self.s3_bucket, 'archives/{}'.format(f.name), ExtraArgs = {'ACL': 'public-read'})
                    print('Valid file [{}] uploaded to S3 bucket [{}]'.format(self.file_name, self.s3_bucket))
                    self.post_api()
            except (BotoCoreError, ClientError, EnvironmentError) as e:
                print("Error uploading file to S3: [{}]".format(e))
                sys.exit(2)

        else:
            sys.exit(2)

    def post_api(self):
        """
        POST a request to the API to process the file uploaded.
        :return: None
        """
        print('Posting to API using key [{}] and client id [{}]'.format(self.file_name, self.client_id))
        pass


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help = 'Path to file to be uploaded', type = str)
    parser.add_argument('client_id', help = 'Client ID for file mapping', type = int)
    args = parser.parse_args()

    if args:
        upload = S3Upload()
        upload.upload_to_s3(args.file_path, args.client_id)

if __name__ == '__main__':
    main(sys.argv[1:])
