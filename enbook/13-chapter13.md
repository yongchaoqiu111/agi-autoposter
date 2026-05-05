# Chapter 13: When to Use This Architecture

## 13.1 Suitable Scenarios

This architecture is suitable for:

- **Social media management**: Multi-platform posting, scheduling
- **Data collection**: Regular API calls, data aggregation
- **Hardware control**: Robotic arms, conveyor belts, sensors
- **Financial operations**: Regular transactions, reconciliation
- **Medical systems**: Prescription verification, record management

**Common characteristics**:

- Need stability
- Need controllability
- Need observability
- Clear responsibility

## 13.2 Unsuitable Scenarios

This architecture is not suitable for:

- **Creative writing**: Need AI to "create" new content
- **Research exploration**: Need AI to "discover" new knowledge
- **Gaming AI**: Need AI to "adapt" to player behavior
- **Personal assistants**: Need AI to "understand" user intent

## 13.3 Decision Tree

```
Do you need stability? -> Yes -> Do you need controllability? -> Yes -> Use this architecture
                            |                              |
                            No                             No
                            |                              |
                    Consider other frameworks      Consider other frameworks
```

## 13.4 Migration Path

If you are using other frameworks and want to migrate:

1. **Identify stable parts**: Which parts need stability?
2. **Extract as atoms**: Convert stable parts to atoms
3. **Add supervision layer**: Record all operations
4. **Gradual migration**: Migrate atom by atom, not all at once

---

## Chapter Summary

| Scenario | Suitable? | Reason |
|----------|-----------|--------|
| Social media management | Yes | Need stability, controllability |
| Data collection | Yes | Need observability |
| Hardware control | Yes | Need stability, clear responsibility |
| Financial operations | Yes | Need stability, controllability |
| Creative writing | No | Need creativity |
| Research exploration | No | Need evolution |
| Gaming AI | No | Need self-adaptation |
| Personal assistants | No | Need understanding |

*One-sentence summary: Use this architecture when you need stability, controllability, and observability. Do not use it when you need creativity, evolution, or self-adaptation.*
