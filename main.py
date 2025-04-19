from flask import Flask,jsonify,request,render_template,send_from_directory, send_file
from app.database import get_db
from data_extraction import ResumeDetails
from bson import ObjectId
import project_config
import os


app = Flask(__name__, static_folder='static', template_folder='templates')

resObj = ResumeDetails()
collection=get_db()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    # return jsonify({"Message":"Successful"})
    return render_template('resume_dashboard.html')

@app.route('/<page>')
def serve_page(page):
    return send_from_directory('templates', page)


@app.route('/upload-resume',methods = ['POST'])
def upload_resume():
    file = request.files['file']
    file_name = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    # file_path = f'uploads/{file_name}'
    # file.save(file_path)
    result = resObj.get_resume_details(file_path)
    response =  collection.find_one({"name":result["name"]})
    if not response:
        collection.insert_one({"file_name": file_name,"name":result["name"],"email":result["email"],"skills":result["skills"],"total_experience":result["total_experience"],"education":result["education"]})
        return jsonify({"status": 'Success', "message" :  "Resume stored Successfully"})

    else:
        return jsonify({"status": 'Error', "message" :  "Resume already existy"})
    
        


@app.route('/get-candidates', methods=['GET'])
def get_candidates():
    response = collection.find()

    candidates = []
    for candidate in response:
        candidate['_id'] = str(candidate['_id'])  # Convert ObjectId to string
        candidates.append(candidate)

    if not candidates:
        return jsonify({"status": 'Error', "message": "Candidates doesn't exist"})
    else:
        return jsonify({
            "status": 'Successful',
            "message": candidates
        })




@app.route('/candidate/<candidate_id>', methods=['GET'])
def get_candidate_id(candidate_id):
    try:
        # Convert candidate_id to ObjectId
        obj_id = ObjectId(candidate_id)
        result = collection.find_one({"_id": obj_id})

        if not result:
            return jsonify({"status": 'Failed', "message": "Candidate ID Not Found"})
        
        # Convert MongoDB document to JSON-friendly format
        result['_id'] = str(result['_id'])
        return jsonify({"status": 'Success', "message": "Candidate found successfully", "data": result})

    except Exception as e:
        return jsonify({"status": 'Error', "message": str(e)})


    
@app.route('/remove-candidate/<candidate_id>', methods=['DELETE'])
def remove_candidate(candidate_id):
    try:
        obj_id = ObjectId(candidate_id)
        candidate = collection.find_one({"_id": obj_id})

        if not candidate:
            return jsonify({"status": "Failed", "message": "Candidate not found"})

        file_name = candidate.get("file_name")
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Remove candidate from database
        collection.delete_one({"_id": obj_id})

        # Remove file if it exists
        if file_name and os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"status": "Success", "message": "Candidate and resume removed successfully"})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8084,debug=True)