from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Note
from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def create_note(request):
    if request.method == 'POST':
        note_text = request.POST.get('content')
        max_views = int(request.POST.get('max_views', 1))
        expiration = int(request.POST.get('expiration', 1))        
        exp_date = timezone.now() + timedelta(days=expiration)

        note = Note.objects.create(
            note_text=note_text,
            exp_date=exp_date,
            max_views=max_views
        )
        note.save()
        link = request.build_absolute_uri(f"/note/{note.id}/")
        return render(
            request,
            "notes/note.html",
            {"link": link},
        )
    
    return render(request, 'notes/create_note.html')

@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def view_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    
    if note.is_expired():
        note.delete()
        return render(request, 'notes/view_note.html', {'note': note, 'expired_or_limit_reached': True})
    
    note.views += 1
    note.save()
    
    return render(request, 'notes/view_note.html', {'note': note, 'expired_or_limit_reached': False})
