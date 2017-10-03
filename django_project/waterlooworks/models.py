from django.db import models


# Create your models here.
class Job(models.Model):
    work_term = models.CharField(max_length=50)
    job_country = models.CharField(max_length=50)
    job_province_state = models.CharField(max_length=50)
    number_of_job_openings = models.CharField(max_length=10)
    fake_id = models.CharField(max_length=50)
    job_summary = models.TextField()
    application_documents_required = models.CharField(max_length=50)
    special_job_requirements = models.CharField(max_length=100)
    job_city = models.CharField(max_length=50)
    required_skills = models.TextField()
    job_type = models.CharField(max_length=50)
    job_Category_noc = models.CharField(max_length=100)
    targeted_degrees_and_disciplines = models.TextField()
    region = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    job_responsibilities = models.TextField()
    division = models.CharField(max_length=50)
    work_Term_duration = models.CharField(max_length=50)
    additional_information = models.CharField(max_length=50)
    job_address_line_one = models.CharField(max_length=100)
    job_postal_code_zip_code_xx_x = models.CharField(max_length=20)
    employer_internal_job_number = models.CharField(max_length=50)
    transportation_and_housing = models.CharField(max_length=50)
    compensation_and_benefits_information = models.TextField()
    level = models.CharField(max_length=50)
    organization = models.CharField(max_length=50)
    additional_application_information = models.CharField(max_length=50)
    job_address_line_two = models.CharField(max_length=100)
    additional_Job_identifiers = models.CharField(max_length=100)
    job_Location_if_exact_address_unknown_or_multiple_locations = models.CharField(max_length=100)
    job_website_url = models.URLField(default="")
    job_icon_url = models.URLField(default="")
    organization_price = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.fake_id + "-" + self.job_title
