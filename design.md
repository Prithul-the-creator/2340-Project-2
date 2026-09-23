# Seekr — Design System & UI/UX Guidelines

## 1. Product Overview

**Seekr** is a modern recruiting platform designed to connect early-career job seekers with recruiters and relevant opportunities.

The platform serves three primary user groups:

* **Job Seekers** — create professional profiles, discover jobs, apply, and track applications.
* **Recruiters** — publish jobs, discover candidates, review applicants, and manage recruiting pipelines.
* **Administrators** — manage users, roles, and platform integrity.

Seekr should feel approachable to a student searching for their first internship while remaining polished and professional enough for a recruiter using the platform every day.

The interface should communicate:

> **Professional without being corporate. Friendly without being playful. Powerful without feeling complicated.**

The visual direction takes inspiration from products such as Stripe, Notion, Linear, and other modern productivity platforms. Seekr should use strong typography, generous whitespace, subtle borders, warm neutral colors, and carefully designed information hierarchy rather than decorative effects.

---

# 2. Core Design Principles

Every Seekr interface should follow six principles.

## 2.1 Simple

The interface should expose the information users need without unnecessary visual noise.

Avoid:

* excessive navigation
* unnecessary cards
* excessive icons
* decorative illustrations
* multiple competing accent colors
* overly complicated dashboards

Prefer clear hierarchy and whitespace.

---

## 2.2 Human

Job searching can already feel transactional. Seekr should make the experience feel more personal.

Candidate profiles should emphasize the person before their metrics.

For example:

**Preferred**

> Alex Chen
> Computer Science @ Georgia Tech
> Interested in distributed systems and developer infrastructure

Rather than:

> Candidate #19281
> Match Score: 87%

Recruiting data should support human decision-making rather than make candidates feel like database entries.

---

## 2.3 Information-Dense, Not Visually Dense

Recruiting applications naturally contain large amounts of information.

Seekr should organize this information using:

* typography hierarchy
* spacing
* tabs
* sections
* tables
* subtle dividers
* progressive disclosure

rather than placing everything inside separate cards.

---

## 2.4 Consistent

The same interaction should look and behave the same everywhere.

For example:

* all primary buttons use the same style
* all filters use the same component
* all status indicators use the same system
* job cards use the same structure
* candidate cards use the same structure
* search behaves consistently across jobs and candidates

Reusable components should be preferred over page-specific UI.

---

## 2.5 Calm

Seekr should avoid the visual intensity common in many career platforms.

Do not use:

* gradients
* neon colors
* oversized shadows
* glassmorphism
* excessive animations
* emojis as interface elements
* overly rounded "bubble" interfaces
* gamification elements

Interactions should feel deliberate and predictable.

---

## 2.6 Trustworthy

Users are sharing employment history, education, applications, salary preferences, and potentially sensitive recruiting information.

The interface should communicate trust through:

* clear privacy controls
* understandable labels
* predictable navigation
* explicit visibility indicators
* confirmation for destructive actions
* transparent application statuses

---

# 3. Brand Identity

## 3.1 Name

**Seekr**

The name should normally appear exactly as:

`Seekr`

Avoid stylizations such as:

`SEEKR`

`seekr.`

`SeekR`

unless used intentionally in a logo treatment.

---

## 3.2 Brand Personality

Seekr's personality should be:

* intelligent
* modern
* welcoming
* ambitious
* calm
* trustworthy
* professional
* youthful without being childish

The product should feel appropriate for both a 19-year-old student searching for an internship and a recruiter managing hundreds of applicants.

---

# 4. Visual Direction

Seekr uses a **warm minimal interface**.

The visual hierarchy should primarily come from:

1. typography
2. whitespace
3. borders
4. surface colors
5. a restrained accent color

Shadows should rarely be necessary.

A typical page should contain large areas of whitespace rather than filling every available region with cards.

---

# 5. Color System

Colors should be implemented as semantic design tokens rather than hardcoded throughout the application.

## 5.1 Light Theme

### Background

```css
--background: #FAF9F7;
--surface: #FFFFFF;
--surface-secondary: #F5F3F0;
--surface-hover: #F1EFEC;
```

The primary background uses a subtle warm off-white rather than pure white.

### Text

```css
--text-primary: #1C1917;
--text-secondary: #57534E;
--text-muted: #78716C;
--text-disabled: #A8A29E;
```

### Borders

```css
--border: #E7E5E4;
--border-strong: #D6D3D1;
```

### Brand Accent

Seekr should use a restrained blue as its primary interactive color.

```css
--accent: #2563EB;
--accent-hover: #1D4ED8;
--accent-subtle: #EFF6FF;
```

The accent should primarily indicate:

* primary actions
* links
* selected controls
* focus states
* active navigation
* important interactive elements

Large areas should generally **not** be filled with the accent color.

### Semantic Colors

```css
--success: #15803D;
--success-subtle: #F0FDF4;

--warning: #B45309;
--warning-subtle: #FFFBEB;

--danger: #B91C1C;
--danger-subtle: #FEF2F2;

--info: #0369A1;
--info-subtle: #F0F9FF;
```

---

# 6. Dark Mode

Dark mode should be intentionally designed rather than simply inverting light-mode colors.

```css
--background: #111110;
--surface: #191918;
--surface-secondary: #222220;
--surface-hover: #292927;

--text-primary: #FAFAF9;
--text-secondary: #D6D3D1;
--text-muted: #A8A29E;
--text-disabled: #78716C;

--border: #302F2D;
--border-strong: #44403C;

--accent: #60A5FA;
--accent-hover: #93C5FD;
--accent-subtle: #172554;
```

Avoid pure `#000000` backgrounds.

Dark mode should maintain the warm-neutral character of the light theme.

Users should be able to choose:

* Light
* Dark
* System

The default should be **System**.

---

# 7. Typography

Typography should provide most of the visual hierarchy.

## Primary Font

Recommended:

**Inter**

Fallback:

```css
font-family:
  Inter,
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;
```

Alternative fonts such as Geist may also be considered if the team prefers them.

---

## 7.1 Type Scale

### Display

```text
48px / 56px
font-weight: 600
letter-spacing: -0.03em
```

Used sparingly for landing pages.

### H1

```text
36px / 44px
font-weight: 600
letter-spacing: -0.025em
```

### H2

```text
28px / 36px
font-weight: 600
letter-spacing: -0.02em
```

### H3

```text
22px / 30px
font-weight: 600
```

### H4

```text
18px / 26px
font-weight: 600
```

### Body

```text
16px / 24px
font-weight: 400
```

### Small

```text
14px / 20px
font-weight: 400
```

### Caption

```text
12px / 16px
font-weight: 500
```

Avoid excessive bold text.

Most body text should use regular weight.

---

# 8. Spacing System

Use a consistent 4px-based spacing scale.

```text
4px
8px
12px
16px
20px
24px
32px
40px
48px
64px
80px
96px
```

Typical usage:

```text
Button padding:        8px 14px
Input padding:         10px 12px
Card padding:          20–24px
Section gap:           32–48px
Major page sections:   64px+
```

Do not create arbitrary spacing values unless necessary.

---

# 9. Border Radius

Seekr should feel modern but not excessively rounded.

```css
--radius-small: 6px;
--radius-medium: 8px;
--radius-large: 12px;
--radius-xl: 16px;
--radius-pill: 999px;
```

Typical usage:

```text
Buttons       8px
Inputs        8px
Cards         12px
Modals        16px
Tags          pill
Avatars       circle
```

Avoid using large 20–30px radii on normal interface cards.

---

# 10. Shadows

Shadows should be subtle and uncommon.

Most containers should use borders rather than shadows.

Example:

```css
box-shadow:
  0 1px 2px rgba(0, 0, 0, 0.04),
  0 2px 8px rgba(0, 0, 0, 0.03);
```

