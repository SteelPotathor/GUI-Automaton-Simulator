![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<h1 align="center"> GUI Automaton Simulator </h1>
<h3 align="center"> Semester 6 - Formal Language Theory </h3>
<h5 align="center"> Project Assignment - <a href="https://www.univ-jfc.fr/">Champollion University</a> (January-March 2024) </h5>

<p align="center">
    <img src="img/automaton_presentation.gif">

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents </h2>

<details open="open">
    <summary>Table of Contents</summary>
<ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#overview"> ➤ Overview</a></li>
    <li><a href="#install"> ➤ Requirements</a></li>
    <li><a href="#change-music"> ➤ Functions</a></li>
    <li><a href="#credits"> ➤ Credits</a></li>
</ol>
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project"> :pencil: About The Project</h2>

<p>
    This project is a <strong>Finite Automaton Simulator</strong> with a graphical user interface, developed in Python 3 as part of a course on <strong>Formal Language Theory</strong>. The simulator supports both <strong>Deterministic Finite Automata (DFA)</strong> and <strong>Nondeterministic Finite Automata (NFA)</strong>, two key models in automata theory.
</p>

<h3>What is a Finite Automaton?</h3>

<p>
    In computer science, a <strong>finite automaton</strong> (or <strong>finite state machine</strong>) is a mathematical model used to represent systems that have a finite number of possible states. Finite automata are fundamental in pattern recognition, lexical analysis, and parsing, where they are used to recognize sequences of symbols that match specific rules.
</p>

<p>There are two primary types of finite automata:</p>

<ol>
    <li>
        <strong>Deterministic Finite Automaton (DFA):</strong>
        <p>
            In a DFA, for each state and input symbol, there is exactly one transition to another state. This predictability makes DFAs simpler to understand and implement but also limits their flexibility. DFAs are often used in applications like lexical analyzers in compilers, where each input leads deterministically to a single next state.
        </p>
    </li>
    <li>
        <strong>Nondeterministic Finite Automaton (NFA):</strong>
        <p>
            In an NFA, for each state and input symbol, there can be multiple possible transitions, or even none. This non-determinism allows NFAs to be more flexible in representing complex patterns, though they can be harder to simulate directly. Despite this, any NFA can be converted into an equivalent DFA, making both models equally powerful in terms of the languages they can recognize.
        </p>
    </li>
</ol>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="overview"> :cloud: Overview</h2>

<p>
    This simulator allows users to <strong>create, visualize, and test both DFAs and NFAs</strong>. Through the graphical interface, users can define states, transitions, and inputs for either type of automaton and simulate their behavior with specific input sequences. The simulator visually demonstrates how an input sequence navigates through the automaton's states and indicates whether it reaches an accepting state (a successful match).
</p>

<p>
    I developed this project with the intention of creating a tool that I could reuse and expand upon in the future. To achieve this, I went beyond the course requirements to build a powerful, user-friendly simulator that makes exploring automata theory engaging and accessible. This tool combines enhanced functionality and a flexible design, allowing for deeper experimentation with DFAs, NFAs, and pattern recognition within strings.
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="setup"> :computer: Installation and Setup</h2>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="features"> :small_red_triangle_down: Features</h2>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="usage"> :question: How to Use the Simulator?</h2>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="examples"> :crystal_ball: Basic Examples</h2>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="acknowledgments"> :mega: Acknowledgments</h2>

<ul>
    <li><strong>Thorgrimm</strong> for taking care of the entire graphical interface, making the simulator user-friendly and visually appealing.</li>
    <li><strong>Professor Thierry Montaut</strong> for providing valuable guidance and insights during the Formal Language Theory course, helping to shape and refine the project.</li>
    <li><strong>Myself</strong> for handling the algorithmic part of the automata, ensuring that the core functionality of DFA and NFA simulations works smoothly.</li>
</ul>
