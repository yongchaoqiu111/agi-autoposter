# Chapter 9: Layer-by-Layer Hallucination Filtering

---

## 9.1 The Nature of Hallucination

Hallucination in large models is not a bug; it is an inherent characteristic.

It will fabricate: non-existent facts, non-existent instructions, non-existent states, non-existent interface parameters.

Existing frameworks generally attempt to "reduce" hallucinations, but no framework can fundamentally "eliminate" them.

The approach of this architecture is not to "make AI hallucinate less," but to **prevent hallucinations from escaping into the real world**.

---

## 9.2 Four-Layer Filtering Mechanism

### Layer One: Content Layer Filtering

**No room for fabrication.**

The content layer does not output "content"; it only outputs "content IDs."

The large model cannot see the full content; it only sees content_id and cannot fabricate out of thin air.

**Filtering effect: The large model cannot fabricate new content.**

### Layer Two: Scheduling Layer Filtering

**No opportunity for hallucination.**

The scheduling layer only allows selection from a whitelist of platforms, IDs, and configurations.

The large model cannot hallucinate non-existent platforms or parameters.

**Filtering effect: Hallucination is limited to "selection," not "instruction fabrication."**

### Layer Three: Execution Layer Filtering

**Trust no input.**

The execution layer enforces validation of parameter format, range, and legality, rejecting illegal input.

**Filtering effect: Even if the upper layer passes wrong parameters, the execution layer will intercept them.**

### Layer Four: Supervision Layer Filtering

**Block anomaly propagation.**

Task failure is only recorded, does not spread, does not propagate, does not affect other atoms.

**Filtering effect: Anomalies are isolated and will not spread globally.**

---

## 9.3 Complete Chain of Four-Layer Filtering

```plaintext
Large model generates instruction
    │
    ▼
  Content Layer (Only exposes IDs → Cannot fabricate)
    │
    ▼
  Scheduling Layer (Whitelist selection → Cannot fictionalize)
    │
    ▼
  Execution Layer (Strong parameter validation → Rejects illegal)
    │
    ▼
  Supervision Layer (Failure isolation → Does not spread)
    │
    ▼
  Real World (Safe)
```

---

## 9.4 Comparison with Traditional Approaches

| Approach | Handling Method | Effect |
|----------|----------------|--------|
| Traditional Agent | Attempts to make large model "not hallucinate" | Cannot cure the root cause |
| MCP Protocol | No filtering, direct execution | Hallucinations may directly land |
| This Architecture | Four-layer filtering, layer-by-layer interception | Hallucinations are isolated, cannot escape |

---

## 9.5 Why This Filtering Mechanism Works

The design principle can be summarized in one sentence:

> **Do not trust the large model.**

Trust decreases layer by layer; validation increases layer by layer.

---

## 9.6 Real Case: How Hallucinations Are Filtered

Assume the large model hallucinates:

```plaintext
platform: "douyin2" (non-existent)
txt_id: 999 (non-existent)
```

- **Content Layer**: ID not in list, cannot generate
- **Scheduling Layer**: Platform is illegal, directly rejected
- **Execution Layer**: No opportunity to execute
- **Supervision Layer**: Records for auditing, does not spread

**Result: The hallucination is locked down throughout the process and never reaches the real world.**

---

## 9.7 Industry Idea Absorption and Design Philosophy of Atomic Architecture

A recent article on AI test token consumption optimization (*Playwright MCP burns 1.5M tokens. CLI does it in 27k.*) confirms the rationality of the atomic three-layer architecture from a cost perspective. The article shows: the token cost difference between interactive exploration and fixed script execution can reach 50-60 times.

This phenomenon is not a problem in atomic architecture, but a natural design choice:

- **Exploratory Atoms**: Handle unknown events, used to find answers, verify rules, generate deterministic results.
- **Execution Atoms**: Handle confirmed, satisfied events, used for large-scale, high-concurrency, low-cost stable execution.

The two types of atoms are completely independent, not nested, not calling each other, can be concurrent, and have failure isolation.

The core design philosophy of the architecture is:

> **Once satisfied, no more exploration.**

When an exploratory atom produces a standard answer that meets expectations, the result will be solidified as the fixed logic of an execution atom. For all subsequent identical tasks, they will be directly completed by the execution atom in a scripted, low-cost, high-efficiency manner, without repeatedly triggering the exploration process.

We often say this architecture does not do "AI self-evolution," but it actually achieves sustainable evolution capability in the lightest, most robust, and most industrial way:

- **Not satisfied** → Allow local exploration
- **Satisfied** → Solidify into execution atoms
- Evolution only occurs within a single atom
- Never spreads, never links, never goes out of control

This is a human-controllable evolution:

> AI is responsible for trying, humans are responsible for acceptance, architecture is responsible for safety.

Without high cost, without high risk, without full system restart,

the system can continue to improve while maintaining stability.

This is not a functional limitation, but a mature trade-off of industrial-grade systems:

> Use one reasonable exploration cost in exchange for millions of stable, efficient, low-cost executions.

The scheduling, execution, and supervision layers always remain independent, not mixed, not nested, not strung into a linear process.

---

## Chapter Summary

| Filtering Layer | Responsibility | Effect |
|----------------|---------------|--------|
| Content Layer | Only outputs IDs | Cannot fabricate new content |
| Scheduling Layer | Whitelist selection | Cannot fabricate non-existent platform / ID |
| Execution Layer | Strong parameter validation | Illegal parameters are rejected |
| Supervision Layer | Anomaly isolation | Failure does not spread or propagate |

**Four layers of filtering, layer-by-layer interception; absorb cutting-edge ideas, adhere to architectural trade-offs;**

**Let hallucinations have nowhere to hide, let the system remain stable at scale.**
