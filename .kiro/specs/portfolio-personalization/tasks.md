# Implementation Plan: Portfolio Personalization

## Overview

This implementation plan transforms the Oyin's Journey portfolio into a fully personalized, admin-managed professional showcase. Tasks are organized to deliver immediate UI improvements first, followed by admin portal infrastructure.

## Tasks

- [x] 1. Update Health Dashboard - Remove deployment info and simplify
  - [x] 1.1 Remove deployment info section from HealthDashboard.tsx
    - Remove the "Deployment Info" card entirely
    - Remove environment and region display
    - _Requirements: 6.1, 6.2, 6.3_
  - [x] 1.2 Rename "Infrastructure" to "Technology" in HealthDashboard.tsx
    - Update section title and any references
    - _Requirements: 6.4_
  - [x] 1.3 Improve error handling to show graceful fallback
    - Remove "Network Error" display
    - Show user-friendly status messages
    - _Requirements: 6.6_
  - [ ]* 1.4 Write property test for Health Dashboard content exclusion
    - **Property 8: Health Dashboard Content Exclusion**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [x] 2. Update Projects Section - Conditional links and honest tagline
  - [x] 2.1 Update projects tagline to be more accurate
    - Change from "No screenshots, no claims..." to something honest
    - _Requirements: 9.1_
  - [x] 2.2 Ensure project buttons are conditional based on data
    - Repo button only shows when repositoryUrl exists
    - Demo button only shows when demoUrl/live_url exists
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [ ]* 2.3 Write property test for project links conditional display
    - **Property 7: Project Links Conditional Display**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 9.2, 9.4**

- [x] 3. Update Certifications Section - Add Credly integration
  - [x] 3.1 Add Credly verification URL support to certifications
    - Update certification interface to include credlyUrl
    - Update "Verify Credential" button to link to Credly
    - _Requirements: 4.1, 4.2_
  - [x] 3.2 Make Credly button conditional
    - Only show verify button when credlyUrl exists
    - _Requirements: 4.3_
  - [x] 3.3 Add Credly badge image display
    - Show badge image when badgeUrl is available
    - _Requirements: 4.5_
  - [ ]* 3.4 Write property test for Credly integration display
    - **Property 6: Credly Integration Conditional Display**
    - **Validates: Requirements 4.1, 4.3, 4.5**

- [x] 4. Update Header - Make buttons functional
  - [x] 4.1 Make "Source" button link to GitHub repository
    - Link to https://github.com/oyindamola-oladipo/oyins-journey
    - Open in new tab
    - _Requirements: 7.1_
  - [x] 4.2 Make "Live API" button link to API endpoint
    - Link to API documentation or base URL
    - Open in new tab
    - _Requirements: 7.2_

- [x] 5. Update Footer - Add social links
  - [x] 5.1 Add social link icons to footer
    - Add LinkedIn, GitHub, and email icons
    - Use same social links as HeroSection
    - _Requirements: 10.1, 10.2, 10.3_
  - [ ]* 5.2 Write property test for social links display
    - **Property 4: Social Links Conditional Display**
    - **Validates: Requirements 3.2, 3.3, 10.1, 10.4**

- [x] 6. Checkpoint - Verify all UI updates work correctly
  - Ensure all frontend changes render correctly
  - Test conditional rendering with various data states
  - Ask the user if questions arise

- [ ] 7. Create Site Configuration infrastructure
  - [ ] 7.1 Create site-config DynamoDB table schema
    - Store social links, branding, source/API URLs
    - _Requirements: 3.1_
  - [ ] 7.2 Create API endpoint for site configuration
    - GET /config for public access
    - PUT /admin/config for admin updates
    - _Requirements: 3.1, 3.2_
  - [ ] 7.3 Update frontend to fetch social links from config
    - Replace hardcoded social links with API data
    - _Requirements: 3.2, 3.3, 3.4_
  - [ ]* 7.4 Write property test for URL validation
    - **Property 5: URL Validation**
    - **Validates: Requirements 3.5**

- [ ] 8. Set up Amazon Cognito authentication
  - [ ] 8.1 Create Cognito User Pool via Terraform
    - Configure user pool with email sign-in
    - Set up app client for admin portal
    - _Requirements: 1.1, 1.5_
  - [ ] 8.2 Create authentication service in frontend
    - Implement sign-in, sign-out, session management
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - [ ] 8.3 Create protected admin route
    - Redirect unauthenticated users to login
    - _Requirements: 1.1, 1.3_
  - [ ]* 8.4 Write property test for authentication access control
    - **Property 1: Authentication Access Control**
    - **Validates: Requirements 1.1, 1.3**

- [ ] 9. Create Admin Portal UI
  - [ ] 9.1 Create admin dashboard layout
    - Navigation for content types (certifications, skills, projects)
    - Overview statistics
    - _Requirements: 1.2_
  - [ ] 9.2 Create certification management forms
    - Add/edit/delete certifications
    - Include Credly URL field
    - _Requirements: 2.1, 4.4_
  - [ ] 9.3 Create skill management forms
    - Add/edit/delete skills
    - _Requirements: 2.2_
  - [ ] 9.4 Create project management forms
    - Add/edit/delete projects
    - Optional repo and demo URL fields
    - _Requirements: 2.3_
  - [ ] 9.5 Create social links configuration form
    - Edit LinkedIn, GitHub, email links
    - URL validation feedback
    - _Requirements: 3.1, 3.5_
  - [ ]* 9.6 Write property test for content CRUD operations
    - **Property 2: Content CRUD Round-Trip**
    - **Validates: Requirements 2.1, 2.2, 2.4, 2.5**
  - [ ]* 9.7 Write property test for optional project fields
    - **Property 3: Optional Project Fields Handling**
    - **Validates: Requirements 2.3**

- [ ] 10. Implement visitor analytics
  - [ ] 10.1 Create analytics tracking service
    - Record page views anonymously
    - No PII collection
    - _Requirements: 8.1, 8.4_
  - [ ] 10.2 Create analytics dashboard in admin portal
    - Display page views, unique visitors, popular sections
    - _Requirements: 8.2, 8.3_
  - [ ]* 10.3 Write property test for analytics privacy
    - **Property 10: Analytics Privacy Compliance**
    - **Validates: Requirements 8.4**

- [ ] 11. Final checkpoint - Ensure all features work
  - Verify admin portal authentication works
  - Test content management end-to-end
  - Verify analytics tracking
  - Ensure all tests pass

## Notes

- Tasks 1-6 focus on immediate UI improvements (can be done without backend changes)
- Tasks 7-10 require infrastructure changes (Cognito, DynamoDB)
- Tasks marked with `*` are optional property tests
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation

## Out-of-the-Box Feature Suggestions

Based on your request, here are additional features you could add:

1. **Contact Form** - Allow visitors to send messages (use AWS SES)
2. **Resume Download** - PDF download of your CV
3. **Blog Section** - Share technical articles (could use markdown files or CMS)
4. **Testimonials** - Display recommendations from colleagues
5. **Timeline/Journey** - Visual career progression
6. **GitHub Activity Feed** - Show recent commits/contributions
7. **Skills Radar Chart** - Visual representation of skill levels
8. **Dark/Light Theme Toggle** - User preference for theme
9. **Newsletter Signup** - Build an email list (use AWS SES + DynamoDB)
10. **Project Case Studies** - Detailed write-ups for key projects
