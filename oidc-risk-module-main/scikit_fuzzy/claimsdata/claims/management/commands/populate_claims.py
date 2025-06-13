from django.core.management.base import BaseCommand
from claims.models import ClaimTableEducation, ClaimTableOSP

class Command(BaseCommand):
    help = 'Populate the database with initial claims data'
    def handle(self, *args, **kwargs):
        # Delete old data
        ClaimTableEducation.objects.all().delete()
        ClaimTableOSP.objects.all().delete()

        # Data for ClaimTableEducation
        education_claims = [
            {"claim_designation": "sub", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "given_name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "family_name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "middle_name", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "nickname", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "username", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "profile", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "picture", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "website", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "email", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "email_verified", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "gender", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "birthdate", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "zoneinfo", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "locale", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "number", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "phone_number_verified", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "address", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "updated_at", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "claims_locales", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "formatted", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "street_address", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "locality", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "region", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "postal_code", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "country", "impact": 0.55, "gdpr_compliance": 0.0},
        ]
        # Data for ClaimTableOSP
        osp_claims = [
            {"claim_designation": "sub", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "given_name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "family_name", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "middle_name", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "nickname", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "username", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "profile", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "picture", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "website", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "email", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "email_verified", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "gender", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "birthdate", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "zoneinfo", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "locale", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "number", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "phone_number_verified", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "address", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "updated_at", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "claims_locales", "impact": 0.2, "gdpr_compliance": 1.0},
            {"claim_designation": "formatted", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "street_address", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "locality", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "region", "impact": 0.85, "gdpr_compliance": 1.0},
            {"claim_designation": "postal_code", "impact": 0.55, "gdpr_compliance": 1.0},
            {"claim_designation": "country", "impact": 0.55, "gdpr_compliance": 1.0},
        ]
        # Populate ClaimTableEducation
        for claim in education_claims:
            ClaimTableEducation.objects.get_or_create(
                claim_designation=claim["claim_designation"],
                impact=claim["impact"],
                gdpr_compliance=claim["gdpr_compliance"]
            )
        # Populate ClaimTableOSP
        for claim in osp_claims:
            ClaimTableOSP.objects.get_or_create(
                claim_designation=claim["claim_designation"],
                impact=claim["impact"],
                gdpr_compliance=claim["gdpr_compliance"]
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
