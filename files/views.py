import os
from django.conf import settings  
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FileUpload, FileChunk
from .serializers import FileUploadSerializer, FileChunkSerializer

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)  

    @action(detail=False, methods=['POST'], url_path='upload-chunk')
    def upload_chunk(self, request):
        try:
            print("Received upload chunk request")
            print("POST data:", request.POST)
            print("Files:", request.FILES)

            chunk = request.FILES.get('chunk')
            if not chunk:
                return Response(
                    {'error': 'No chunk file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            chunk_index = request.POST.get('chunk_index')
            total_chunks = request.POST.get('total_chunks')
            filename = request.POST.get('filename')

            if not all([chunk_index, total_chunks, filename]):
                return Response(
                    {'error': 'Missing required parameters'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                chunk_index = int(chunk_index)
                total_chunks = int(total_chunks)
            except ValueError:
                return Response(
                    {'error': 'Invalid chunk_index or total_chunks'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_chunk, created = FileChunk.objects.update_or_create(
                filename=filename,
                chunk_index=chunk_index,
                defaults={'total_chunks': total_chunks, 'chunk': chunk}
            )

            chunks = FileChunk.objects.filter(filename=filename)
            
            print(f"Received chunk {chunk_index + 1} of {total_chunks} for file {filename}")
            print(f"Total chunks received: {chunks.count()}")

            if chunks.count() == total_chunks:
                try:
                    final_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
                    os.makedirs(os.path.dirname(final_path), exist_ok=True)

                    with open(final_path, 'wb') as final_file:
                        for i in range(total_chunks):
                            chunk = FileChunk.objects.get(filename=filename, chunk_index=i)
                            with open(chunk.chunk.path, 'rb') as chunk_file:
                                final_file.write(chunk_file.read())

                    file_size = os.path.getsize(final_path)
                    file_upload = FileUpload.objects.create(
                        name=filename,
                        size=file_size,
                        file=f'uploads/{filename}'
                    )

                    chunks.delete()

                    return Response(
                        {'status': 'File upload completed'}, 
                        status=status.HTTP_201_CREATED
                    )
                except Exception as e:
                    print(f"Error combining chunks: {str(e)}")
                    return Response(
                        {'error': f'Error combining chunks: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                {
                    'status': 'Chunk uploaded successfully',
                    'chunk_number': chunk_index + 1,
                    'total_chunks': total_chunks,
                    'chunks_received': chunks.count()
                }, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Error in upload_chunk: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )