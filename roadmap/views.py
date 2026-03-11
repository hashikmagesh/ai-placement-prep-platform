from django.shortcuts import render

# Create your views here.
import json
import os
from django.shortcuts import render, redirect
from django.conf import settings

def load_roadmap_data():
    """Load roadmap data from JSON file"""
    json_path = os.path.join(settings.BASE_DIR, 'roadmap', 'data.json')
    with open(json_path, 'r') as f:
        return json.load(f)

def select_page(request):
    """Homepage - Select domain and company"""
    if request.method == 'POST':
        domain = request.POST.get('domain')
        company = request.POST.get('company')
        
        if domain and company:
            # Store selections in session
            request.session['domain'] = domain
            request.session['company'] = company
            request.session['completed_topics'] = []
            return redirect('roadmap')
    
    # Load data for dropdowns
    data = load_roadmap_data()
    domains = list(data.keys())
    
    # Get all unique companies
    companies = set()
    for domain_data in data.values():
        companies.update(domain_data.keys())
    companies = sorted(list(companies))
    
    context = {
        'domains': domains,
        'companies': companies
    }
    return render(request, 'roadmap/select.html', context)

def roadmap_page(request):
    """Roadmap page - Display topics for selected domain/company"""
    domain = request.session.get('domain')
    company = request.session.get('company')
    
    if not domain or not company:
        return redirect('select')
    
    # Handle topic completion
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        completed = request.session.get('completed_topics', [])
        if topic_id and int(topic_id) not in completed:
            completed.append(int(topic_id))
            request.session['completed_topics'] = completed
            request.session.modified = True
        return redirect('roadmap')
    
    # Load roadmap data
    data = load_roadmap_data()
    topics = data.get(domain, {}).get(company, [])
    
    # Filter out completed topics
    completed = request.session.get('completed_topics', [])
    remaining_topics = [t for t in topics if t['id'] not in completed]
    
    # Calculate progress
    total_topics = len(topics)
    completed_count = len(completed)
    progress_percentage = (completed_count / total_topics * 100) if total_topics > 0 else 0
    
    context = {
        'domain': domain,
        'company': company,
        'topics': remaining_topics,
        'completed_count': completed_count,
        'total_topics': total_topics,
        'progress_percentage': round(progress_percentage, 1)
    }
    return render(request, 'roadmap/roadmap.html', context)

def reset_progress(request):
    """Reset progress and go back to selection"""
    if 'completed_topics' in request.session:
        del request.session['completed_topics']
    if 'domain' in request.session:
        del request.session['domain']
    if 'company' in request.session:
        del request.session['company']
    return redirect('select')