Use shadows primarily for elevated elements:

* dropdowns
* command menus
* popovers
* modals
* floating navigation elements

---

# 11. Navigation

Seekr uses a **top navigation system**.

The navigation should remain consistent across the product.

## Job Seeker Navigation

```text
Seekr        Jobs        Applications        Network/Profile        [Search]       [Avatar]
```

A cleaner implementation may use:

```text
Seekr        Jobs        Applications        Profile                 Search   Avatar
```

## Recruiter Navigation

```text
Seekr        Jobs        Candidates        Applications        Saved Searches       Avatar
```

## Administrator Navigation

```text
Seekr        Users        Roles        Reports / Moderation        Avatar
```

The logo should always return users to their primary dashboard.

---

# 12. Global Search

Search should be treated as a major product interaction.

The global search experience can be inspired by command palettes found in modern productivity applications.

Example:

```text
┌─────────────────────────────────────────────┐
│ Search jobs, candidates, skills...          │
├─────────────────────────────────────────────┤
│ Recent                                      │
│ Software Engineer                           │
│ Machine Learning Intern                     │
│ Atlanta                                     │
└─────────────────────────────────────────────┘
```

Keyboard navigation should be supported where practical.

---

# 13. Buttons

There should be four major button styles.

## Primary

Used for the most important action.

Examples:

* Apply
* Post job
* Save changes
* Send application

Visual treatment:

```text
solid accent background
white text
```

Only one primary action should generally dominate a section.

---

## Secondary

White/surface background with border.

Examples:

* Save job
* Edit profile
* View profile
* Add experience

---

## Ghost

Minimal background.

Used for lower-priority actions.

Examples:

* Cancel
* Clear filters
* navigation actions

---

## Destructive

Reserved for destructive actions.

Examples:

* Delete account
* Remove job
* Delete posting

Never use destructive styling for ordinary navigation.

---

# 14. Inputs

All inputs should share consistent:

* height
* typography
* border
* focus state
* validation behavior

Standard input height:

`40–44px`

Example:

```text
Location

┌───────────────────────────────────┐
│ Atlanta, GA                       │
└───────────────────────────────────┘
```

Labels should remain visible rather than relying exclusively on placeholders.

---

# 15. Tags and Chips

Tags are useful for:

* skills
* technologies
* job types
* locations
* candidate attributes
* filters

Example:

```text
Python    React    AWS    Machine Learning
```

Tags should use subtle backgrounds.

Avoid giving every skill a different color.

---

# 16. Status System

Applications use:

```text
Applied → Review → Interview → Offer → Closed
```

Statuses should combine text with subtle visual indicators.

Never rely solely on color to communicate status.

Example:

```text
● Interview
```

The text label is always required.

---

# 17. Job Seeker Experience

## 17.1 Job Discovery

The Jobs page is one of Seekr's primary surfaces.

Recommended layout:

```text
---------------------------------------------------------

Jobs

Find opportunities that fit what you're looking for.

[ Search jobs, companies, or skills              ]

[Location] [Experience] [Salary] [Remote] [Visa] [More]

---------------------------------------------------------

247 opportunities

┌─────────────────────────────┐
│ Software Engineer Intern    │
│ Acme                        │
│                             │
│ Atlanta, GA · Hybrid        │
│ $35–45/hr                   │
│                             │
│ Python   React   AWS        │
│                             │
│ Posted 2 days ago      Save │
└─────────────────────────────┘
```

Job cards should emphasize:

1. role
2. company
3. location/work model
4. compensation when available
5. relevant skills
6. posting recency

Avoid overcrowding cards with company information.

---

# 18. Job Detail Page

Recommended hierarchy:

```text
Company

Software Engineer Intern

Atlanta, GA · Hybrid
$35–45/hr
Internship

[Apply] [Save]

------------------------------------------------

About the role

Responsibilities

Qualifications

Skills

Python    React    AWS

------------------------------------------------

About the company
```

The primary action should remain easy to locate.

A sticky application action may be used on desktop.

---

# 19. Application Flow

Applying should be intentionally lightweight.

Clicking **Apply** opens a focused flow.

```text
Apply to Software Engineer Intern

Your profile
Prithul Baveja
Computer Science · Georgia Tech

Resume
resume.pdf

Optional note

┌─────────────────────────────────────┐
│ Tell the recruiter why you're       │
│ interested...                       │
└─────────────────────────────────────┘

                 Cancel     Submit application
```

The user should understand exactly what information will be shared before submission.

---

# 20. Application Tracking

Applications should resemble a clean workflow rather than a complicated applicant-tracking system.

Example:

```text
Applications

All    Applied    Review    Interview    Offer    Closed

Software Engineer Intern
Acme
Applied Sep 18

Applied ───── Review ───── Interview ───── Offer
                        ●
```

Users should immediately understand:

* where they applied
* when they applied
* their current status
* whether action is required

---

# 21. Job Seeker Profile

Profiles should feel like professional portfolios rather than resumes copied into a webpage.

Recommended hierarchy:

```text
[Avatar]

Alex Chen
Computer Science @ Georgia Tech
Atlanta, GA

Building distributed systems and developer tools.

[Website] [GitHub] [LinkedIn]

Python   Go   AWS   Kubernetes

------------------------------------------------

About

Experience

Education

Projects

Skills
```

Recruiters should be able to scan a profile quickly while still having the option to explore deeper.

---

# 22. Privacy Controls

Privacy should be understandable rather than buried inside settings.

Example:

```text
Profile visibility

○ Public to recruiters
  Recruiters on Seekr can discover your profile.

○ Applications only
  Only recruiters at companies you apply to can view it.

○ Private
  Your profile cannot be discovered.
```

Specific fields may eventually receive additional visibility controls.

---

# 23. Map Experience

Location is a major differentiator for Seekr.

The job discovery interface should support:

```text
[List] [Map]
```

and potentially a split view:

```text
┌───────────────────────┬──────────────────────────────┐
│                       │                              │
│ Job results           │             MAP              │
│                       │                              │
│ Software Engineer     │        • Atlanta             │
│ Atlanta               │                              │
│                       │              • Charlotte     │
│ Data Scientist        │                              │
│ Charlotte             │                              │
│                       │                              │
└───────────────────────┴──────────────────────────────┘
```

Selecting a map marker should highlight the corresponding job.

Selecting a job should highlight its marker.

Map markers should remain visually simple.

---

# 24. Recruiter Experience

Recruiter interfaces may contain more information than job-seeker interfaces but should maintain the same design system.

Recruiters should primarily interact with:

```text
Jobs
Candidates
Applications
Saved Searches
```

---

# 25. Recruiter Dashboard

Example:

```text
Good morning, Alex

Here's what's happening with your hiring.

Active jobs                     8
New applicants                 34
Candidates in interview        12

------------------------------------------------

Recent activity

Jordan Lee applied to Software Engineer Intern
2 hours ago

Maya Patel moved to Interview
4 hours ago

------------------------------------------------

Your jobs

Software Engineer Intern
124 applicants
18 in review
5 interviewing
```

Avoid filling the dashboard with unnecessary charts simply because data exists.

Every visualization should answer a useful question.

---

# 26. Job Management

Recruiters should be able to see their openings in a simple table.

```text
Jobs

[Post a job]

Role                     Status       Applicants     Updated

Software Engineer        Active       124            Today
Product Designer         Active        68            Yesterday
Data Scientist           Draft          —            Sep 14
```

Tables should be preferred over collections of large cards when users need to compare many records.

---

# 27. Candidate Search

Candidate discovery should mirror the job search experience.

```text
Candidates

[ Search candidates, skills, projects... ]

[Skills] [Location] [Education] [Experience] [More]

------------------------------------------------------

Jordan Lee
Georgia Tech · Computer Science
Atlanta, GA

Python   PyTorch   AWS

Machine Learning Intern · Previous experience at...
```

