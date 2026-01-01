# Requirements Document

## Introduction

Comprehensive personalization of Oyin's Journey portfolio website to transform it from a generic CV-as-API template into a fully personalized, admin-managed professional showcase. This includes an admin portal with Amazon Cognito authentication, visitor analytics, configurable social links, Credly certification verification, and enhanced UI/UX improvements.

## Glossary

- **Admin_Portal**: Secure interface for managing portfolio content (certifications, skills, projects, social links)
- **Cognito_Auth**: Amazon Cognito authentication service for admin access
- **Visitor_Analytics**: System for tracking and displaying website visitor statistics
- **Social_Links_Manager**: Component for managing and displaying configurable social media links
- **Credly_Integration**: Integration with Credly for certification verification links
- **Technology_Stack**: Display of technologies used (renamed from Infrastructure)
- **Health_Dashboard**: System observability component (simplified, without deployment info)

## Requirements

### Requirement 1: Admin Portal Authentication

**User Story:** As the portfolio owner, I want a secure admin portal with Cognito authentication, so that only I can manage my portfolio content.

#### Acceptance Criteria

1. WHEN accessing the admin portal, THE System SHALL require Amazon Cognito authentication
2. WHEN authenticated successfully, THE Admin_Portal SHALL display the content management dashboard
3. WHEN authentication fails, THE System SHALL display an appropriate error message and deny access
4. WHEN the session expires, THE System SHALL redirect to the login page
5. THE System SHALL use Cognito's pay-as-you-go pricing (first 50K MAUs free)

### Requirement 2: Content Management

**User Story:** As the portfolio owner, I want to manage all portfolio content through the admin portal, so that changes reflect immediately on the public site.

#### Acceptance Criteria

1. WHEN adding a new certification, THE Admin_Portal SHALL save it to DynamoDB and display it on the public site
2. WHEN adding a new skill, THE Admin_Portal SHALL save it to DynamoDB and display it on the public site
3. WHEN adding a new project, THE Admin_Portal SHALL allow specifying optional repo and demo URLs
4. WHEN modifying existing content, THE Admin_Portal SHALL update DynamoDB and reflect changes immediately
5. WHEN deleting content, THE Admin_Portal SHALL remove it from DynamoDB and the public site

### Requirement 3: Social Links Management

**User Story:** As the portfolio owner, I want to configure my social media links through the admin portal, so that visitors can connect with me on various platforms.

#### Acceptance Criteria

1. WHEN configuring social links, THE Admin_Portal SHALL allow setting LinkedIn, GitHub, and email links
2. WHEN social links are configured, THE System SHALL display them in the header, hero section, and footer
3. WHEN a social link is not configured, THE System SHALL hide that specific link icon
4. WHEN clicking a social link, THE System SHALL open the configured URL in a new tab
5. THE System SHALL validate URL formats before saving social links

### Requirement 4: Credly Certification Integration

**User Story:** As a visitor, I want to verify certifications through Credly, so that I can confirm the portfolio owner's credentials.

#### Acceptance Criteria

1. WHEN displaying certifications, THE System SHALL show a "Verify on Credly" button for each certification
2. WHEN clicking the verify button, THE System SHALL open the Credly verification page in a new tab
3. WHEN a certification has no Credly URL, THE System SHALL hide the verify button for that certification
4. WHEN adding certifications via admin, THE Admin_Portal SHALL allow specifying the Credly verification URL
5. THE System SHALL display the Credly badge image when available

### Requirement 5: Project Links Enhancement

**User Story:** As a visitor, I want to access project repositories and demos when available, so that I can explore the portfolio owner's work.

#### Acceptance Criteria

1. WHEN a project has a repository URL, THE System SHALL display a "Repo" button
2. WHEN a project has no repository URL, THE System SHALL hide the "Repo" button
3. WHEN a project has a demo/live URL, THE System SHALL display a "Demo" button
4. WHEN a project has no demo URL, THE System SHALL hide the "Demo" button
5. WHEN clicking project buttons, THE System SHALL open the respective URLs in new tabs

### Requirement 6: Health Dashboard Simplification

**User Story:** As a visitor, I want to see the technology stack and system health without unnecessary deployment details, so that I can understand the technical implementation.

#### Acceptance Criteria

1. THE Health_Dashboard SHALL NOT display environment information (production/staging)
2. THE Health_Dashboard SHALL NOT display region information (us-east-1)
3. THE Health_Dashboard SHALL NOT display deployment info section
4. THE Health_Dashboard SHALL rename "Infrastructure" to "Technology"
5. THE Health_Dashboard SHALL display technology stack (AWS Lambda, DynamoDB, CloudFront, CloudWatch)
6. WHEN the API is unavailable, THE Health_Dashboard SHALL show graceful fallback without "Network Error" messages

### Requirement 7: Header and Navigation Enhancement

**User Story:** As a visitor, I want functional navigation buttons, so that I can access the source code and live API.

#### Acceptance Criteria

1. WHEN clicking "Source" button, THE System SHALL open the GitHub repository in a new tab
2. WHEN clicking "Live API" button, THE System SHALL open the API documentation or endpoint
3. THE Header SHALL display the portfolio owner's branding (oyin.journey)
4. THE Header SHALL include navigation links to all main sections

### Requirement 8: Visitor Analytics

**User Story:** As the portfolio owner, I want to track visitor statistics, so that I can understand my portfolio's reach and engagement.

#### Acceptance Criteria

1. WHEN a visitor accesses the site, THE System SHALL record the visit anonymously
2. WHEN accessing the admin portal, THE Admin_Portal SHALL display visitor statistics
3. THE Analytics SHALL track page views, unique visitors, and popular sections
4. THE Analytics SHALL respect visitor privacy (no PII collection)
5. THE System SHALL use a lightweight analytics solution (e.g., simple CloudWatch metrics or Plausible)

### Requirement 9: Projects Section Enhancement

**User Story:** As a visitor, I want an honest description of projects, so that I understand what evidence is available.

#### Acceptance Criteria

1. THE Projects_Section SHALL update the tagline to be more accurate (not all projects have live demos)
2. WHEN displaying projects, THE System SHALL show available evidence links based on actual data
3. THE Projects_Section SHALL display project status (active, completed, in-progress)
4. WHEN a project has no external links, THE System SHALL still display the project with description only

### Requirement 10: Footer Enhancement

**User Story:** As a visitor, I want to see social links and contact information in the footer, so that I can connect with the portfolio owner.

#### Acceptance Criteria

1. THE Footer SHALL display configured social links (LinkedIn, GitHub, email)
2. THE Footer SHALL display the portfolio branding
3. THE Footer SHALL display the technology stack used to build the site
4. WHEN social links are not configured, THE Footer SHALL hide those specific icons
