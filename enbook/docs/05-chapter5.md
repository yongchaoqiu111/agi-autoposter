# Chapter 5: Atomic Characteristics

---

## 5.1 What Is an Atom

An atom is the smallest, independent, and complete execution unit in the system.

One atom = a complete internal three-layer structure: content + scheduling + execution.

Atoms are independent, replaceable, composable, and isolated.

---

## 5.2 Between Atoms: No Links, No Communication, No Dependencies

There is no direct association between atoms:

- No shared memory
- No mutual calls
- No message passing
- No dependency on results

No links = no coupling

No coupling = infinite scalability

---

## 5.3 Between Atoms: Unaware of Each Other's Existence

Each atom only cares about its own execution,

and does not need to know whether other atoms exist, whether they succeed, or whether they fail.

This ensures the system will never crash due to complexity explosion.

---

## 5.4 One Atom Fails, No Impact on Any Other Atom

Failure is completely locked within a single atom.

No spread, no contagion, no blocking, no chain reaction.

This is the foundation of industrial-grade high availability.

---

## 5.5 Atoms Can Be Independently Tested, Deployed, and Upgraded

Atoms have no dependencies, so:

- Can be upgraded independently
- Can be replaced independently
- Can be restarted independently
- Can be scaled independently

The system never needs downtime, never needs full updates.

---

## 5.6 Atoms Can Be Software or Hardware

Atoms do not care about the runtime environment:

software processes, Docker, hardware devices, robotic arms, sensors...

As long as they follow the three-layer structure, they are atoms.

Unified architecture, extending from software to hardware.

---

## Chapter Summary

The power of atoms comes from minimalism and isolation:

No links, no communication, no perception, no spread.

Small and stable, then large and strong.
