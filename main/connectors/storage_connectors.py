
class StorageInterface:
    def upload(self, source, destination):
        return NotImplementedError('Method should be overridden by subclass')
    
    def download(self, source, destination):
        return NotImplementedError('Method should be overridden by subclass')
    
    def list_files(self, directory):
        return NotImplementedError('Method should be overridden by subclass')
    
    def delete(self, file_path):
        return NotImplementedError('Method should be overridden by subclass')    
  
  
from minio import Minio

class MinIOStorage(StorageInterface):
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.client = Minio(endpoint, access_key, secret_key, secure=False)
        self.bucket_name = bucket_name
        self.helper_check_bucket(bucket_name)
        
    def helper_check_bucket(self, bucket_name):
        """Helper function to check if the target bucket exists. If not, create it."""
        bucket_exists = self.client.bucket_exists(bucket_name)
        if not bucket_exists:
            self.client.make_bucket(bucket_name)
            print(f'Bucket {bucket_name} created.')
        else:
            print(f'Bucket {bucket_name} already exists.')
        
    
    def upload(self, local_file_path, object_name):
        """Uploads a file to MinIO."""
        self.client.fput_object(self.bucket_name, object_name, local_file_path)
        print(f"{local_file_path} successfully uploaded to bucket {self.bucket_name} as {object_name}")

    def download(self, object_name, local_file_path):
        """Downloads a file from MinIO."""
        self.client.fget_object(self.bucket_name, object_name, local_file_path)
        print(f"{object_name} successfully downloaded from bucket {self.bucket_name} to {local_file_path}")

    def list_files(self, prefix):
        """Lists files in a MinIO bucket with a specific prefix."""
        objects = self.client.list_objects(self.bucket_name, prefix=prefix)
        return [obj.object_name for obj in objects]

    def delete(self, object_name):
        """Deletes a file from MinIO."""
        self.client.remove_object(self.bucket_name, object_name)
        print(f"{object_name} successfully deleted from bucket {self.bucket_name}")
        
        
#TODO: create class DuckDBStorage(StorageInterface) once to finish dagster worfklows for some transformations