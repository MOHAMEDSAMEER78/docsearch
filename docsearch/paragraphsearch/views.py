# paragraph_search/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paragraph, Word
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

@csrf_exempt
@permission_classes([AllowAny])
def add_paragraphs(request):
    try:
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)
            data = json.loads(request.body)
            paragraphs = data.get('paragraphs', [])

            for paragraph_text in paragraphs.split('\n\n'):
                words = [word.lower() for word in paragraph_text.split()]
                
                # Create or retrieve words from the database
                word_objects = [Word.objects.get_or_create(word=w)[0] for w in words]
                
                paragraph = Paragraph(content=paragraph_text, unique_id=hash(paragraph_text))
                paragraph.save()
                paragraph.words.set(word_objects)

            return JsonResponse({"message": "Paragraphs added successfully"}, status=201)
        
        return JsonResponse({"error": "Invalid request"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_paragraphs(request):
    search_word = request.GET.get('word', '').lower()

    if search_word:
        matching_paragraphs = Paragraph.objects.filter(words__word=search_word)[:10]
        result = []

        for paragraph in matching_paragraphs:
            words_in_paragraph = paragraph.words.values_list('word', flat=True)
            result.append({
                "id": paragraph.unique_id,
                "content": paragraph.content,
                "matched_word": search_word,
                "words_in_paragraph": list(words_in_paragraph),
            })

        return JsonResponse(result, safe=False)

    return JsonResponse({"error": "Missing or empty 'word' parameter"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_paragraphs(request):
    all_paragraphs = Paragraph.objects.all()
    result = []

    for paragraph in all_paragraphs:
        words_in_paragraph = paragraph.words.values_list('word', flat=True)
        result.append({
            "id": paragraph.unique_id,
            "content": paragraph.content,
            "words_in_paragraph": list(words_in_paragraph),
        })

    return JsonResponse(result, safe=False)
