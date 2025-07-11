import os
import time
import pandas as pd
from django.core.management.base import BaseCommand
from chatbot.models import CompanyInfo
import google.generativeai as genai

# Load API Client
GENAI_API_KEY = "AIzaSyCpjHqW6t4oSg1Ge_zYcag854fqGVYwdXA"
genai.configure(api_key=GENAI_API_KEY)

def extract_company_names(excel_path):
    """Extracts company names from the Excel file."""
    df = pd.read_excel(excel_path)
    company_names = df.iloc[:, 1].dropna().unique().tolist()  # Assuming company names are in the second column
    return company_names

def fetch_company_details(company_name):
    """Fetches company details using Gemini 1.5 Pro Latest, with Flash as fallback."""
    prompt = f"""
    Provide detailed information for the company: {company_name}.
    - Official Website
    - Short Company Description
    - Official Contact Email (if available)
    - Industry, Headquarters, Founded Year (if applicable)
    Respond in a structured format.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        time.sleep(5)
        return parse_response(response.text)
    except Exception as e:
        print(f"Gemini Pro failed, switching to Flash: {e}")
        time.sleep(5)  # Increase delay before retrying
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            return parse_response(response.text)
        except Exception as e:
            print(f"Gemini Flash also failed: {e}")
            return {}

def parse_response(response_text):
    """Parses the AI response into structured data."""
    details = {
        "website": "",
        "description": "",
        "contact_email": "",
        "industry": "",
        "headquarters": "",
        "founded_year": ""
    }
    
    lines = response_text.split("\n")
    for line in lines:
        if "Website:" in line:
            details["website"] = line.split("Website:")[1].strip()
        elif "Description:" in line:
            details["description"] = line.split("Description:")[1].strip()
        elif "Email:" in line:
            details["contact_email"] = line.split("Email:")[1].strip()
        elif "Industry:" in line:
            details["industry"] = line.split("Industry:")[1].strip()
        elif "Headquarters:" in line:
            details["headquarters"] = line.split("Headquarters:")[1].strip()
        elif "Founded:" in line:
            details["founded_year"] = line.split("Founded:")[1].strip()
    
    return details

class Command(BaseCommand):
    help = "Extracts company names from Excel and stores details in Django model"

    def handle(self, *args, **kwargs):
        excel_path = r"C:\Users\darkc\Downloads\Comapny-name-list-1.xlsx"
        companies = extract_company_names(excel_path)

        for company in companies:
            if not CompanyInfo.objects.filter(company_name=company).exists():
                details = fetch_company_details(company)
                CompanyInfo.objects.create(
                    company_name=company,
                    website=details.get("website", ""),
                    description=details.get("description", ""),
                    contact_email=details.get("contact_email", ""),
                    additional_info=f"Industry: {details.get('industry', '')}, Headquarters: {details.get('headquarters', '')}, Founded: {details.get('founded_year', '')}"
                )
                self.stdout.write(self.style.SUCCESS(f"Added: {company}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped (Exists): {company}"))
            time.sleep(5)  # Prevent hitting API rate limits
