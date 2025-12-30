# ADR-009: Frontend Architecture Decision

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

## Context
Need to choose frontend architecture for Oyin's Journey that balances:
- Professional engineering signal vs pure DevOps minimalism
- Static hosting compatibility (S3 + CloudFront)
- Scalability without rewrite
- Cloud engineer → product engineer brand evolution

## Decision
Implement **React + TypeScript + Vite** with **shadcn/ui + Tailwind** architecture:

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                # shadcn components
│   │   ├── APIExplorer.tsx    # ⭐ interactive API docs
│   │   ├── HealthDashboard.tsx # ops maturity signal
│   │   ├── HeroSection.tsx    # terminal animation
│   │   └── SkillsSection.tsx  # queryable interface
│   ├── services/
│   │   └── api.ts             # real backend calls
│   ├── hooks/
│   │   └── useApi.ts          # reusable logic
│   └── types/
│       └── index.ts           # API contracts
├── living-cv.html             # fallback static version
└── package.json               # modern tooling
```

## Rationale

### ✅ **Engineering Signal Amplification**
- **Clear separation of concerns**: components/services/hooks/types
- **Scalable React architecture**: Textbook structure recruiters recognize
- **TypeScript contracts**: Shows API-first thinking
- **Modern tooling**: Vite + Tailwind = current best practices

### ✅ **Unique Differentiators**
- **APIExplorer.tsx**: Turns frontend into interactive API documentation
- **HealthDashboard.tsx**: Subtle but powerful ops thinking signal
- **Terminal animation**: Engaging developer experience
- **Queryable skills**: Database-like interface shows data modeling

### ✅ **Static Hosting Optimized**
- **No runtime dependencies**: shadcn/ui is copy-paste components
- **Static build output**: Perfect for S3 + CloudFront
- **Free-tier safe**: No server requirements
- **Fallback HTML**: Shows accessibility and failure planning

## Implementation Principles

### 🎯 **API-First Development**
```typescript
// Define contracts BEFORE UI
interface Skill {
  skill_id: string;
  category: 'cloud' | 'devops' | 'backend';
  proficiency: number;
  aws_service?: boolean;
}

// Real backend calls, not mocks
export const getSkills = async (filters: SkillFilters): Promise<Skill[]>
```

### 🎯 **Selective Component Usage**
- Use shadcn/ui **deliberately**, not exhaustively
- Focus on **functionality over aesthetics**
- Remember: **"The system is the product, not the UI"**

### 🎯 **Navigation & UX Fixes**
- Fix hash-based scrolling (currently showing 404)
- Add smooth scroll behavior
- Implement scroll-triggered animations
- Ensure mobile responsiveness

## Technical Specifications

### **Color System**
```css
--primary: hsl(175, 80%, 50%);    /* Cyan accent */
--success: hsl(150, 80%, 45%);    /* Green status */
--background: hsl(220, 20%, 8%);  /* Dark slate */
```

### **Key Components**
- **Header**: Fixed nav with health badge, live clock
- **Hero**: Terminal animation with ambient effects
- **APIExplorer**: 3-column interactive docs
- **SkillsSection**: Query builder interface
- **HealthDashboard**: System observability panel

## Consequences

### **Positive**
- Demonstrates full-stack + cloud capabilities
- Scales without architectural rewrite
- Shows product engineering evolution
- Interactive CV experience (rare and impressive)
- Professional UI that doesn't overshadow infrastructure

### **Negative**
- More complex than basic HTML
- Requires build process and Node.js
- Risk of overengineering if not disciplined

### **Mitigation Strategies**
- API contracts defined first, UI second
- Regular "system vs UI" priority checks
- Keep deployment pipeline simple
- Maintain static HTML fallback

## Success Metrics
- ✅ APIs are source of truth (not mock data in `resumeData.ts`)
- ✅ APIExplorer shows real endpoints with live responses
- ✅ HealthDashboard connects to actual CloudWatch metrics
- ✅ Static build deploys successfully to S3
- ✅ Navigation works smoothly (fix hash routing)
- ✅ Mobile responsive design

## Next Steps
1. **Fix navigation issues**: Hash-based scrolling, smooth scroll
2. **Wire real APIs**: Replace mock data with actual backend calls
3. **Add scroll animations**: Enhance user experience
4. **CloudWatch integration**: Connect HealthDashboard to real metrics

---

*This ADR ensures the frontend enhances rather than overshadows the infrastructure demonstration while maintaining the core value proposition of a "living architecture resume."*