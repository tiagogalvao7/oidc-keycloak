from django.db import models

class ClaimTableEducation(models.Model):
    claim_designation = models.CharField(max_length=255)
    impact = models.FloatField()
    gdpr_compliance = models.FloatField()

    def __str__(self):
        return f"Education Claim - Designation: {self.claim_designation}, Impact: {self.impact}, GDPR Compliance: {self.gdpr_compliance}"

class ClaimTableOSP(models.Model):
    claim_designation = models.CharField(max_length=255)
    impact = models.FloatField()
    gdpr_compliance = models.FloatField()

    def __str__(self):
        return f"OSP Claim - Designation: {self.claim_designation}, Impact: {self.impact}, GDPR Compliance: {self.gdpr_compliance}"

class Transaction(models.Model):
    name = models.CharField(max_length=255)
    transaction = models.CharField(max_length=255)

    def __str__(self):
        return f"Transaction - Name: {self.name}, Transaction: {self.transaction}"
