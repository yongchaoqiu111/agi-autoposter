# Chapter 2: Why Existing Frameworks Are Unstable

## 2.1 Large Model Hallucinations Cannot Be Eliminated

Hallucination is not a bug; it is a characteristic of large models. They will fabricate non-existent facts, non-existent instructions, non-existent states.

Existing frameworks attempt to "reduce" hallucinations, but no framework can "eliminate" them.

**As long as hallucinations exist, the system is not stable.**

## 2.2 Execution Layer and Decision Layer Are Coupled

In protocols like MCP, tool invocation and decision logic are coupled together. Whoever can write the configuration can execute arbitrary commands.

This means the system's trust boundary is blurred: you cannot distinguish between "this is legitimate scheduling" and "this is a malicious operation caused by hallucination."

## 2.3 No Unified Supervision Layer

Most Agent frameworks do not have the concept of a "supervision layer." Once a task is sent out, you do not know what happens next: Did it succeed? Did it fail? Why did it fail? What if it gets stuck?

**Without supervision, there is no controllability.**

## 2.4 Cannot Find Responsibility When Things Go Wrong

When a task fails, existing frameworks struggle to answer: Is it the large model's problem? The tool's problem? A network problem? Or a configuration problem?

**Unclear responsibility means no improvement.**

---

## Chapter Summary

| Problem | Cause |
|---------|-------|
| Hallucinations cannot be eliminated | Large model characteristic |
| Execution and decision are coupled | Blurred trust boundary |
| No supervision layer | Cannot trace |
| Unclear responsibility | Cannot improve |

Industrial-grade systems need an architecture that is observable, traceable, and has clear responsibilities.