The search/filter interaction should feel almost identical to job discovery.

---

# 28. Candidate Detail

Recruiters should be able to evaluate candidates without constantly changing pages.

A candidate detail panel or page should include:

```text
Jordan Lee

Computer Science @ Georgia Tech
Atlanta, GA

Python   PyTorch   AWS

[Save candidate] [Contact]

-----------------------------------

Application

Applied Sep 20
Software Engineer Intern

Note
"I'm particularly interested..."

-----------------------------------

Experience

Projects

Education

Skills
```

Application context and candidate profile information should appear together.

---

# 29. Applicant Pipeline

Recruiters should have a lightweight pipeline.

```text
Applied        Review        Interview       Offer

Jordan         Maya          Alex            Sam
Taylor         Chris         Jamie
Morgan
```

A Kanban-style interface may be appropriate, but it should not become visually cluttered.

An alternative table view should eventually be considered for larger applicant pools.

---

# 30. Candidate Recommendations

Recommendations should explain **why** a candidate is being surfaced.

Avoid:

```text
98% MATCH
```

Prefer:

```text
Recommended for Software Engineer Intern

Jordan Lee

Matches 4 required skills
Python · React · AWS · PostgreSQL

Located in Atlanta
Open to hybrid roles
```

This makes recommendations more understandable and trustworthy.

---

# 31. Saved Searches

Recruiters should be able to save candidate filters.

Example:

```text
Backend interns — Atlanta

Python
AWS
Atlanta, GA
Internship experience

23 candidates

[View results]
```

Alerts should clearly state why the recruiter received them.

Example:

> 4 new candidates match your "Backend interns — Atlanta" search.

---

# 32. Administrator Experience

Administration should prioritize functionality and clarity.

Primary sections:

```text
Users
Roles
Reports
Platform Settings
```

Example user table:

```text
Name             Role          Status          Joined

Jordan Lee       Job Seeker    Active          Sep 18
Alex Morgan      Recruiter     Active          Sep 12
Taylor Smith     Recruiter     Suspended       Aug 30
```

Potential actions:

```text
View account
Change role
Suspend account
Restore account
```

Destructive or high-impact actions should require confirmation.

---

# 33. Empty States

Empty states should explain what happened and provide a useful next step.

Bad:

> No results.

Better:

> No jobs match these filters.

> Try expanding your location or removing a skill filter.

`Clear filters`

For a recruiter:

> No candidates saved yet.

> Save candidates while searching to build your shortlist.

`Find candidates`

Do not use cartoon illustrations or emojis for empty states.

---

# 34. Loading States

Use skeleton interfaces when content structure is predictable.

Example:

```text
██████████████████

████████
██████████████

██████  ██████  █████
```

Avoid large loading spinners for entire pages whenever possible.

---

# 35. Error States

Errors should explain:

1. what happened
2. whether user data was affected
3. what the user can do next

Example:

> We couldn't submit your application.

> Your information hasn't been lost. Try submitting again.

`Try again`

Avoid technical errors such as:

> HTTP 500

unless displayed in a developer environment.

---

# 36. Toast Notifications

Use temporary notifications for successful lightweight actions.

Examples:

```text
Job saved
Profile updated
Search saved
Application submitted
```

Do not use toast notifications for information requiring user action.

---

# 37. Modals

Modals should only interrupt users when necessary.

Appropriate:

```text
Delete job?
Remove candidate?
Discard unsaved changes?
Change user role?
```

Not appropriate:

```text
Viewing ordinary profile information
Reading a job description
Browsing search results
```

---

# 38. Motion

Animation should communicate state rather than decorate the interface.

Recommended duration:

```text
100–200ms
```

Appropriate animation:

* dropdown opening
* tab transitions
* hover states
* modal appearance
* expanding filters
* loading transitions

Avoid:

* bouncing elements
* looping animations
* animated backgrounds
* elaborate page transitions

Support:

```css
prefers-reduced-motion
```

---

# 39. Responsive Design

Seekr should support:

```text
Desktop
Tablet
Mobile
```

Suggested breakpoints:

```css
mobile:  < 640px
tablet:  640px–1024px
desktop: > 1024px
```

Desktop should be the primary design target for recruiter workflows.

Job-seeker workflows should receive strong mobile support because students may frequently browse opportunities from phones.

---

# 40. Mobile Navigation

Desktop top navigation should collapse into a compact mobile navigation.

Example:

```text
Seekr                              [Avatar]

Jobs
Applications
Profile
```

A bottom navigation may also be considered for job-seeker mobile experiences if usability testing supports it.

Do not simply compress desktop navigation until labels no longer fit.

---

# 41. Page Width

General content:

```css
max-width: 1200px;
margin: 0 auto;
```

Reading-heavy content:

```css
max-width: 760px;
```

Search and dashboard interfaces may use wider layouts.

Avoid stretching paragraphs across very wide screens.

---

# 42. Accessibility

Seekr should target **WCAG 2.1 AA** accessibility standards.

Requirements include:

* sufficient color contrast
* keyboard-accessible controls
* visible focus indicators
* semantic HTML
* meaningful labels
* accessible form errors
* alt text where appropriate
* screen-reader-friendly navigation
* minimum reasonable touch target sizes

Color should never be the only indication of state.

For example:

Bad:

```text
Green = accepted
Red = rejected
```

Better:

```text
● Offer
● Closed
```

with accessible text labels.

---

# 43. Iconography

Use one consistent icon library.

Recommended:

**Lucide Icons**

Icons should generally use:

```text
16px
18px
20px
```

Do not mix icon styles.

Do not use emojis as icons.

Avoid icons when text communicates the action more clearly.

---

# 44. Content Tone

Seekr copy should be concise and conversational.

Avoid corporate language.

Bad:

> Utilize our advanced candidate discovery functionality to identify prospective talent.

Better:

> Find candidates

Bad:

> Your application has been successfully transmitted.

Better:

> Application submitted.

---

# 45. Naming Conventions

Navigation labels should generally be nouns:

```text
Jobs
Candidates
Applications
Profile
Settings
```

Buttons should generally begin with verbs:

```text
Apply
Save job
Edit profile
Post job
View candidates
Save search
```

---

# 46. Search and Filter Behavior

Filters should update results predictably.

Active filters should always be visible.

Example:

```text
Software Engineer

Atlanta ×
Remote ×
$30+/hr ×

Clear all
```

Users should never wonder which filters are currently affecting results.

On mobile, filters may open inside a dedicated filter sheet.

---

# 47. URL Design

Important views should have shareable URLs.

Examples:

```text
/jobs
/jobs/:jobId

/candidates
/candidates/:candidateId

/applications

/profile/:username

/recruiter/jobs
/recruiter/jobs/:jobId/applicants

/settings/privacy
```

Search parameters should preferably appear in URLs.

Example:

```text
/jobs?location=atlanta&remote=true&skill=python
```

This allows searches to be bookmarked and shared.

---

# 48. Component Architecture

The frontend should prioritize reusable components.

Potential component structure:

```text
components/

  navigation/
    Navbar
    UserMenu
    SearchButton

  jobs/
    JobCard
    JobList
    JobFilters
    JobDetails
    JobStatus

  candidates/
    CandidateCard
    CandidateList
    CandidateFilters
    CandidateProfile

  applications/
    ApplicationCard
    ApplicationStatus
    ApplicationTimeline

  profile/
    ProfileHeader
    ExperienceSection
    EducationSection
    ProjectSection
    SkillsList

  maps/
    JobMap
    CandidateMap
    MapMarker

  ui/
    Button
    Input
    Select
    Checkbox
    Radio
    Badge
    Modal
    Dropdown
    Tabs
    Tooltip
    Toast
    Skeleton
    Avatar
```

