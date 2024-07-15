
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
    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(endpoint, access_key, secret_key, secure=False)
        
    def helper_check_bucket(self, bucket_name):
        """Helper function to check if the target bucket exists. If not, create it."""
        bucket_exists = self.client.bucket_exists(bucket_name)
        if not bucket_exists:
            self.client.make_bucket(bucket_name)
            print(f'Bucket {bucket_name} created.')
        else:
            print(f'Bucket {bucket_name} already exists.')
        
    def upload(self, local_file_path, bucket_name, object_name):
        """Uploads a file to MinIO."""
        self.helper_check_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, local_file_path)
        
        print(
            f"{local_file_path} successfully uploaded to bucket {bucket_name} as {object_name}"
        )

    def download(self, bucket_name, object_name, local_file_path):
        """Downloads a file from MinIO."""
        self.helper_check_bucket(bucket_name)
        self.client.fget_object(bucket_name, object_name, local_file_path)
        
        print(
            f"{object_name} successfully downloaded from bucket {bucket_name} to {local_file_path}"
        )

    def list_files(self, bucket_name, prefix):
        """Lists files in a MinIO bucket with a specific prefix."""
        self.helper_check_bucket(bucket_name)
        objects = self.client.list_objects(bucket_name, prefix=prefix)
        return [obj.object_name for obj in objects]

    def delete(self, bucket_name, object_name):
        """Deletes a file from MinIO."""
        self.client.remove_object(bucket_name, object_name)
        
        print(f"{object_name} successfully deleted from bucket {bucket_name}")

        
        
#TODO: create class DuckDBStorage(StorageInterface) once to finish dagster worfklows for some transformations