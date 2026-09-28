from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from jobs.models import Job

ROLE_INFO = {
    'Software Engineering Intern': {
        'skills': 'Python, Java, JavaScript, React, SQL, Git, Data Structures, Algorithms',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 45,
    },
    'Quantitative Developer Intern': {
        'skills': 'Python, C++, Statistics, Probability, Linear Algebra, Market Microstructure',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 60,
    },
    'Trading Intern': {
        'skills': 'Statistics, Probability, Excel, Market Microstructure, Communication',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 55,
    },
    'Machine Learning Engineering Intern': {
        'skills': 'Python, Machine Learning, Statistics, SQL, PyTorch',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 50,
    },
    'Product Management Intern': {
        'skills': 'Product Strategy, Data Analysis, Communication, Agile, SQL',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 40,
    },
    'Software Engineer, New Grad': {
        'skills': 'Python, Java, JavaScript, React, SQL, Git, AWS, Docker, Data Structures, Algorithms',
        'employment_type': Job.EmploymentType.FULL_TIME,
        'salary': 140000,
    },
    'Associate Product Manager': {
        'skills': 'Product Strategy, Data Analysis, Communication, Agile, Roadmapping',
        'employment_type': Job.EmploymentType.FULL_TIME,
        'salary': 120000,
    },
}

COMPANIES = [
    {
        'name': 'Three Sigma',
        'location': 'New York, NY',
        'recruiter_username': 'recruiter_threesigma',
        'remote_work': False,
        'visa_sponsorship': True,
        'postings': [
            ('Quantitative Developer Intern', 3),
            ('Trading Intern', 2),
        ],
    },
    {
        'name': 'Orange',
        'location': 'San Francisco, CA',
        'recruiter_username': 'recruiter_orange',
        'remote_work': True,
        'visa_sponsorship': True,
        'postings': [
            ('Software Engineering Intern', 3),
            ('Machine Learning Engineering Intern', 2),
        ],
    },
    {
        'name': 'GiftGrabs',
        'location': 'Atlanta, GA',
        'recruiter_username': 'recruiter_giftgrabs',
        'remote_work': False,
        'visa_sponsorship': False,
        'postings': [
            ('Software Engineering Intern', 3),
            ('Product Management Intern', 2),
        ],
    },
    {
        'name': 'Silverman Sachs',
        'location': 'Chicago, IL',
        'recruiter_username': 'recruiter_silverman',
        'remote_work': False,
        'visa_sponsorship': True,
        'postings': [
            ('Trading Intern', 1),
            ('Software Engineering Intern', 2),
            ('Software Engineer, New Grad', 1),
            ('Associate Product Manager', 1),
        ],
    },
]

DEMO_PASSWORD = 'seekr1234'


class Command(BaseCommand):
    help = 'Seeds demo companies, recruiters, and job postings.'

    def handle(self, *args, **options):
        recruiter_group, _ = Group.objects.get_or_create(name='Recruiter')

        for company in COMPANIES:
            recruiter, _ = User.objects.get_or_create(username=company['recruiter_username'])
            recruiter.set_password(DEMO_PASSWORD)
            recruiter.save()
            recruiter.groups.add(recruiter_group)

            Job.objects.filter(company=company['name']).delete()
            for title, count in company['postings']:
                info = ROLE_INFO[title]
                for _ in range(count):
                    Job.objects.create(
                        title=title,
                        company=company['name'],
                        location=company['location'],
                        skills_needed=info['skills'],
                        employment_type=info['employment_type'],
                        salary=info['salary'],
                        remote_work=company['remote_work'],
                        visa_sponsorship=company['visa_sponsorship'],
                        owner=recruiter,
                    )

            self.stdout.write(f"{company['name']}: {sum(c for _, c in company['postings'])} postings ({company['recruiter_username']} / {DEMO_PASSWORD})")

        self.stdout.write(self.style.SUCCESS('Seeded 20 job postings across 4 companies.'))
