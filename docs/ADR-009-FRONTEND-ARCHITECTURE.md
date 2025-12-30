# ADR-009: Frontend Architecture Decision

**Date**: 2024-12-19  
**Status**: Accepted  
**Decision Makers**: Development Team

## Context
Need to choose frontend architecture for Oyin's Journey that balances:
- Professional engineering signal
- Static hosting compatibility (S3 + CloudFront)
- Scalability without rewrite
- Cloud engineer brand alignment

## Decision
Implement **React + TypeScript + Vite** with **shadcn/ui + Tailwind** architecture:

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                # shadcn components
│   │   ├── APIExplorer.tsx    # ⭐ differentiator
│   │   └── HealthDashboard.tsx # ops thinking
│   ├── services/
│   │   └── api.ts             # real backend calls
│   ├── hooks/
│   │   └── useApi.ts
│   └── types/
│       └── index.ts
└── oyins-journey.html         # fallback static version
```

## Rationale

### ✅ **Engineering Signal**
- Clear separation of concerns
- Scalable React architecture
- TypeScript for contracts
- Professional tooling (Vite, Tailwind)

### ✅ **Differentiators**
- **APIExplorer**: Interactive API documentation
- **HealthDashboard**: Shows ops maturity
- **oyins-journey.html**: Accessibility/fallback thinking

### ✅ **Static Hosting Compatible**
- No runtime dependencies
- Builds to static files
- S3 + CloudFront ready
- Free-tier safe

## Implementation Principles

### 🎯 **API-First Development**
- Define contracts in `types/` BEFORE UI
- Real backend calls in `services/api.ts`
- Keep `data/` minimal (dev/mock only)

### 🎯 **Selective Component Usage**
- Use shadcn/ui deliberately, not exhaustively
- Focus on functionality over aesthetics
- Remember: "The system is the product, not the UI"

## Consequences

### **Positive**
- Demonstrates full-stack capabilities
- Scales without architectural rewrite
- Shows cloud + frontend engineering
- Interactive CV experience

### **Negative**
- More complex than basic HTML
- Requires build process
- Risk of overengineering

### **Mitigation**
- API contracts defined first
- Regular "system vs UI" priority checks
- Keep deployment pipeline simple

## Success Metrics
- APIs are source of truth (not mock data)
- APIExplorer shows real endpoints
- HealthDashboard connects to CloudWatch
- Static build deploys successfully

---

*This ADR ensures the frontend enhances rather than overshadows the infrastructure demonstration.*