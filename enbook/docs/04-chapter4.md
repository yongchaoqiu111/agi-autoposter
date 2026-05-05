# Chapter 4: Three-Layer Structure Definition

---

## 4.1 Content Layer: Only Outputs IDs

The content layer does not output real content; it only outputs content IDs.

Its responsibilities are only three: store content, assign unique IDs, and only expose IDs externally.

The large model cannot see the original text, images, or videos; it only sees indexes like content_id=5.

No room for fabrication, cutting off hallucinations from the source.

---

## 4.2 Scheduling Layer: Only Selects IDs

The scheduling layer is driven by the large model, but it does not create, execute, or explore.

It only does one thing: select IDs from a whitelist.

- Does not fabricate platforms
- Does not fabricate content
- Does not fabricate parameters
- Does not parse web pages in real-time
- Does not run browsers

The lighter the scheduling layer, the more stable, faster, and more token-efficient the system.

---

## 4.3 Execution Layer: Only Recognizes Parameters

The execution layer is pure scripts, pure fixed logic, no intelligence.

It only does one thing: execute according to parameters.

The execution layer does not think, does not decide, does not validate whether it should be done,

it only ensures: whatever parameters are given, whatever actions are performed.

This is the only correct structure for large-scale, high-concurrency, low-cost systems.

---

## 4.4 Supervision Layer: Only Records the Truth

The supervision layer does not intervene, does not block, does not validate in real-time.

It only records facts: success, failure, duration, errors, results.

The supervision layer is the system's memory,

not the system's police.

It provides truth, does not make judgments.

---

## Chapter Summary

The core of the three-layer structure is complete decoupling:

- **Content Layer**: Provides IDs
- **Scheduling Layer**: Selects IDs
- **Execution Layer**: Executes IDs
- **Supervision Layer**: Records results

Each layer only does its own work, does not intrude, does not mix, does not nest.
