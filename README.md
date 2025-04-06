# GSoC 2025 Proposal Support: Gemini Robustness Evaluation

**Applicant:** Somtochukwu Onyekwelu
**GSoC Organization:** Google (DeepMind)
**Project Idea:** Evaluate Gemini on an Open-Source Benchmark

---

## Overview

This repository contains supporting materials and proof-of-concept code for my Google Summer of Code 2025 application. The proposed project centers on a crucial aspect of real-world AI deployment: **robustness**. Specifically, it aims to rigorously evaluate the multimodal capabilities of Google's Gemini models when faced with **imperfect, noisy inputs in both image and text modalities**.

Standard benchmarks often rely on high-quality data. This project moves beyond that limitation by systematically introducing controlled noise (e.g., blur, occlusion for images; typos, semantic shifts for text) to the VQA v2 benchmark dataset.

Crucially, this evaluation will extend **beyond typical English-centric analysis**. By assessing performance across **English** (high-resource), **Hindi** (medium-resource, different script), and **Igbo** (low-resource, different grammatical structure), the project will provide valuable insights into Gemini's **linguistic fairness and robustness** across diverse user populations. Understanding how noise impacts performance differently across these languages is vital for building truly globally applicable AI.

This repository currently serves to demonstrate initial technical feasibility, particularly for image noise injection, and my proactive engagement with the project's core requirements.

## Purpose of this Repository

The primary purpose of this repository **at the proposal stage** is to:

1.  **Demonstrate Proactivity:** Show active development on core components outlined in my proposal.
2.  **Prove Technical Feasibility:** Provide working proof-of-concept code for key technical challenges (initially focusing on image noise injection).
3.  **Illustrate Planned Methodology:** Give a tangible example of the noise generation approach that will be extended to text and applied systematically.
4.  **Support Proposal Claims:** Offer concrete evidence of my understanding of the required tools (Python, OpenCV, NumPy) and the project's technical direction.

This repository will host the full project codebase if the proposal is accepted.

## Current Functionality: Proof-of-Concept (Image Noise Injection)

The repository currently includes:

*   **`.gitignore`**: Standard Python environment exclusions.
*   **`requirements.txt`**: Initial project dependencies (OpenCV, NumPy).
*   **`src/ImageNoiseFunctions.py`**: A Python script demonstrating the implementation of the two core **image noise** types proposed:
    *   **Gaussian Blur:** Simulates out-of-focus or low-detail images ("low", "medium", "high" levels map to sigma values).
    *   **Occlusion:** Simulates partially hidden objects ("low", "medium", "high" levels map to % area occluded with mean image color).
    *   The script includes helper functions, type hinting, error handling, and a runnable example to visualize the noise effects clearly.

This initial code **validates the approach** for generating controlled image degradation programmatically. The **next step** in the full project involves implementing analogous functions for **text noise**.

## Planned Methodology (GSoC Project Summary)

The full GSoC project methodology includes:

1.  **Benchmark & Dataset:** VQA v2 dataset, providing image-question-answer triplets.
2.  **Multilingual Scope:** Evaluate on original English data and automatically translated versions for **Hindi** and **Igbo** to assess performance across varying linguistic resource levels and structures.
3.  **Multimodal Noise Injection:** Apply controlled noise systematically:
    *   **Image Noise:** Gaussian Blur, Occlusion (levels: Low, Medium, High) - PoC implemented.
    *   **Text Noise:** Character-Level Noise (typos), Back-Translation (semantic shifts via MT) (levels: Low, Medium, High) - To be implemented.
4.  **Model Integration:** Utilize Google's Gemini models via available APIs for inference on the noisy image-text pairs.
5.  **Evaluation Metric:** Quantify robustness using standard **VQA Accuracy**. The primary outcome will be the **performance drop** compared to clean baselines for each language/noise condition.
6.  **Analysis & Insights:** Analyze how different noise types/levels impact accuracy across the three languages, identifying specific model sensitivities and potential disparities.

## Setup and Usage (Current Proof-of-Concept)

To run the current image noise demonstration:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SomtoOnyekwelu/gsoc-2025-gemini-robustness.git
    cd gsoc-2025-gemini-robustness
    ```
2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the example script:**
    ```bash
    python src/ImageNoiseFunctions.py
    ```
    *   Displays examples of the implemented image noise effects using OpenCV's `imshow` (if GUI is available/enabled).

## Future Work (If Proposal Accepted)

Following acceptance into GSoC 2025, the project milestones include:

*   Implementing text noise functions (Character Noise, Back-Translation).
*   Securing API access and integrating Gemini inference.
*   Setting up the VQA dataset processing pipeline (including handling translations).
*   Executing systematic evaluation experiments across all defined conditions.
*   Conducting thorough result analysis and documenting insights.
*   Preparing a final report and potentially contributing reusable code modules.

---

Thank you for considering my application. I am highly motivated to tackle this challenging evaluation of Gemini's multimodal and multilingual robustness under the mentorship available at Google DeepMind.