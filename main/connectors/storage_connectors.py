
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
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
            print('Create bucket', bucket_name)
        else:
            print('Bucket', bucket_name, 'found')
        
    def upload(self, source, bucket_name, destination):
        self.helper_check_bucket(self, bucket_name)
        self.client.fput_object(bucket_name, destination, source)
        
        print(
            source, "successfully uploaded as object", 
            destination, "to bucket", bucket_name,
        )

    def download(self, source, bucket_name, destination):
        self.helper_check_bucket(self, bucket_name)
        self.client.fget_object(bucket_name, destination, source)
        
        print(
            source, "successfully downloaded as object", 
            destination, "to bucket", bucket_name,
        )
        
        
#TODO: create class DuckDBStorage(StorageInterface) once to finish dagster worfklows for some transformations