# Chapter 7: Composition Rules of Atoms

---

## 7.1 Why Composition Rules Are Needed

Atoms are small, but business is large.

Composition rules allow small atoms to build large-scale systems without breaking atomic characteristics.

---

## 7.2 Three-Layer Composition: Atom → Molecule → System → Ecosystem

- **Atom**: Smallest execution unit
- **Molecule**: A scheduling plan for a group of atoms (not a super atom)
- **System**: A business collection of multiple molecules
- **Ecosystem**: Collaboration of multiple systems

Composition only does scheduling, does not create new logic.

---

## 7.3 Composition Rule One: Any Content + Any Scheduling + Any Execution = New Event

The three layers are completely decoupled and can be freely combined.

No need for pre-definition, no development, no code changes.

---

## 7.4 Composition Rule Two: Composition Maintains All Atomic Characteristics

Composition does not break:

- No links
- No communication
- Failure isolation
- Independent deployment

Infinite composition, complexity does not explode.

---

## 7.5 Composition Rule Three: Composition Is Scheduling, Not Inheritance

Composition does not create super atoms; it only configures execution order and timing.

No new code, no new logic, no new coupling.

---

## 7.6 Composition Boundary: Atoms Do Not Directly Call or Depend on Each Other

- **Wrong**: Atom A → calls → Atom B
- **Correct**: Scheduling layer → schedules A → schedules B

All dependency relationships are moved up to the scheduling layer, keeping atoms pure.

---

## Chapter Summary

The core of composition rules:

Only build frameworks, do not modify atoms;

Only do scheduling, do not create;

Can scale infinitely, yet remain forever stable.
