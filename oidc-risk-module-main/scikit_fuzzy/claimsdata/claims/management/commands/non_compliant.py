from django.core.management.base import BaseCommand
from claims.models import ClaimTableEducation, ClaimTableOSP

class Command(BaseCommand):
    help = 'Populate the database with initial claims data with gdpr_compliance set to 0.0'

    def handle(self, *args, **kwargs):
        # Delete old data
        ClaimTableEducation.objects.all().delete()
        ClaimTableOSP.objects.all().delete()

        # Data for ClaimTableEducation
        education_claims = [
            {"claim_designation": "username", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "profile", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "email", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "phone", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "address", "impact": 0.85, "gdpr_compliance": 0.0},
        ]

        # Data for ClaimTableOSP
        osp_claims = [
            {"claim_designation": "username", "impact": 0.2, "gdpr_compliance": 0.0},
            {"claim_designation": "profile", "impact": 0.55, "gdpr_compliance": 0.0},
            {"claim_designation": "email", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "phone", "impact": 0.85, "gdpr_compliance": 0.0},
            {"claim_designation": "address", "impact": 0.85, "gdpr_compliance": 0.0},
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

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with gdpr_compliance set to 0.0'))
