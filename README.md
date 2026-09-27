# ArrowLens

> An accessibility-focused developer tool that helps developers understand errors, documentation, implementation ideas, and unfamiliar codebases through focused AI-powered workflows.

---

## 🚀 Overview

Developers constantly switch between error messages, source code, documentation, repositories, notes, and AI tools just to understand what to do next.

ArrowLens brings these workflows into one focused environment.

Instead of functioning as a generic AI chatbot, ArrowLens provides four task-specific **Lenses**, each designed around a particular developer problem:

- **Error Lens** — understand and debug errors
- **Docs Lens** — simplify technical documentation
- **Plan Lens** — turn rough ideas into implementation plans
- **Codebase Lens** — explore and understand unfamiliar projects

The interface is designed with accessibility and cognitive clarity in mind, providing tools such as Focus Mode, Spotlight Mode, High Contrast, Reduced Motion, keyboard-friendly interactions, structured information hierarchy, and readable code presentation.

## Video Demo

**[https://drive.google.com/file/d/1wXBZuOS2i1pUGY8vdIMeUMjTjqVQSfw1/view?usp=sharing]**

The demonstration showcases the core ArrowLens workflows and accessibility features.
# 📸 Screenshots

## Landing Page

![ArrowLens Landing Page](screenshots/landing.png)

---

## Dashboard

![ArrowLens Dashboard](screenshots/dashboard.png)

---

## Error Lens

![ArrowLens Error Lens](screenshots/e-lens.png)

---

## Docs Lens

![ArrowLens Docs Lens](screenshots/d-lens.png)

---

## Plan Lens

![ArrowLens Plan Lens](screenshots/p-lens.png)

---

## Codebase Lens

![ArrowLens Codebase Lens](screenshots/cb-lens.png)

---

## Accessibility Features

![ArrowLens Accessibility Features](screenshots/accessibility.png)

---

# 🔎 The Four Lenses

## 01 — Error Lens

Error messages often provide information without explaining what the developer should actually do.

Error Lens accepts:

- An error message
- Relevant code
- Additional context

It produces a structured explanation containing:

- **Problem**
- **Likely Cause**
- **Suggested Fix**
- **Verification**

This gives the developer a clearer path from an error to the next debugging step.

---

## 02 — Docs Lens

Technical documentation can contain large amounts of information that are difficult to process quickly.

Docs Lens allows developers to:

- Paste documentation
- Provide a documentation URL
- Fetch documentation content
- Edit the extracted content
- Analyze the documentation

The result is organized into:

- **Summary**
- **Key Concepts**
- **Example**
- **Common Mistake**

Markdown and code examples are presented in a readable, syntax-highlighted format.

---

## 03 — Plan Lens

Developers often have an idea without having a clear implementation path.

Plan Lens transforms rough ideas or notes into structured implementation plans.

Each plan can contain:

- A title
- A goal
- Implementation steps
- Actions
- Dependencies
- Verification steps

Plans can also be represented visually through an implementation map.

The workflow becomes:

**Idea → Plan → Implementation**

---

## 04 — Codebase Lens

Understanding an unfamiliar codebase can require navigating dozens or hundreds of files.

Codebase Lens allows developers to import:

- ZIP projects
- Public GitHub repositories

After importing a project, developers can:

- Explore files
- View syntax-highlighted source code
- Inspect file relationships
- Ask questions about the codebase
- Explain individual files
- Explain selected sections of code
- Copy useful context for other AI coding tools

An interactive implementation map helps visualize relationships between project files.

---

# ♿ Accessibility

Accessibility is integrated into the main ArrowLens workflow rather than being treated as an afterthought.

ArrowLens includes:

### Focus Mode

Reduces surrounding interface distractions and centers attention on the primary task.

### Spotlight Mode

Dims surrounding content so the currently relevant interface area receives greater visual attention.

### High Contrast

Provides stronger visual separation between interface elements.

### Reduced Motion

Reduces unnecessary interface animations and transitions.

### Keyboard-Friendly Interaction

Important controls and workflows are designed to remain accessible through keyboard interaction.

### Structured Information

AI output is divided into predictable sections instead of being presented as a large unstructured response.

### Readable Code

Source code uses line numbers, syntax highlighting, selection support, and horizontal scrolling where required.

---

# 🧠 Designed Around Developer Tasks

ArrowLens is built around the question:

> **What is the developer trying to understand right now?**

Rather than starting with a blank AI chat box, the user starts with a task.

```text
Error
  ↓
Error Lens
  ↓
Understand the problem
  ↓
Take action