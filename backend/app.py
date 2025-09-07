from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# Set up CORS to allow requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# Load sample data with proper error handling
def load_data():
    # Use absolute path for reliability
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(current_dir, 'internship.json')
    
    print("\n===== DATA LOADING DEBUG INFO =====")
    print("🔍 DEBUG: Current working directory:", os.getcwd())
    print("🔍 DEBUG: Script directory:", current_dir)
    print(f"🔍 DEBUG: Using absolute path: {abs_path}")
    print(f"🔍 DEBUG: File exists: {os.path.exists(abs_path)}")
    
    # Print all files in current directory
    print("🔍 DEBUG: Files in directory:")
    for file in os.listdir(current_dir):
        print(f"  - {file}")
    
    # First, try with the absolute path
    try:
        if os.path.exists(abs_path):
            with open(abs_path, 'r', encoding='utf-8') as f:
                print("🔍 DEBUG: Reading file content...")
                file_content = f.read()
                print(f"🔍 DEBUG: File size: {len(file_content)} bytes")
                print("🔍 DEBUG: First 100 chars:", file_content[:100])
                print("🔍 DEBUG: Parsing JSON...")
                
                # Fix any potential JSON issues - remove incomplete entries
                try:
                    internships = json.loads(file_content)
                    # Filter out entries without essential fields
                    internships = [item for item in internships if 'id' in item and 'title' in item and 'company' in item]
                    print(f"✅ Successfully loaded {len(internships)} internships from absolute path")
                    if len(internships) > 0:
                        print(f"🔍 DEBUG: First internship title: {internships[0].get('title', 'Unknown')}")
                        print(f"🔍 DEBUG: Last internship with id: {internships[-1].get('id', 'Unknown')}")
                    return internships
                except json.JSONDecodeError as json_error:
                    print(f"❌ JSON parsing error: {str(json_error)}")
                    raise
        else:
            print("❌ File does not exist at absolute path")
    except Exception as e:
        print(f"❌ Failed to load from absolute path: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # If direct approach failed, try multiple paths as fallback
    possible_paths = [
        'internship.json',
        './internship.json',
        '../internship.json',
        'data/internship.json',
        '../data/internship.json'
    ]
    
    for path in possible_paths:
        print(f"🔍 DEBUG: Checking fallback path: {path}, exists: {os.path.exists(path)}")
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    internships = json.load(f)
                print(f"✅ Successfully loaded {len(internships)} internships from {path}")
                return internships
        except Exception as e:
            print(f"❌ Failed to load from {path}: {e}")
            continue
    
    # If no file found, return sample data
    print("⚠ No JSON file found, using fallback sample data")
    return get_sample_data()

def get_sample_data():
    """Fallback sample data if JSON file is not found"""
    return [
        {
            "id": 1,
            "title": "Software Development Intern",
            "company": "Tata Consultancy Services",
            "company_type": "Private",
            "description": "Develop web applications using modern frameworks",
            "required_education": "graduate",
            "required_skills": ["computer", "english", "programming"],
            "location_type": "Hybrid",
            "location_state": "maharashtra",
            "location_city": "mumbai",
            "category": "technology",
            "sector": "Information Technology",
            "stipend": 25000,
            "duration": "6 months"
        }
    ]

# Enhanced AI Recommendation Algorithm
def calculate_match_score(candidate, internship):
    score = 0
    match_details = []
    
    # Education Match (35% weight)
    education_levels = {
        '10th': 1, '12th': 2, 'diploma': 3, 'graduate': 4, 'postgraduate': 5
    }
    
    candidate_edu = education_levels.get(candidate.get('education', '10th'), 1)
    required_edu = education_levels.get(internship.get('required_education', '10th'), 1)
    
    if candidate_edu >= required_edu:
        education_score = 1.0
        match_details.append(f"Education requirement met ({candidate.get('education')})")
    elif candidate_edu == required_edu - 1:
        education_score = 0.8
        match_details.append("Education close match")
    else:
        education_score = 0.4
        match_details.append("Education below requirement")
    
    score += education_score * 0.35
    
    # Skills Match (30% weight)
    candidate_skills = set([skill.lower().strip() for skill in candidate.get('skills', [])])
    required_skills = set([skill.lower().strip() for skill in internship.get('required_skills', [])])
    
    if len(required_skills) > 0:
        matched_skills = candidate_skills.intersection(required_skills)
        skill_match = len(matched_skills) / len(required_skills)
        if len(matched_skills) > 0:
            match_details.append(f"Skills match: {', '.join(list(matched_skills)[:2])}")
        else:
            skill_match = 0.3
    else:
        skill_match = 0.8
        match_details.append("No specific skills required")
    
    score += skill_match * 0.30
    
    # Location Match (20% weight)
    candidate_location = candidate.get('location_state', '').lower()
    internship_location = internship.get('location_state', '').lower()
    
    if internship.get('location_type') == 'Remote':
        location_score = 1.0
        match_details.append("Remote work available")
    elif candidate_location == 'any' or candidate_location == internship_location:
        location_score = 1.0
        match_details.append("Perfect location match")
    else:
        location_score = 0.6
        match_details.append("Different state location")
    
    score += location_score * 0.20
    
    # Interest/Category Match (15% weight)
    candidate_interests = set([interest.lower().strip() for interest in candidate.get('interests', [])])
    internship_category = internship.get('category', '').lower().strip()
    
    interest_score = 0.5
    for interest in candidate_interests:
        if interest in internship_category or internship_category in interest:
            interest_score = 1.0
            match_details.append(f"Interest match: {interest}")
            break
    
    score += interest_score * 0.15
    
    return min(score, 1.0), match_details

# API endpoint for recommendations
@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        print("\n===== RECOMMENDATION REQUEST =====")
        print("Request Headers:", request.headers)
        print("Request Content-Type:", request.content_type)
        
        try:
            if request.is_json:
                candidate_data = request.json
                print("Request JSON Data:", candidate_data)
            else:
                print("Request is not JSON format. Content:", request.data)
                return jsonify({'error': 'Request must be JSON format'}), 400
        except Exception as e:
            print("Error parsing request data:", str(e))
            return jsonify({'error': 'Invalid request data', 'details': str(e)}), 400
        
        if not candidate_data:
            print("No candidate data provided")
            return jsonify({'error': 'No candidate data provided'}), 400
            

        # Load internships data
        print("Loading internship data...")
        internships = load_data()
        print(f"Loaded {len(internships)} internships")

        # Fix missing fields in candidate data
        if 'skills' not in candidate_data or not candidate_data['skills']:
            candidate_data['skills'] = ['english', 'computer']
            print("Added default skills")

        if 'interests' not in candidate_data or not candidate_data['interests']:
            candidate_data['interests'] = ['technology']
            print("Added default interests")

        if 'education' not in candidate_data:
            candidate_data['education'] = 'graduate'
            print("Added default education level")

        # --- FILTERS ---
        filters = candidate_data.get('filters', {})
        duration_filters = filters.get('duration', [])  # e.g. ['3 months', '6 months']
        stipend_filters = filters.get('stipend', [])    # e.g. ['0-5000', '5000-15000', '15000+']

        def stipend_in_range(stipend, ranges):
            for r in ranges:
                if r == '0-5000' and stipend <= 5000:
                    return True
                if r == '5000-15000' and 5000 < stipend <= 15000:
                    return True
                if r == '15000+' and stipend > 15000:
                    return True
            return False

        filtered_internships = []
        for internship in internships:
            # Duration filter
            if duration_filters:
                if not any(d.lower() in internship.get('duration', '').lower() for d in duration_filters):
                    continue
            # Stipend filter
            if stipend_filters:
                if not stipend_in_range(internship.get('stipend', 0), stipend_filters):
                    continue
            filtered_internships.append(internship)

        print(f"Filtered internships count: {len(filtered_internships)}")

        # Calculate scores for all internships
        print("Calculating scores...")
        recommendations = []
        for internship in filtered_internships:
            # Skip entries without required fields
            if not all(key in internship for key in ['id', 'title', 'company']):
                continue

            try:
                score, match_details = calculate_match_score(candidate_data, internship)
                if score > 0.3:
                    recommendations.append({
                        'internship': internship,
                        'score': round(score * 100),
                        'match_percentage': f"{round(score * 100)}%",
                        'match_details': match_details[:3]
                    })
            except Exception as calc_err:
                print(f"Error calculating score for internship {internship.get('id', 'unknown')}: {str(calc_err)}")
                continue

        # Sort by score and return top 5
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        print(f"Found {len(recommendations)} matching recommendations")

        # If no recommendations were found, return default ones
        if not recommendations:
            print("No recommendations found, returning fallbacks")
            fallbacks = [internship for internship in filtered_internships 
                        if all(key in internship for key in ['id', 'title', 'company'])][:5]
            recommendations = [{
                'internship': internship,
                'score': 70,
                'match_percentage': "70%",
                'match_details': ["Default recommendation"]
            } for internship in fallbacks]

        response = {
            'success': True,
            'total_found': len(recommendations),
            'recommendations': recommendations[:5]
        }
        print(f"Returning {len(response['recommendations'])} recommendations")
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        print("\n===== HEALTH CHECK REQUEST =====")
        internships = load_data()
        response = {
            'status': 'healthy', 
            'message': 'Backend running!',
            'data_count': len(internships),
            'working_directory': os.getcwd(),
            'data_sample': []
        }
        
        # Add sample data for debugging
        if internships and len(internships) > 0:
            # Add first and last internship as samples
            response['data_sample'] = [
                {
                    'id': internships[0].get('id', 'Unknown'),
                    'title': internships[0].get('title', 'Unknown'),
                    'company': internships[0].get('company', 'Unknown')
                },
                {
                    'id': internships[-1].get('id', 'Unknown'),
                    'title': internships[-1].get('title', 'Unknown'),
                    'company': internships[-1].get('company', 'Unknown')
                }
            ]
        
        return jsonify(response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Test endpoint to directly read the JSON file
@app.route('/api/test-json', methods=['GET'])
def test_json():
    try:
        filepath = os.path.join(os.getcwd(), 'internship.json')
        print(f"Reading file from: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            print(f"File size: {len(file_content)} bytes")
            data = json.loads(file_content)
        
        # Create a simplified response with essential information
        first_item = {
            'id': data[0].get('id', None),
            'title': data[0].get('title', None),
            'company': data[0].get('company', None),
        } if data else None
        
        last_item = {
            'id': data[-1].get('id', None),
            'title': data[-1].get('title', None),
            'company': data[-1].get('company', None),
        } if data else None
        
        return jsonify({
            'success': True,
            'count': len(data),
            'first_item': first_item,
            'last_item': last_item,
            'file_path': filepath,
            'file_exists': os.path.exists(filepath),
            'file_size_bytes': os.path.getsize(filepath) if os.path.exists(filepath) else 0,
            'working_directory': os.getcwd(),
            'data_loaded': True
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'working_directory': os.getcwd(),
            'file_path': filepath,
            'file_exists': os.path.exists(filepath) if 'filepath' in locals() else 'Unknown'
        }), 500

# Additional debug endpoint to list all JSON files
@app.route('/api/debug/files', methods=['GET'])
def list_json_files():
    try:
        current_dir = os.getcwd()
        result = {
            'working_directory': current_dir,
            'json_files': [],
            'directory_contents': []
        }
        
        # List all files in current directory
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                result['directory_contents'].append(f"DIR: {item}")
            else:
                result['directory_contents'].append(f"FILE: {item} ({os.path.getsize(item_path)} bytes)")
                if item.endswith('.json'):
                    result['json_files'].append({
                        'name': item,
                        'path': item_path,
                        'size': os.path.getsize(item_path)
                    })
        
        # Check for internship.json specifically
        internship_json = os.path.join(current_dir, 'internship.json')
        result['internship_json_exists'] = os.path.exists(internship_json)
        if result['internship_json_exists']:
            result['internship_json_size'] = os.path.getsize(internship_json)
            
            # Try to read first few bytes
            with open(internship_json, 'r', encoding='utf-8') as f:
                result['internship_json_preview'] = f.read(200)
                
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Serve React app's static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join('../dist', path)):
        return send_from_directory('../dist', path)
    else:
        return send_from_directory('../dist', 'index.html')

# Legacy routes for HTML files (fallback)
@app.route('/style.css')
def serve_css():
    return send_from_directory('../', 'styles.css')

@app.route('/script.js')  
def serve_js():
    return send_from_directory('../', 'script.js')

if __name__ == '__main__':
    print("🚀 Starting InternFind AI Recommendation Engine...")
    print("📁 Looking for internship.json in backend directory")
    print("🌐 Frontend served from: ../dist/")
    print("🔗 Access at: http://localhost:5000")
    
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')