from django.db import models

class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name

class FileChunk(models.Model):
    file = models.ForeignKey(FileUpload, related_name='chunks', on_delete=models.CASCADE, null=True)
    filename = models.CharField(max_length=255)
    chunk_index = models.IntegerField()
    total_chunks = models.IntegerField()
    chunk = models.FileField(upload_to='chunks/')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['filename', 'chunk_index']

    def __str__(self):
        return f"{self.filename} - Chunk {self.chunk_index + 1}/{self.total_chunks}"