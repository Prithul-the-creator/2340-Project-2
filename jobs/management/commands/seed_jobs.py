from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from jobs.models import Job

ROLE_INFO = {
    'Software Engineering Intern': {
        'skills': 'Python, Java, JavaScript, React, SQL, Git, Data Structures, Algorithms',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 45,
        'descriptions': [
            'Ship real features alongside our web platform team over a 10-12 week summer internship.',
            'Pair with senior engineers on our internal tools team to build and test new features.',
            'Join our mobile team for the summer to design, build, and ship a customer-facing feature.',
        ],
    },
    'Quantitative Developer Intern': {
        'skills': 'Python, C++, Statistics, Probability, Linear Algebra, Market Microstructure',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 60,
        'descriptions': [
            'Build and backtest trading systems alongside quantitative researchers and traders.',
            'Prototype pricing models and research tooling used directly by our trading desks.',
            'Optimize low-latency trading infrastructure alongside our core platform team.',
        ],
    },
    'Trading Intern': {
        'skills': 'Statistics, Probability, Excel, Market Microstructure, Communication',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 55,
        'descriptions': [
            "Sit with a trading desk to learn market-making and risk management firsthand.",
            "Support a trading desk's daily flow while learning execution and risk controls.",
        ],
    },
    'Machine Learning Engineering Intern': {
        'skills': 'Python, Machine Learning, Statistics, SQL, PyTorch',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 50,
        'descriptions': [
            'Train and ship machine learning models that power our recommendation system.',
            'Build data pipelines and evaluation tooling for our applied ML team.',
        ],
    },
    'Product Management Intern': {
        'skills': 'Product Strategy, Data Analysis, Communication, Agile, SQL',
        'employment_type': Job.EmploymentType.INTERN,
        'salary': 40,
        'descriptions': [
            'Partner with engineering and design to scope and ship a real product feature.',
            'Run user research and help define requirements for a new product initiative.',
        ],
    },
    'Software Engineer, New Grad': {
        'skills': 'Python, Java, JavaScript, React, SQL, Git, AWS, Docker, Data Structures, Algorithms',
        'employment_type': Job.EmploymentType.FULL_TIME,
        'salary': 140000,
        'descriptions': [
            'Join a product engineering team as a full-time software engineer.',
        ],
    },
    'Associate Product Manager': {
        'skills': 'Product Strategy, Data Analysis, Communication, Agile, Roadmapping',
        'employment_type': Job.EmploymentType.FULL_TIME,
        'salary': 120000,
        'descriptions': [
            'Own a piece of the roadmap and work cross-functionally to ship it.',
        ],
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
                for i in range(count):
                    Job.objects.create(
                        title=title,
                        company=company['name'],
                        location=company['location'],
                        skills_needed=info['skills'],
                        description=info['descriptions'][i % len(info['descriptions'])],
                        employment_type=info['employment_type'],
                        salary=info['salary'],
                        remote_work=company['remote_work'],
                        visa_sponsorship=company['visa_sponsorship'],
                        owner=recruiter,
                    )

            self.stdout.write(f"{company['name']}: {sum(c for _, c in company['postings'])} postings ({company['recruiter_username']} / {DEMO_PASSWORD})")

        self.stdout.write(self.style.SUCCESS('Seeded 20 job postings across 4 companies.'))