Page-specific components should compose these primitives rather than recreate them.

---

# 49. Interaction States

Every interactive component should account for:

```text
Default
Hover
Focus
Active
Disabled
Loading
Error
```

Buttons, for example, should not shift dimensions when entering a loading state.

---

# 50. Design Tokens

Core visual values should eventually live as reusable tokens.

Example:

```css
:root {
  --background: #FAF9F7;
  --surface: #FFFFFF;

  --text-primary: #1C1917;
  --text-secondary: #57534E;

  --border: #E7E5E4;

  --accent: #2563EB;

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
}
```

Components should reference these tokens rather than introducing arbitrary values.

---

# 51. Layout Philosophy

A common Seekr page should approximately follow:

```text
TOP NAVIGATION

------------------------------------------------

PAGE TITLE
Short contextual description                 ACTION

------------------------------------------------

SEARCH / FILTERS

------------------------------------------------

PRIMARY CONTENT

------------------------------------------------
```

Users should be able to understand the purpose of a page within seconds.

---

# 52. Progressive Disclosure

Advanced functionality should appear when users need it.

For example, job search should initially show:

```text
Title
Location
Remote
Salary
```

Less common filters can live under:

`More filters`

Similarly, recruiter candidate search should not display twenty filters simultaneously.

---

# 53. Visual Hierarchy

When looking at a page, attention should generally follow:

```text
Page title
↓
Primary action
↓
Primary content
↓
Secondary information
↓
Metadata
```

Metadata should not visually compete with the main content.

---

# 54. Landing Page Direction

Seekr's public landing page should remain extremely simple.

Possible structure:

```text
Seekr                                      Jobs    For recruiters    Sign in

--------------------------------------------------------------------------

Find the right opportunity.
Meet the right people.

A better way for early-career talent and
recruiters to find each other.

[Explore jobs]     [Find candidates]

--------------------------------------------------------------------------

Find opportunities built around what matters to you.

[Job search preview]

--------------------------------------------------------------------------

For candidates

Build a profile.
Discover relevant roles.
Track every application.

--------------------------------------------------------------------------

For recruiters

Discover talent.
Manage applicants.
Build stronger candidate pipelines.

--------------------------------------------------------------------------

Seekr
```

Avoid giant product illustrations unless they communicate actual functionality.

Real interface previews are preferred.

---

# 55. What Seekr Should NOT Look Like

Seekr should not resemble:

* a crypto product
* a gaming interface
* a generic Bootstrap dashboard
* a social-media feed
* a traditional enterprise HR portal
* an overly playful student project
* a collection of disconnected cards

Specifically avoid:

```text
Gradients
Glassmorphism
Neon colors
Emojis
Huge drop shadows
Excessive pills
Animated backgrounds
3D decorative objects
Excessive illustrations
Multiple accent colors
Overly rounded components
```

---

# 56. Inspiration

Seekr should take conceptual inspiration from several modern products without directly copying them.

### Stripe

Take inspiration from:

* typography
* information hierarchy
* polished interactions
* thoughtful spacing
* professional visual language

Do **not** adopt Stripe's gradient-heavy branding.

### Notion

Take inspiration from:

* calm interfaces
* restrained colors
* content-first layouts
* simple navigation
* understandable controls

### Linear

Take inspiration from:

* compact information presentation
* subtle borders
* keyboard-friendly interactions
* polished interaction states
* consistent component systems

Seekr should combine these ideas into its own identity.

---

# 57. Feature-to-Interface Mapping

The Spring #1 requirements map to the following major interfaces.

| User Story                | Primary Interface                |
| ------------------------- | -------------------------------- |
| Profile Creation          | Profile / Edit Profile           |
| Job Search & Filtering    | Job Discovery                    |
| Application Submission    | Job Detail / Apply Flow          |
| Application Tracking      | Applications                     |
| Privacy Controls          | Settings / Privacy               |
| Job Management            | Recruiter Jobs                   |
| Candidate Search          | Candidate Discovery              |
| Saved Searches & Alerts   | Saved Searches                   |
| Candidate Recommendations | Job Candidates / Recommendations |
| Application Review        | Candidate/Application Detail     |
| User & Role Management    | Admin Users                      |

These pages should form the initial design and development priority.

---

# 58. Suggested Initial Sitemap

```text
Public
├── /
├── /jobs
├── /jobs/:id
├── /signin
└── /signup

Job Seeker
├── /jobs
├── /jobs/:id
├── /applications
├── /profile
├── /profile/edit
└── /settings
    ├── /account
    ├── /privacy
    └── /appearance

Recruiter
├── /recruiter
├── /recruiter/jobs
├── /recruiter/jobs/new
├── /recruiter/jobs/:id
├── /recruiter/jobs/:id/applicants
├── /candidates
├── /candidates/:id
└── /saved-searches

Administrator
├── /admin
├── /admin/users
└── /admin/roles
```

---

# 59. Priority Screens for Initial Design

Before implementing the entire application, the team should design these screens first:

1. Job discovery
2. Job detail
3. Job seeker profile
4. Applications dashboard
5. Recruiter candidate search
6. Candidate profile/application review
7. Recruiter job management
8. Create/edit job
9. Admin user management
10. Mobile job discovery

These screens represent most of the core design patterns needed elsewhere.

---

# 60. Final Design Standard

When reviewing a new Seekr interface, ask:

**Is it immediately understandable?**

**Does it look like the rest of Seekr?**

**Is the most important action obvious?**

**Could anything be removed without hurting usability?**

**Does this work in both light and dark mode?**

**Does it work without relying on color alone?**

**Would both a job seeker and recruiter understand the terminology?**

**Does the interface feel professional without feeling corporate or intimidating?**

**Does the design help the user complete a task rather than simply look visually impressive?**

If the answer to any of these questions is no, the interface should be reconsidered before implementation.

---

# 61. Page Header Standard

Most authenticated pages should use a consistent page-header structure.

```text
------------------------------------------------------------

Jobs                                      [Optional Action]

Find opportunities that match what
you're looking for.

------------------------------------------------------------
```

The page header consists of:

1. Page title
2. Optional one-line description
3. Optional primary action
4. Content below

Examples:

```text
Jobs

Find opportunities that match your skills and preferences.
```

```text
Applications

Keep track of every opportunity you've applied to.
```

```text
Candidates                                   [Save search]

Find candidates for your open roles.
```

```text
Your jobs                                    [Post a job]

Create and manage your active job postings.
```

Do not create oversized dashboard-style headers for ordinary pages.

---

# 62. Navbar Specification

The top navigation should be one of the most consistent elements in Seekr.

Suggested dimensions:

```css
height: 64px;
border-bottom: 1px solid var(--border);
background: var(--background);
```

Example:

```text
┌───────────────────────────────────────────────────────────────┐
│ Seekr     Jobs    Applications                    Search  PB  │
└───────────────────────────────────────────────────────────────┘
```

Recruiter:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Seekr    Jobs    Candidates    Applications    Saved       Search  PB │
└────────────────────────────────────────────────────────────────────────┘
```

The active navigation item should be visually distinguishable but subtle.

For example:

```text
Jobs
────
```

or a slightly stronger text color/background.

Avoid large colored navigation pills for every link.

---

# 63. Logo Direction

The Seekr wordmark should initially remain typography-focused.

Recommended:

```text
Seekr
```

Rather than creating a complicated logo during early development, use a strong wordmark with carefully selected typography.

Potential future icon concepts may explore:

* search
* discovery
* connection
* pathways
* location
* matching

However, the logo should avoid obvious clichés such as:

* magnifying glass + briefcase
* handshake icons
* graduation caps
* generic people icons

The interface should not depend on having a complex logo.

---

# 64. Authentication

Authentication screens should be extremely minimal.

Example:

```text
                         Seekr


                  Welcome back

             Sign in to your account.

          ┌───────────────────────────┐
          │ Email                     │
          └───────────────────────────┘

          ┌───────────────────────────┐
          │ Password                  │
          └───────────────────────────┘

          [        Sign in          ]

              Forgot password?

        New to Seekr? Create an account.
