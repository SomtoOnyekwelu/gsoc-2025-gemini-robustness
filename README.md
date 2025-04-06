# GSoC 2025 Proposal Support: Gemini Robustness Evaluation

**Applicant:** Somto Onyekwelu ([https://github.com/SomtoOnyekwelu](https://github.com/SomtoOnyekwelu))
**GSoC Organization:** Google DeepMind
**Project Idea:** Evaluate Gemini on an Open-Source Benchmark

---

## Overview

This repository contains supporting materials and **proof-of-concept (PoC) code** for my Google Summer of Code 2025 application. The proposed project aims to rigorously evaluate the **multimodal robustness** of Google's Gemini models on the **VQA v2 benchmark**.

The core idea is to move beyond standard evaluations using pristine data by systematically injecting controlled noise into both **image** (e.g., blur, occlusion) and **text** (e.g., typos, semantic shifts) inputs. A key aspect of this evaluation is its **multilingual scope**, assessing performance not only on English but also on automatically translated **Hindi** (medium-resource, Devanagari script) and **Igbo** (low-resource, unique structure) to understand robustness across diverse linguistic contexts.

The goal is to provide quantifiable benchmarks and comparative analysis of Gemini's performance under varying degrees of realistic input degradation, contributing valuable insights for model development, deployment, and fairness considerations.

This repository serves primarily to **demonstrate technical feasibility** and **proactive engagement** by providing initial implementations of the core noise generation mechanisms described in the full GSoC proposal.

## Purpose of this Repository (Proposal Stage)

1.  **Demonstrate Proactivity:** Show concrete steps already taken to implement core project components.
2.  **Prove Technical Feasibility:** Offer working Python code for the planned image and text noise injection methods.
3.  **Illustrate Methodology:** Provide tangible examples of the noise generation techniques using relevant libraries (OpenCV, NumPy, Python built-ins).
4.  **Support Proposal Claims:** Serve as direct evidence supporting the technical plan outlined in the GSoC proposal document.

*(This repository will host the full project codebase if the proposal is accepted for GSoC 2025.)*

## Current Functionality: Proof-of-Concept (Noise Injection)

The repository currently includes functional PoC implementations for the core noise mechanisms:

*   **`src/ImageNoiseFunctions.py`**: ([View Code](https://github.com/SomtoOnyekwelu/gsoc-2025-gemini-robustness/blob/main/src/ImageNoiseFunctions.py))
    *   Implements `apply_gaussian_blur` using OpenCV, controlled by sigma values corresponding to Low/Medium/High conceptual impact levels.
    *   Implements `apply_occlusion` using OpenCV, applying random rectangular patches (mean color filled) scaled for Low/Medium/High impact.
    *   Includes runnable example (`if __name__ == "__main__":`) demonstrating visual effects.
*   **`src/CharacterNoiseFunctions.py`**: ([View Code](https://github.com/SomtoOnyekwelu/gsoc-2025-gemini-robustness/blob/main/src/CharacterNoiseFunctions.py))
    *   Implements `add_char_noise` supporting Substitute, Delete, Insert, and Swap operations based on a target percentage (Low-5%, Med-15%, High-25%) of original characters modified.
    *   Uses a robust "build new list" approach for applying noise based on originally selected indices.
    *   Includes basic support for English, Hindi, and Igbo using simplified alphabets (**Note: Limitations explicitly documented in code comments**).
    *   Includes runnable example (`if __name__ == "__main__":`) demonstrating noise application on sample text for each language (using `random.seed(42)` for reproducible output).
*   **`requirements.txt`**: Lists necessary dependencies (OpenCV, NumPy).
*   **`.gitignore`**: Standard Python exclusions.

This PoC code validates the proposed approach for programmatically generating controlled noise for both modalities.

## Planned Methodology Summary (GSoC Project)

1.  **Benchmark & Languages:** VQA v2 dataset; evaluate on English, automatically translated Hindi & Igbo.
2.  **Noise:** Apply Image (Blur, Occlusion) and Text (CharNoise, BackTranslation) noise at Low(5%)/Medium(15%)/High(25%) intensity levels.
3.  **Model:** Evaluate Google Gemini (e.g., Pro Vision) via API.
4.  **Metric:** Analyze VQA Accuracy degradation (Absolute/Relative Drop vs. Baselines).
5.  **Goal:** Quantify and compare multimodal/multilingual robustness.

*(Please refer to the full GSoC proposal document for detailed methodology, timeline, and objectives.)*

## Setup and Usage (Current Proof-of-Concept Demos)

To run the demonstration scripts:

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
4.  **Run the desired demo script:**
    *   For Image Noise:
        ```bash
        python src/ImageNoiseFunctions.py
        ```
        *(This will typically display noisy images using OpenCV if a GUI is available)*
    *   For Character Noise:
        ```bash
        python src/CharacterNoiseFunctions.py
        ```
        *(This will print original and noisy sample text for English, Hindi, and Igbo to the console)*

## Future Work (If Proposal Accepted for GSoC 2025)

*   Finalize noise function implementations based on mentor feedback.
*   Implement the Back-Translation text noise mechanism.
*   Develop the full pipeline for VQA data handling, translation, Gemini API interaction, and result aggregation.
*   Execute systematic evaluation experiments.
*   Conduct thorough analysis and generate visualizations.
*   Produce the final report and codebase deliverables as outlined in the proposal.

---

Thank you for reviewing my supporting materials. I am enthusiastic about the potential of this project to contribute valuable insights into AI robustness and look forward to the possibility of developing it further during Google Summer of Code at DeepMind.

**References Mentioned in Proposal:**

*   Goyal, Y., et al. (2017). Making the V in VQA Matter... *CVPR*. ([visualqa.org](https://visualqa.org/))
*   Reuel, A., et al. (2024). BetterBench: Assessing AI Benchmarks... *arXiv:2402.08165*. ([arxiv.org/abs/2402.08165](https://arxiv.org/abs/2402.08165))