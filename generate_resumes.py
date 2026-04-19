import os
import random

def create_txt_resume(filepath: str, name: str, skills: list, experience: str):
    content = f"RESUME\n\nName: {name}\n\nContact: {name.lower().replace(' ', '.')}@email.com | 555-0102\n\nSummary:\nHighly motivated professional with experience in {', '.join(skills[:2])}.\n\nSkills:\n- " + "\n- ".join(skills) + f"\n\nExperience:\n{experience}\n\nEducation:\nB.S. in Computer Science, University of Technology, 2018"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filepath}")

if __name__ == "__main__":
    resumes_dir = "resumes"
    os.makedirs(resumes_dir, exist_ok=True)

    candidates = [
        {"name": "Alice Johnson", "skills": ["Python", "Machine Learning", "Data Analysis", "SQL"], "exp": "Data Scientist at Tech Corp (2019-Present)\n- Built predictive models using Python.\n- Improved data processing pipeline."},
        {"name": "Bob Smith", "skills": ["Java", "Spring Boot", "Microservices", "Docker"], "exp": "Backend Developer at Web Solutions (2020-Present)\n- Developed RESTful APIs using Java.\n- Deployed microservices with Docker."},
        {"name": "Charlie Davis", "skills": ["JavaScript", "React", "Node.js", "CSS"], "exp": "Frontend Engineer at Creative Design (2018-2022)\n- Created responsive web apps with React.\n- Collaborated with UX designers."},
        {"name": "Diana Evans", "skills": ["Python", "Django", "PostgreSQL", "AWS"], "exp": "Full Stack Developer at StartUp Inc (2021-Present)\n- Maintained Django backend.\n- Managed AWS infrastructure."},
        {"name": "Evan Wright", "skills": ["C++", "System Architecture", "Linux", "Performance Tuning"], "exp": "Systems Engineer at Hardware Co (2015-Present)\n- Optimized low-level C++ code.\n- Designed scalable system architectures."}
    ]

    # Generate 5 text resumes
    for i, candidate in enumerate(candidates):
        filename = f"{resumes_dir}/resume_{candidate['name'].lower().replace(' ', '_')}.txt"
        create_txt_resume(filename, candidate['name'], candidate['skills'], candidate['exp'])
    
    # We create a dummy script to avoid requiring full PDF/DOCX generation libraries for dummy data creation.
    # We will rely on TXT files for the primary functionality testing, or users can add their own PDF/DOCX files.
    print(f"Generated {len(candidates)} resume files in the '{resumes_dir}' directory.")