```

Sign-up should ask the user which role they are creating.

```text
How will you use Seekr?

┌────────────────────────────┐
│ I'm looking for work       │
│ Create a job seeker profile│
└────────────────────────────┘

┌────────────────────────────┐
│ I'm hiring                 │
│ Create a recruiter account │
└────────────────────────────┘
```

Role selection should use descriptive text rather than requiring users to understand internal terminology.

---

# 65. Job Seeker Onboarding

Profile creation should not initially present one enormous form.

Use a short multi-step flow.

Suggested sequence:

```text
1. Basics
2. Education
3. Experience
4. Skills
5. Links
6. Preferences
```

Example:

```text
Create your profile

Step 2 of 6

Education

School
[Georgia Institute of Technology          ]

Degree
[Bachelor's                               ]

Field of study
[Computer Science                         ]

Graduation
[May 2029                                 ]

[Back]                              [Continue]
```

Users should be able to return and edit information later.

Avoid making every profile field mandatory.

---

# 66. Profile Completion

Profile completion can be communicated subtly.

Example:

```text
Your profile

Profile strength

████████████████░░░░  80%

Add work experience to help recruiters
understand your background.

[Add experience]
```

Avoid gamifying profile completion with:

* points
* streaks
* trophies
* confetti
* levels

The purpose is to help users understand what information is missing.

---

# 67. Recruiter Onboarding

Recruiters should provide enough organizational context to establish trust.

Potential fields:

```text
Name
Company
Role
Company website
Work email
```

After onboarding, recruiters should be directed toward their highest-value action:

```text
Post your first job
```

or

```text
Find candidates
```

---

# 68. Job Posting Form

Creating a job should use clear sections.

```text
Post a job

Basic information
------------------------------------------------

Job title
[Software Engineer Intern                  ]

Company
[Seekr                                     ]

Location
[Atlanta, GA                               ]

Work model
( ) On-site
( ) Hybrid
( ) Remote


Role details
------------------------------------------------

Employment type
[Internship                                ]

Description
[                                           ]
[                                           ]

Required skills
[Python ×] [React ×] [+ Add skill]


Compensation
------------------------------------------------

Minimum
[$30/hr]

Maximum
[$45/hr]


Additional details
------------------------------------------------

Visa sponsorship
[Available                                  ]

                                    [Save draft]
                                    [Publish job]
```

Long forms should be divided into logical sections instead of placing every field inside individual cards.

---

# 69. Job Search Result Layout

Desktop job search should consider a split-view interaction.

```text
┌───────────────────────────────────────────────────────────────────────┐
│ Search jobs                                                          │
│                                                                       │
│ [Software Engineer             ] [Atlanta        ] [Search]          │
│                                                                       │
│ [Remote] [Salary] [Experience] [Visa] [More filters]                 │
├─────────────────────────────────┬─────────────────────────────────────┤
│                                 │                                     │
│ 247 jobs                        │ Software Engineer Intern             │
│                                 │ Acme                                │
│ Software Engineer Intern        │                                     │
│ Acme                            │ Atlanta · Hybrid                     │
│ Atlanta · Hybrid               │ $35–45/hr                           │
│                                 │                                     │
│ Python  React  AWS             │ [Apply] [Save]                      │
│                                 │                                     │
│ -----------------------------   │ About the role                      │
│                                 │                                     │
│ Backend Engineer Intern         │ ...                                 │
│ Example Co.                     │                                     │
│ Remote                          │                                     │
│                                 │                                     │
└─────────────────────────────────┴─────────────────────────────────────┘
```

This allows users to inspect jobs without repeatedly navigating backward.

On smaller screens, job results and details should become separate views.

---

# 70. Search Result Selection

When a result is selected:

```text
border-color: var(--border-strong);
background: var(--surface-secondary);
```

Selection should not rely on a bright accent border.

The interface should remain calm even during interaction.

---

# 71. Salary Display

Compensation should be displayed consistently.

Examples:

```text
$35–45/hr

$80K–$105K

$95,000/year
```

Avoid:

```text
Competitive
Great salary
Excellent compensation
```

unless that is literally the information provided by the employer.

If compensation is unavailable:

```text
Salary not listed
```

is preferable to hiding the field in contexts where users expect it.

---

# 72. Remote and Location Information

Location should follow predictable patterns.

Examples:

```text
Atlanta, GA · On-site

New York, NY · Hybrid

Remote · United States

Remote
```

Avoid creating separate brightly colored badges for every location attribute.

---

# 73. Visa Sponsorship

Visa sponsorship is an important filter and should be represented clearly.

Possible values:

```text
Sponsorship available

No sponsorship

Sponsorship status not provided
```

Avoid ambiguous labels such as:

```text
Visa friendly
```

unless the platform clearly defines what that means.

---

# 74. Application Timeline

Application tracking should visually communicate progression.

Example:

```text
Applied            Review            Interview           Offer
   ●────────────────●──────────────────○───────────────────○

Sep 18             Sep 20
```

Completed stages:

```text
●
```

Future stages:

```text
○
```

Closed applications should explicitly state:

```text
Application closed
```

rather than attempting to represent closure as another positive progression stage.

---

# 75. Recruiter Application Review

Application review should combine the candidate and application into one workspace.

```text
Applicants / Software Engineer Intern

┌──────────────────────┬─────────────────────────────────────────────┐
│                      │                                             │
│ 124 applicants       │ Jordan Lee                                 │
│                      │ CS @ Georgia Tech                          │
│ Jordan Lee           │ Atlanta, GA                               │
│ Maya Patel           │                                             │
│ Alex Morgan          │ Python  React  AWS                         │
│ Chris Chen           │                                             │
│ Taylor Smith         │ [Move to Interview] [More]                 │
│                      │                                             │
│                      │ Application                                 │
│                      │ Applied Sep 20                             │
│                      │                                             │
│                      │ Note                                        │
│                      │ I'm particularly interested in...           │
│                      │                                             │
│                      │ Experience                                  │
│                      │ ...                                         │
└──────────────────────┴─────────────────────────────────────────────┘
```

Recruiters should be able to move between candidates quickly without losing context.

---

# 76. Recruiter Candidate Filters

Candidate filters may include:

```text
Skills
Location
School
Graduation year
Experience
Projects
Availability
```

The first release should prioritize filters directly connected to the required user stories.

Avoid adding filters simply because candidate data exists.

---

# 77. Saved Search Interaction

After applying filters:

```text
Python ×
AWS ×
Atlanta ×
2027–2029 graduation ×

                         [Save search]
```

Clicking `Save search`:

```text
Save this search

Name
[Atlanta Python candidates             ]

Notify me about new matches

[x] Email notifications
[x] In-app notifications

Cancel                         Save search
```

The saved search should preserve the exact filter state.

---

# 78. Recommendations

Recommendation sections should remain secondary to explicit search.

Example:

```text
Recommended candidates

Based on the requirements for
Software Engineer Intern.

------------------------------------------------

Jordan Lee
Computer Science · Georgia Tech

Python    React    AWS

Matches 4 required skills
Atlanta, GA · Open to hybrid

[View profile]
```

Recommendations should never obscure why the candidate appeared.

---

# 79. Notification System

Seekr may eventually contain an in-app notification center.

Example:

```text
Notifications

Today

Your application moved to Interview
Software Engineer Intern · Acme
2h

A new candidate matches your saved search
Backend interns — Atlanta
4h
```

Notification categories could include:

Job seeker:

```text
Application updates
Saved job updates
Platform messages
```

Recruiter:

```text
New applications
Candidate matches
Saved search alerts
```

---

# 80. Notification Badge

Unread notifications may use a small indicator.

Example:

```text
Notifications  •
```

Avoid aggressive counters unless the number itself provides useful information.

---

# 81. User Menu

Clicking the avatar should open:

```text
Prithul Baveja
prithul@example.com

View profile
Settings
Appearance

----------------

Sign out
```

Recruiters may additionally have:

```text
Company profile
```

The menu should remain compact.

---

# 82. Appearance Settings

Example:

```text
Appearance

Theme

○ Light

○ Dark

● System
```

Theme changes should occur immediately.

---

# 83. Settings Architecture

Settings should use a simple secondary navigation.

```text
Settings

Account
Profile
Privacy
Notifications
Appearance
```

Desktop:

```text
┌──────────────────┬────────────────────────────────────┐
│ Account          │                                    │
│ Profile          │ Privacy                            │
│ Privacy          │                                    │
│ Notifications    │ Control who can discover and       │
│ Appearance       │ view your profile.                 │
│                  │                                    │
└──────────────────┴────────────────────────────────────┘
```

Mobile should collapse this into separate pages or tabs.

---

# 84. Destructive Actions

Destructive actions should:

1. use explicit language
2. explain consequences
3. require confirmation when irreversible

Example:

```text
Delete job posting?

Software Engineer Intern will be permanently
removed. Existing applicants will no longer
be accessible through this posting.

Cancel                          Delete job
```

Avoid confirmation dialogs that only say:

```text
Are you sure?
```

---

# 85. Tables

Tables should be used when users need to compare structured records.

Good uses:

* recruiter jobs
* applicants
* admin users
* saved searches

Example:

```text
Role                     Applicants      Status       Updated

Software Engineer        124             Active       Today
ML Engineer               87             Active       Sep 21
Product Designer          42             Paused       Sep 19
```

Rows should have comfortable spacing.

Avoid excessive vertical lines.

Horizontal separators are usually sufficient.

---

# 86. Pagination

Large datasets should use predictable pagination or incremental loading.

Example:

```text
Showing 1–25 of 247

← Previous                         Next →
```

Infinite scrolling should not be the default for recruiter workflows because recruiters may need to maintain their position within a candidate list.

---

# 87. Sorting

Search results should support relevant sorting options.

Jobs:

```text
Sort by: Relevance

Relevance
Newest
Salary: high to low
Salary: low to high
```

Candidates:

```text
Sort by: Relevance

Relevance
Recently active
Recently updated
```

The current sort should always be visible.

---

# 88. Map Markers

Map markers should use simple geometric shapes.

Selected:

```text
●
```

Unselected:

```text
○
```

Clusters may show:

```text
12
```

Do not create elaborate illustrated map pins.

Map interaction should remain secondary to job/candidate information.

---

# 89. Recruiter Applicant Distribution Map

Recruiters may use maps to understand candidate geography.

Example:

```text
Candidate locations

Atlanta          48
New York         27
San Francisco    19
Boston           14
Other            16
```

The map should supplement this information rather than forcing users to interpret geography visually.

---

# 90. Form Validation

Validation should happen as close as possible to the relevant input.

Example:

```text
Company website

[seekr]

Enter a valid URL.
```

Avoid displaying every form error only at the top of the page.

Do not remove user-entered data after a validation error.

---

# 91. Required Fields

Required fields should be clearly identified.

Example:

```text
Job title *
```

Optional fields may explicitly say:

```text
Portfolio URL
Optional
```

Do not make fields required unless the platform genuinely needs the information.

---

# 92. Focus States

Keyboard focus must be obvious.

Example:

```css
outline: 2px solid var(--accent);
outline-offset: 2px;
```

Never globally remove browser focus outlines without providing an accessible replacement.

---

# 93. Hover States

Hover states should be subtle.

Example:

```text
Default:
background: transparent

Hover:
background: var(--surface-hover)
```

Cards should not dramatically lift, scale, rotate, or animate when hovered.

---

# 94. Dark Mode Surface Hierarchy

Dark mode should distinguish surfaces primarily using subtle changes in brightness.

Example:

```text
Page
#111110

Card
#191918

Secondary surface
#222220

Hover
#292927
```

Avoid excessive borders around every dark-mode component.

---

# 95. Responsive Search

Desktop:

```text
[Search jobs........................] [Location........] [Search]
```

Mobile:

```text
[Search jobs........................]

[Location...........................]

[Search]

[Filters (3)]
```

Filters should move into a bottom sheet or dedicated view on smaller screens.

---

# 96. Mobile Job Cards

Mobile cards should prioritize:

```text
Software Engineer Intern
Acme

Atlanta, GA · Hybrid
$35–45/hr

Python   React   AWS

2d ago                              Save
```

Do not attempt to display every desktop field.

---

# 97. Mobile Application Tracking

The application pipeline may become vertically oriented.

```text
● Applied
│ Sep 18
│
● Review
│ Sep 20
│
○ Interview
│
○ Offer
```

This is easier to understand on narrow screens than forcing a horizontal timeline.

---

# 98. Mobile Recruiter Experience

Recruiter functionality should remain usable on mobile but does not need to reproduce every desktop interaction exactly.

For example, the desktop applicant split view:

```text
Applicant list | Candidate details
```

should become:

```text
Applicant list
      ↓
Candidate detail page
```

Mobile should preserve functionality rather than layout.

---

# 99. Accessibility of Maps

Map-based information must always have a non-map alternative.

Users should still be able to discover jobs through:

```text
List view
Search
Filters
Location text
```

No required workflow should depend exclusively on interacting with a map.

---

# 100. Data Privacy Indicators

Whenever privacy-sensitive information appears, Seekr should make visibility understandable.

Example:

```text
Location

Atlanta, GA

Visible to recruiters
```

or:

```text
Phone number

(404) 555-0123

Only visible when you apply
```

Privacy controls should explain outcomes in plain language.

---

# 101. Profile Preview

Job seekers should be able to preview what recruiters see.

Example:

```text
Edit profile                              [Preview as recruiter]
```

The preview should reflect the user's current privacy settings.

This helps make privacy controls tangible rather than abstract.

---

# 102. Company Representation

Jobs should consistently identify the organization behind the posting.

Example:

```text
Software Engineer Intern

Stripe
Atlanta, GA · Hybrid
```

Company logos may supplement company names but should never replace them.

If no logo exists, use a neutral fallback rather than generating random branding.

---

# 103. Avatar System

Candidate avatars should use:

```text
48px     list/card
64px     medium profile preview
96px     full profile
```

If no photo exists, use initials.

Example:

```text
JL
```

Do not use generic silhouette illustrations unless necessary.

---

# 104. Information Priority for Job Cards

Job cards should prioritize:

```text
1. Job title
2. Company
3. Location / work model
4. Compensation
5. Skills
6. Recency
```

Secondary information should not visually compete with the job title.

---

# 105. Information Priority for Candidate Cards

Candidate cards should prioritize:

```text
1. Candidate name
2. Headline / education
3. Location
4. Relevant skills
5. Relevant experience/projects
6. Availability or preferences
```

Avoid reducing candidates to match percentages.

---

# 106. Information Priority for Recruiter Job Cards

Recruiter job management should prioritize:

```text
1. Job title
2. Posting status
3. Applicant count
4. Pipeline activity
5. Last updated
```

---

# 107. Breadcrumbs

Breadcrumbs should only appear when hierarchy becomes deep.

Example:

```text
Jobs / Software Engineer Intern / Applicants
```

Do not add breadcrumbs to simple top-level pages such as:

```text
Jobs
Applications
Profile
```

---

# 108. URL and Browser History

Major interactions should respect browser navigation.

Opening:

```text
/jobs/123
```

should allow users to press Back and return to their previous search with:

* filters preserved
* search query preserved
* scroll position preserved when practical

This is particularly important for search-heavy workflows.

---

# 109. Search Persistence

Navigating into a job or candidate profile should not destroy search state.

For example:

```text
Search:
Python + Atlanta + Internship

→ Open job
→ Back

Search remains:
Python + Atlanta + Internship
```

This behavior should be considered part of the user experience, not merely an implementation detail.

---

# 110. Skeleton Patterns

Skeleton states should approximate actual layouts.

Job:

```text
████████████████████
██████████

████████ · ███████
████████████

██████  ███████  █████
```

Candidate:

```text
██    ███████████████
      █████████

      █████  █████  █████
```

Skeletons should not animate aggressively.

---

# 111. Search Empty State

Example:

```text
No jobs found

We couldn't find jobs matching all of your filters.

Try removing a filter or expanding your location.

[Clear filters]
```

If useful, Seekr may display related results below:

```text
Jobs you may still be interested in
```

but these must be clearly separated from exact search results.

---

# 112. First-Time Empty State

A recruiter with no jobs:

```text
You haven't posted a job yet

Create your first job posting to start
receiving applications.

[Post a job]
```

A job seeker with no applications:

```text
No applications yet

Jobs you apply to will appear here so you
can track their progress.

[Explore jobs]
```

---

# 113. Copy Style

Seekr should use sentence case.

Preferred:

```text
Post a job
Save search
Edit profile
Candidate recommendations
```

Avoid:

```text
Post A Job
SAVE SEARCH
Edit Profile
Candidate Recommendations
```

except where proper nouns require capitalization.

---

# 114. Date Formatting

Recent events may use relative time:

```text
2h ago
Yesterday
3 days ago
```

Older records should use dates:

```text
Sep 18, 2026
```

Application timelines should generally prefer explicit dates because those records may remain relevant for months.

---

# 115. Number Formatting

Use compact numbers only when exact precision is unnecessary.

Example:

```text
1,247 applicants
```

rather than:

```text
1.2K applicants
```

for recruiter management interfaces.

Exact counts are usually more useful.

---

# 116. Design for Trust

Seekr should avoid creating artificial urgency.

Do not use:

```text
ONLY 2 SPOTS LEFT!
APPLY NOW!!!
Trending hot job
87 people viewing this
```

unless such information is accurate, useful, and intentionally part of the product.

The platform should help users make career decisions rather than pressure them.

---

# 117. Recommendation Transparency

When recommending candidates or jobs, Seekr should provide understandable reasons.

Example:

```text
Why this job?

Matches your skills
Python · AWS

Matches your preferences
Atlanta · Hybrid

Internship
```

Recruiter:

```text
Why this candidate?

4 required skills
Python · React · AWS · PostgreSQL

Atlanta, GA

Relevant backend project experience
```

This principle should guide future recommendation features.

---

# 118. Permission-Aware UI

Users should only see controls relevant to their role and permissions.

A job seeker should not see:

```text
Edit posting
Move candidate
Change user role
```

A recruiter should not see administrative actions unless explicitly authorized.

Permission checks must exist in the backend as well; hiding controls in the UI is not sufficient security.

---

# 119. Admin Safety

Administrator actions can have large consequences.

Actions such as:

```text
Suspend user
Change role
Delete account
```

should clearly identify:

* affected user
* action being performed
* consequences

Example:

```text
Suspend Jordan Lee?

Jordan will no longer be able to access Seekr
until the account is restored.

Cancel                            Suspend account
```

---

# 120. Performance Expectations

The design should support perceived speed.

Prioritize fast rendering of:

* navigation
* page structure
* search controls
* existing cached information

Then load:

* search results
* recommendations
* maps
* secondary metadata

Users should not stare at a blank page while one API request completes.

---

# 121. Image Usage

Seekr should use imagery sparingly.

Appropriate:

* candidate avatars
* company logos
* real product screenshots
* optional company imagery

Avoid decorative stock photography such as:

```text
People shaking hands
People pointing at laptops
Generic office teams
Graduation stock photos
```

The product itself should provide most of the visual identity.

---

# 122. Map Loading

Maps can be expensive and slower than ordinary interface components.

The rest of the job discovery page should remain functional while the map loads.

Example:

```text
Job list loads
↓
Map skeleton
↓
Map becomes interactive
```

A failed map should not prevent job discovery.

---

# 123. Accessibility Labels

Icon-only buttons require accessible labels.

Example:

```html
<button aria-label="Save job">
```

Tooltips may visually explain unfamiliar icons but should not replace accessibility labels.

---

# 124. Keyboard Interaction

Core workflows should support keyboard navigation.

Important targets:

* navigation
* search
* filters
* job results
* candidate results
* modals
* dropdowns
* application forms

Search-heavy recruiter workflows particularly benefit from efficient keyboard interaction.

---

# 125. Filter Component Standard

Filters should use predictable components based on data type.

Boolean:

```text
[x] Remote
[x] Visa sponsorship
```

Single selection:

```text
Work type

○ Any
○ Remote
○ Hybrid
○ On-site
```

Multiple selection:

```text
Skills

[x] Python
[x] React
[ ] Java
[ ] Go
```

Range:

```text
Salary

Minimum       Maximum
[$30/hr]      [$50/hr]
```

---

# 126. Filter Count

When filters collapse:

```text
Filters (3)
```

The count represents active filters, not available filters.

This is especially useful on mobile.

---

# 127. Tooltips

Tooltips should explain unfamiliar concepts.

Appropriate:

```text
Visa sponsorship ⓘ
```

Tooltip:

```text
Whether the employer indicates they may
sponsor employment authorization.
```

Do not hide essential information exclusively inside tooltips.

---

# 128. Dropdowns

Dropdown menus should:

* open near their trigger
* remain visually compact
* close on outside click
* support keyboard navigation
* clearly indicate selection

Example:

```text
Sort by: Relevance

┌──────────────────┐
│ ✓ Relevance      │
│   Newest         │
│   Salary: high   │
│   Salary: low    │
└──────────────────┘
```

---

# 129. Tabs

Tabs should be used for closely related views.

Example:

```text
Applications

All     Applied     Review     Interview     Offer     Closed
───
```

Avoid using tabs as primary navigation across unrelated areas of the application.

---

# 130. Cards

Cards should not be the default container for everything.

Use cards when a group of information behaves as one selectable or meaningful object.

Good:

```text
Job result
Candidate result
Saved search
Recommendation
```

Avoid:

```text
Page title inside card
Filters inside card
Every profile section inside a separate floating card
Navigation inside card
```

Flat page sections with whitespace and dividers are often preferable.

---

# 131. Dividers

Use subtle horizontal dividers:

```css
border-color: var(--border);
```

Dividers help separate information without introducing additional containers.

This supports Seekr's minimal visual language.

---

# 132. Sidebar Usage

Although Seekr's primary navigation is top-based, secondary sidebars may be used inside complex pages.

Appropriate:

```text
Settings navigation
Applicant list
Filter panel
Admin sections
```

The sidebar should support the task rather than replace the global top navigation.

---

# 133. Search Architecture

Search should conceptually follow:

```text
Query
+
Filters
+
Sort
=
Results
```

Each part should remain independently understandable.

Example:

```text
Query:
"Software Engineer"

Filters:
Atlanta
Internship
Hybrid

Sort:
Newest
```

This state should ideally be represented in the URL.

---

# 134. Job Search Map Mode

The user should be able to switch between:

```text
List
Map
```

Desktop may additionally support:

```text
Split
```

Example:

```text
[List] [Map]

or

[List] [Split] [Map]
```

The simplest implementation should be selected for the first release.

---

# 135. Map Search Behavior

Moving the map should not unexpectedly replace search results.

A familiar pattern may be used:

```text
[Search this area]
```

after the user moves the map.

This gives the user control over when geography changes their search.

---

# 136. Saved Jobs

Even though saved jobs are not required in the initial stories, the interface should leave room for the pattern.

Job actions should consistently reserve secondary space for:

```text
Save
```

This prevents future functionality from requiring major redesign.

---

# 137. Application Notes

The tailored application note should be intentionally lightweight.

Recommended:

```text
Optional note

Share why you're interested or anything you'd
like the recruiter to know.

0 / 500

[                                              ]
[                                              ]
```

A reasonable character limit prevents the field from turning into a second cover letter system.

---

# 138. Application Confirmation

After submitting:

```text
Application submitted

Your application for Software Engineer Intern
at Acme has been sent.

[View application]     [Keep exploring]
```

Avoid unnecessary celebratory animations.

The moment should feel positive but professional.

---

# 139. Recruiter Status Changes

Changing an application status should be straightforward.

Example:

```text
Status

[Interview        ▾]
```

Changing the value may show:

```text
Candidate moved to Interview.
```

Important status transitions may require confirmation if they trigger external communication.

---

# 140. Candidate Search Map

If candidate geography is shown, exact home locations should never be implied by the visual design.

Use city/region-level information where appropriate.

Example:

```text
Atlanta, GA
```

not a precise residential marker.

Candidate privacy settings should determine whether location information is visible.

---

# 141. Design Tokens — Extended

Recommended implementation:

```css
:root {
  /* Background */
  --background: #FAF9F7;

  /* Surfaces */
  --surface: #FFFFFF;
  --surface-secondary: #F5F3F0;
  --surface-hover: #F1EFEC;

  /* Text */
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-muted: #78716C;
  --text-disabled: #A8A29E;

  /* Borders */
  --border: #E7E5E4;
  --border-strong: #D6D3D1;

  /* Brand */
  --accent: #2563EB;
  --accent-hover: #1D4ED8;
  --accent-subtle: #EFF6FF;

  /* Semantic */
  --success: #15803D;
  --warning: #B45309;
  --danger: #B91C1C;
  --info: #0369A1;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Layout */
  --content-width: 1200px;
  --reading-width: 760px;

  /* Navigation */
  --nav-height: 64px;
}
```

Dark theme:

```css
[data-theme="dark"] {
  --background: #111110;

  --surface: #191918;
  --surface-secondary: #222220;
  --surface-hover: #292927;

  --text-primary: #FAFAF9;
  --text-secondary: #D6D3D1;
  --text-muted: #A8A29E;
  --text-disabled: #78716C;

  --border: #302F2D;
  --border-strong: #44403C;

  --accent: #60A5FA;
  --accent-hover: #93C5FD;
  --accent-subtle: #172554;
}
```

---

# 142. Suggested Frontend Design Stack

The exact technology is an implementation decision, but a modern Seekr frontend could use:

```text
React
TypeScript
Tailwind CSS
Lucide Icons
```

A component library may be used as a foundation, but its default appearance should be adapted to the Seekr design system.

Do not allow a component library to define the visual identity of the product.

Seekr should still look like Seekr.

---

# 143. Component Naming

Components should use semantic names.

Preferred:

```text
JobCard
CandidateCard
ApplicationTimeline
SearchFilters
ProfileHeader
StatusBadge
```

Avoid:

```text
BlueCard
BigBox
Container2
LeftThing
InfoThing
```

Names should describe responsibility rather than appearance.

---

# 144. Component Variants

Shared components should support controlled variants.

Example:

```text
Button

variant:
primary
secondary
ghost
destructive

size:
small
medium
large
```

Avoid creating:

```text
BlueButton
WhiteButton
DeleteButton
BigButton
NavbarButton
```

as unrelated implementations.

---

# 145. Responsive Component Behavior

Components should define how they behave at different sizes.

For example:

```text
JobCard

Desktop:
full metadata

Tablet:
reduced metadata

Mobile:
essential metadata only
```

Responsive design should not be treated as a final cleanup step.

---

# 146. Design Review Checklist

Before merging a frontend feature, verify:

* Does it use existing design tokens?
* Does it reuse existing components?
* Does it work in light mode?
* Does it work in dark mode?
* Does it work on mobile?
* Does it have hover states?
* Does it have keyboard focus states?
* Does it handle loading?
* Does it handle empty data?
* Does it handle errors?
* Is text readable and concise?
* Are destructive actions clear?
* Is important information accessible without color?
* Does the page maintain Seekr's visual hierarchy?
* Are there unnecessary cards or containers?
* Are there unnecessary animations?
* Are there arbitrary colors or spacing values?

---

# 147. Feature Design Review

Before implementing a new feature, answer:

```text
Who is using this?

What are they trying to accomplish?

What information do they need?

What is the primary action?

What is secondary?

What happens when there is no data?

What happens when something fails?

What happens on mobile?

What information is private?

Does this pattern already exist elsewhere in Seekr?
```

The team should answer these questions before designing a new interaction from scratch.

---

# 148. Client / Mentor Feedback

Seekr is being developed for a client, so this document should guide the product rather than prevent iteration.

When mentor or client feedback changes a design decision:

1. Understand the underlying usability concern.
2. Determine whether the change affects a reusable pattern.
3. Update the relevant design component.
4. Apply the updated pattern consistently.
5. Update this document if the change affects the design system.

Avoid fixing feedback on only one screen when the issue exists throughout the product.

---

# 149. Design Consistency Rule

When two interfaces solve the same problem, they should generally use the same interaction.

Examples:

Job search:

```text
Search
Filters
Sort
Results
```

Candidate search:

```text
Search
Filters
Sort
Results
```

Job status:

```text
StatusBadge
```

Application status:

```text
StatusBadge
```

Profile skills:

```text
SkillTag
```

Job skills:

```text
SkillTag
```

Consistency reduces both user confusion and engineering complexity.

---

# 150. Seekr's Visual Signature

Seekr should become recognizable through restraint rather than decoration.

Its visual signature should come from:

```text
Warm neutral backgrounds
Strong typography
Generous whitespace
Thin borders
Small-radius components
Restrained blue accent
Clear information hierarchy
Minimal iconography
Fast interactions
Consistent search experiences
```

No individual effect should dominate the product.

The entire system should feel intentionally composed.

---

# 151. Product Personality in Practice

A Seekr page should feel closer to:

```text
A polished productivity tool
```

than:

```text
A traditional job board
```

Closer to:

```text
Notion / Linear / Stripe-level restraint
```

than:

```text
A generic SaaS dashboard template
```

Closer to:

```text
Professional network + recruiting workspace
```

than:

```text
Social media
```

---

# 152. Final Visual Rule

When choosing between two designs, prefer the one with:

```text
less decoration
clearer hierarchy
fewer colors
fewer containers
better spacing
stronger typography
more obvious interactions
```

Do not add visual elements merely because a page feels empty.

Whitespace is part of the design.

---

# 153. Seekr Design Summary

Seekr is a modern recruiting platform built equally for job seekers and recruiters.

The interface should be:

**Minimal, but not empty.**

**Professional, but not corporate.**

**Friendly, but not playful.**

**Information-rich, but not overwhelming.**

**Modern, but not trend-dependent.**

The Seekr design language consists of:

```text
Warm neutral surfaces
+
Strong typography
+
Subtle borders
+
Generous whitespace
+
Restrained blue accents
+
Consistent reusable components
+
Clear search and discovery experiences
```

The product should avoid relying on visual gimmicks.

No gradients.

No emojis as interface elements.

No excessive shadows.

No unnecessary glass effects.

No excessive animation.

No random colors.

No unnecessary cards.

No clutter.

Every element should either communicate information, establish hierarchy, or help the user take an action.

That principle should guide every future Seekr design decision.
