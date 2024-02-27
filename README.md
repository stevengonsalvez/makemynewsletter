# The newsletter platform

[![UNDER CONSTRUCTION](https://img.shields.io/badge/UNDER%20CONSTRUCTION-FF0000)]()
## Introduction

The newsletter platform is designed to be your second brain, helping you manage cognitive overload and information overload from your daily browsing and reading. It contextualizes the information for you and delivers it when you need it, reducing anxiety and improving productivity.

## Table of Contents

- [The newsletter platform](#the-newsletter-platform)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [for local dev](#for-local-dev)
  - [Features](#features)
    - [Codebase Features](#codebase-features)
  - [Contributing](#contributing)
  - [Acknowledgements](#acknowledgements)
  - [Gotcha's](#gotchas)



## Getting Started

### for local dev

- create a virtual env 
```
python -m venv venv
source ./venv/bin/activate
```

- create a .env file 
```
cp .env.example .env
```

- at the root folder ` export PYTHONPATH="$PYTHONPATH:$PWD"`
- install dependencies
```
pip install -r requirements.txt
```

- check browser capture
```
python src/talktothebrowser.py
```

or run the file on vscode selecting the correct python interpreter


## Features

- **Knowledge Graph Interaction:** Seamlessly interact with your browsers to create a knowledge graph out of various sources, including blogs, videos, threads, and codebases.
- **Newsletter Generation:** Automatically generate newsletters based on the knowledge graph contextualized from your activities and interests.
- **Chat with Your Second Brain:** Engage in meaningful conversations with your AI-enhanced second brain to clarify doubts, explore concepts, and more.

### Codebase Features


- **Code Summarization:** Get concise natural language summaries for code snippets and documentation, aiding quick comprehension.
- **Code Search:** Utilize natural language queries to find relevant functions/classes within the codebase.
- **Code Generation:** Generate code examples and templates for common tasks to enhance productivity.
- **Code Q&A:** Ask the AI assistant questions in natural language about your codebase for helpful insights.

## Contributing

We welcome contributions to the Developer Productivity Platform! Please read through our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest enhancements.

## Acknowledgements


## Gotcha's
- if `pyobjc` does not install properly then do the following for using foundation and applescript on the mac, need to execute this separately within the virtualenv

```
pip install -U 'pyobjc[allbindings]'
```