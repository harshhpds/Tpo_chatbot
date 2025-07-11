import os
from django.core.management.base import BaseCommand
from chatbot.models import PlacementStatistics, TopCompanyOffers, CompanyInfo

class Command(BaseCommand):
    help = 'Populates the CompanyInfo, PlacementStatistics, and TopCompanyOffers models with predefined data.'

    def handle(self, *args, **kwargs):
        # Define the data structure for CompanyInfo
        company_data = [
            {"company_name": "Aakash Educational Services Limited", "description": "Educational Services", "additional_info": "Provides educational services and training."},
            {"company_name": "Accenture P. Ltd.", "description": "Consulting and Technology Services", "additional_info": "Global professional services company."},
            {"company_name": "Accion Lab", "description": "Laboratory Services", "additional_info": "Provides laboratory testing and analysis."},
            {"company_name": "ACG Worldwide", "description": "Global Logistics", "additional_info": "Provides global logistics and supply chain management."},
            {"company_name": "Aditya Birla Capital Ltd", "description": "Financial Services", "additional_info": "Offers financial services and investment solutions."},
            {"company_name": "Amazon Development Centre (india) P. Ltd.", "description": "E-commerce and Technology", "additional_info": "Develops and maintains e-commerce platforms."},
            {"company_name": "Amdocs", "description": "Software and Services", "additional_info": "Provides software solutions and services."},
            {"company_name": "Ansai Nerolac Paints Ltd.", "description": "Paints and Coatings", "additional_info": "Manufactures and sells paints and coatings."},
            {"company_name": "Apl Logistics (india) Pvt. Ltd.", "description": "Logistics Services", "additional_info": "Provides logistics and transportation services."},
            {"company_name": "Arcadis", "description": "Design and Consultancy", "additional_info": "Offers design and consultancy for natural and built assets."},
            {"company_name": "Arcon Technologies", "description": "Technology Solutions", "additional_info": "Provides technology solutions and services."},
            {"company_name": "Ariston Capital Services P. Ltd.", "description": "Capital Services", "additional_info": "Offers capital services and financial solutions."},
            {"company_name": "Arvind Mills Ltd", "description": "Textile Manufacturing", "additional_info": "Manufactures and sells textiles and apparel."},
            {"company_name": "Asahi India Glass Ltd.", "description": "Glass Manufacturing", "additional_info": "Manufactures and sells glass products."},
            {"company_name": "ASEC Engineers", "description": "Engineering Services", "additional_info": "Provides engineering services and solutions."},
            {"company_name": "Asian Heart Institute", "description": "Healthcare", "additional_info": "Provides specialized healthcare services."},
            {"company_name": "Asian Paints", "description": "Paints and Coatings", "additional_info": "Manufactures and sells paints and coatings."},
            {"company_name": "Aspect Ratio", "description": "Aerospace Solutions", "additional_info": "Provides aerospace solutions and services."},
            {"company_name": "Atidan Technologies", "description": "Technology Solutions", "additional_info": "Provides technology solutions and services."},
            {"company_name": "Atos Origin", "description": "IT Services", "additional_info": "Provides IT services and solutions."},
            {"company_name": "Auxilo Finserve Pvt. Ltd", "description": "Financial Services", "additional_info": "Offers financial services and solutions."},
            {"company_name": "Avanti Learning Centres Pvt.ltd.", "description": "Educational Services", "additional_info": "Provides educational services and training."},
        ]

        # Define the data structure for PlacementStatistics
        placement_data = [
            {"branch": "B.Tech Civil", "enrolled_to_tpo": 73, "total_placed": 69, "placement_percentage": 94.52, "average_ctc": 4.93, "academic_year": "2022-2023"},
            {"branch": "B.TECH COMP", "enrolled_to_tpo": 74, "total_placed": 74, "placement_percentage": 100, "average_ctc": 10.33, "academic_year": "2022-2023"},
            {"branch": "B.TECH Elect", "enrolled_to_tpo": 73, "total_placed": 70, "placement_percentage": 95.9, "average_ctc": 5.4, "academic_year": "2022-2023"},
            {"branch": "B.TECH EX", "enrolled_to_tpo": 71, "total_placed": 64, "placement_percentage": 90.1, "average_ctc": 6.25, "academic_year": "2022-2023"},
            {"branch": "B.Tech Extc", "enrolled_to_tpo": 72, "total_placed": 72, "placement_percentage": 100, "average_ctc": 6.13, "academic_year": "2022-2023"},
            {"branch": "B.Tech IT", "enrolled_to_tpo": 80, "total_placed": 80, "placement_percentage": 100, "average_ctc": 8.09, "academic_year": "2022-2023"},
            {"branch": "B.TECH Mech", "enrolled_to_tpo": 71, "total_placed": 63, "placement_percentage": 88.73, "average_ctc": 5.41, "academic_year": "2022-2023"},
            {"branch": "B.TECH Prod", "enrolled_to_tpo": 80, "total_placed": 42, "placement_percentage": 52.5, "average_ctc": 4.27, "academic_year": "2022-2023"},
            {"branch": "B.Tech Text", "enrolled_to_tpo": 77, "total_placed": 77, "placement_percentage": 100, "average_ctc": 5.13, "academic_year": "2022-2023"},
            # Add more data for other academic years as needed
        ]

        # Define the data structure for TopCompanyOffers
        top_company_data = [
            {"company_name": "Morgan Stanley", "ctc_in_lakhs": 29.63, "branch": "B.Tech Computer Engineering", "academic_year": "2022-2023"},
            {"company_name": "VISA", "ctc_in_lakhs": 28.5, "branch": "B.Tech Computer Engineering", "academic_year": "2022-2023"},
            {"company_name": "SAP Labs", "ctc_in_lakhs": 24.5, "branch": "B.Tech Computer Engineering", "academic_year": "2022-2023"},
            {"company_name": "Goldman Sachs", "ctc_in_lakhs": 24, "branch": "B.Tech Computer Engineering", "academic_year": "2022-2023"},
            {"company_name": "Wells Fargo", "ctc_in_lakhs": 24, "branch": "B.Tech Computer Engineering", "academic_year": "2022-2023"},
            # Add more data for other companies and branches as needed
        ]

        # Populate CompanyInfo
        for item in company_data:
            CompanyInfo.objects.update_or_create(
                company_name=item['company_name'],
                defaults={
                    'description': item['description'],
                    'additional_info': item['additional_info']
                }
            )

        # Populate PlacementStatistics
        for data in placement_data:
            PlacementStatistics.objects.update_or_create(
                branch=data['branch'],
                academic_year=data['academic_year'],
                defaults={
                    'enrolled_to_tpo': data['enrolled_to_tpo'],
                    'total_placed': data['total_placed'],
                    'placement_percentage': data['placement_percentage'],
                    'average_ctc': data['average_ctc'],
                }
            )

        # Populate TopCompanyOffers
        for data in top_company_data:
            company, created = CompanyInfo.objects.get_or_create(
                company_name=data['company_name'],
                defaults={
                    'description': 'Description for ' + data['company_name'],
                    'additional_info': 'Additional info for ' + data['company_name'],
                }
            )
            TopCompanyOffers.objects.update_or_create(
                company_name=data['company_name'],
                academic_year=data['academic_year'],
                defaults={
                    'ctc_in_lakhs': data['ctc_in_lakhs'],
                    'branch': data['branch'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the CompanyInfo, PlacementStatistics, and TopCompanyOffers models with data.'))