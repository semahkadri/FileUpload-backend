from rest_framework import serializers
from .models import FileUpload, FileChunk

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'name', 'size', 'upload_date']

class FileChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileChunk
        fields = ['filename', 'chunk_index', 'total_chunks', 'chunk']