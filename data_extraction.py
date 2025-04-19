import PyPDF2
import re
import os

class ResumeDetails():
    def extract_text_from_pdf(self,pdf_file_path):
        with open(pdf_file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            self.text = ""
            for page in reader.pages:
                self.text += page.extract_text() + "\n"
        return self.text

    def extract_resume_details(self,text):
        data = {}

            # Extract Name
        name_pattern = r"([A-Za-z]+ [A-Za-z]+)"
        name_match = re.search(name_pattern, text)
        data["name"] = name_match.group() if name_match else "Not found"

        # Extract Email ID
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        email_match = re.search(email_pattern, text)
        data["email"] = email_match.group() if email_match else "Not found"

        # Extract Skills
        skills_pattern = r"Technical\s+Skill\s*:\s*([A-Za-z0-9,/.\s-]+)"
        skills_match = re.search(skills_pattern, text)
        data["skills"] = skills_match.group(1).strip() if skills_match else "Not found"

        # Extract Education
        education_pattern = r"EDUCATION\s*\n(.*?)\nEXPERIENCE"
        education_match = re.search(education_pattern, text, re.DOTALL)
        data["education"] = education_match.group(1).strip() if education_match else "Not found"

        # Extract Total Experience Duration
        experience_pattern = r"(\d{1,2}\s\w+\s\d{4})\s[–-]\s(\d{1,2}\s\w+\s\d{4})"
        experience_matches = re.findall(experience_pattern, text)
        total_experience_months = sum([(int(end.split()[1]) - int(start.split()[1])) + (int(end.split()[2]) - int(start.split()[2])) * 12 for start, end in experience_matches])
        data["total_experience"] = f"{total_experience_months} months" if total_experience_months else "Not found"

        return data

    

    def get_resume_details(self,pdf_file_path):
        res = self.extract_text_from_pdf(pdf_file_path)
        return self.extract_resume_details(res)
        # print(self.extract_resume_details(res))

obj = ResumeDetails()
pdf_file_path = r"C:\Users\Tribhushan\Downloads\TR_Resume.pdf"
obj.get_resume_details(pdf_file_path)
