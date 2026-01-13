# Reimagining a Classic in a New World

## Overview
This project implements a structured, schema-driven pipeline that reimagines a classic narrative in a new fictional world while preserving its original narrative structure, character roles, and emotional intent.

Instead of directly rewriting the source text, the system first extracts a **loss-minimal narrative schema**, which becomes the single source of truth for all subsequent transformations.

The final output is a fully generated long-form story (3000–4000 words) with a newly generated title, exported as a PDF.

---

## Narrative Transformation Pipeline

![Narrative Transformation Pipeline](./ChatGPT%20Image%20Jan%2012,%202026,%2005_53_56%20PM.png)

The pipeline enforces controlled transformation through structured prompts, deterministic extraction, and causal consistency across stages.

---

## Pipeline Flow

### 1. Input Parsing
- Source PDF is loaded using a PDF parser.
- Text is extracted page-by-page.
- Extracted text is chunked to respect LLM context limits.
- Chunking enables scalability and stability for large documents.

---

### 2. Schema Extraction
- Each chunk is passed through a **strict schema-extraction prompt**.
- Temperature is set to **0** for deterministic output.
- Schema is written incrementally to a **plain-text (.txt) file**.

#### Extracted Schema Includes:
- Themes  
- Tone  
- Setting / world type  
- Characters and narrative roles  
- Ordered plot beats  
- Resolution style  

> The extraction prompt explicitly forbids inference, invention, or reinterpretation.

---

### 3. World & Character Mapping
- The schema is mapped onto a user-defined target world.
- Characters are re-anchored while preserving:
  - Narrative role
  - Motivation
  - Emotional intent
  - Relationships

---

### 4. Plot Transformation
- Original plot beats are rewritten to fit the new world.
- Narrative order, causality, and escalation remain unchanged.
- Structural alterations are prohibited.

---

### 5. Outline Generation
- Transformed plot beats are organized into a **three-act structure**:
  - Act I – Setup
  - Act II – Escalation
  - Act III – Resolution
- This outline serves as a blueprint for prose generation.

---

### 6. Long-Form Story Generation
- A novelist-style prompt expands the outline into full prose.
- Optimized for:
  - 3000–4000 words
  - Emotional pacing
  - Scene-based expansion
  - Internal consistency

---

### 7. Title Generation
- A concise, evocative title is generated **after** the story is complete.
- Ensures the title reflects the final narrative rather than influencing it.

---

### 8. Assembly & Output
- Title and story are assembled into a single document.
- Final output is compiled and exported as a **PDF**.

---

## Solution Design

### Schema-First Approach
The system separates **understanding** from **generation** by extracting a structured narrative schema before any transformation occurs.

This approach:
- Minimizes semantic loss
- Prevents creative drift
- Enables deterministic transformations

The schema becomes the **single source of narrative truth**.

---

### Controlled Pipeline Logic
All pipeline stages enforce:
- Structured prompts
- Iterative processing
- Causal consistency
- Deterministic output

---

## Challenges & Mitigations

### Schema Extraction Reliability
- JSON/YAML formats caused inconsistencies.
- Solution: tightly constrained **plain-text schema format**.

### Large File Processing
- Single-pass processing was slow and unstable.
- Solution: chunk-based extraction to avoid context overflow.

### Performance Constraints
- Lightweight models used for extraction and transformation.
- Larger models reserved for final generation.

---

## Edge Cases
- Source PDFs may contain:
  - Licensing text
  - Page numbers
  - Author metadata
  - Front/back matter
- Extraction prompts explicitly ignore all non-narrative content.

> Output quality depends on the chosen LLM. Larger models improve quality at the cost of runtime.

---

## Future Improvements

### Persistent Narrative Memory
- Store schemas and transformations in a database
- Enable branching narratives and revisions
- Potential integration with **LangGraph**

### Interactive UI
- Visual pipeline editor
- Editable schemas and plot beats
- Real-time narrative preview

### Evaluation & Validation Layer
- Automated plot-beat completeness checks
- Character consistency validation
- Structural integrity enforcement

---

## Conclusion
This project demonstrates a deterministic, scalable approach to narrative transformation by prioritizing structured understanding before creative generation, enabling faithful reimagining across worlds without structural loss.
